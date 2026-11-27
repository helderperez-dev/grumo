"""Release-gate smoke test for the default Grumo + Grumo Store journey.

This intentionally crosses the public/runtime seams a normal application uses:
Model data, durable queue work, event persistence and canonical Execution all
share one application.grumo and survive a full Store close/reopen cycle.
"""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from grumo.data import Model
from grumo.data.store_backend import bind_runtime_store
from grumo.primitives.intent import Intent
from grumo.runtime.execution import ExecutionStatus
from grumo.runtime.execution.engine import ComputeResult, ExecutionEngine
from grumo.runtime.store import (
    RuntimeStore,
    StoreConfig,
    bind_active_runtime_store,
)
from grumo.storage.events.store import GrumoStoreEventBus
from grumo.storage.execution.store import GrumoStoreExecutionStore
from grumo.storage.queue.store import GrumoStoreQueue


class JourneyRecord(Model):
    name: str
    value: int


def _bind(runtime: RuntimeStore) -> None:
    bind_active_runtime_store(runtime)
    bind_runtime_store(runtime)


def _unbind() -> None:
    bind_runtime_store(None)
    bind_active_runtime_store(None)


@pytest.mark.asyncio
async def test_store_first_application_domains_survive_restart(tmp_path: Path) -> None:
    path = tmp_path / ".grumo" / "application.grumo"

    runtime = RuntimeStore(StoreConfig(path=path))
    runtime.start()
    _bind(runtime)
    execution_id = ""
    record_id = None
    try:
        record = await JourneyRecord.create(name="counter", value=41)
        assert isinstance(record.id, UUID)
        assert record.id.version == 7
        record_id = record.id

        queue = GrumoStoreQueue()
        await queue.setup()
        job = await queue.enqueue(
            "recalculate",
            {"record_id": record.id},
            idempotency_key="journey-job-1",
        )
        assert job.type == "recalculate"

        bus = GrumoStoreEventBus()
        event = bus.publish("journey.created", {"record_id": record.id})
        assert event["event_type"] == "journey.created"

        engine = ExecutionEngine()
        execution_store = GrumoStoreExecutionStore()
        engine.use_store(execution_store)

        async def compute(_ctx):
            return ComputeResult(value={"record_id": record.id, "ok": True})

        execution = await engine.execute(
            Intent(name="journey.verify"),
            compute,
            actor="user:smoke",
        )
        assert execution.status is ExecutionStatus.COMPLETED
        execution_id = execution.id

        assert path.exists()
    finally:
        _unbind()
        runtime.stop()

    reopened = RuntimeStore(StoreConfig(path=path))
    reopened.start()
    _bind(reopened)
    try:
        persisted = await JourneyRecord.first(name="counter")
        assert persisted is not None
        assert record_id is not None
        assert persisted.id == record_id
        assert persisted.value == 41

        queue = GrumoStoreQueue()
        await queue.setup()
        jobs = await queue.list(task_type="recalculate")
        assert len(jobs) == 1
        assert jobs[0].idempotency_key == "journey-job-1"
        assert jobs[0].payload == {"record_id": str(record_id)}

        replayed: list[dict] = []
        bus = GrumoStoreEventBus()
        assert bus.replay("journey.created", replayed.append) == 1
        assert replayed[0]["payload"] == {"record_id": str(record_id)}

        execution_store = GrumoStoreExecutionStore()
        executions = execution_store.load_all()
        restored = next(item for item in executions if item.id == execution_id)
        assert restored.status is ExecutionStatus.COMPLETED
        assert restored.result == {"record_id": str(record_id), "ok": True}
    finally:
        _unbind()
        reopened.stop()
