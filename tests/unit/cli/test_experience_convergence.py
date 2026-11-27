"""Sprint 29 experience-convergence regression tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from grumo.agents.models import AgentEntity, AgentRunRecord
from grumo.agents.registry import GrumoStoreAgentRegistry
from grumo.cli import app
from grumo.cli.context import (
    acquire_execution_store,
    acquire_schedule_store,
)
from grumo.cli.new import _scaffold_offline
from grumo.cli.scaffolding import _fallback_ai_assets
from grumo.runtime.store import (
    RuntimeStore,
    StoreConfig,
    bind_active_runtime_store,
)


def test_grumo_new_scaffold_is_store_first(tmp_path: Path) -> None:
    project = tmp_path / "sample"
    _scaffold_offline(project, "sample")

    config = (project / "grumo.toml").read_text()
    home = (project / "app" / "page.py").read_text()

    assert "[store]" in config
    assert 'provider = "grumo"' in config
    assert 'path = ".grumo/application.grumo"' in config
    assert "from grumo.ui import" in home
    assert "from grumo import A" not in home
    assert list(project.rglob("*.db")) == []


def test_ai_scaffold_teaches_grumo_store_not_aiosqlite() -> None:
    assets = _fallback_ai_assets()
    persistence = assets[".grumo/ai/DATABASE.md"]
    rules = assets[".grumo/ai/RULES.md"]
    skills = assets[".grumo/ai/SKILLS.md"]

    combined = "\n".join((persistence, rules, skills))
    assert "application.grumo" in combined
    assert "from grumo import Model" in persistence
    assert "aiosqlite" not in combined
    assert ".grumo/state/data.db" not in combined


def test_cli_operational_store_creates_no_sqlite_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    executions, store_path = acquire_execution_store()
    try:
        assert store_path == ".grumo/application.grumo"
        assert Path(store_path).exists()
        assert executions.load_all() == []
    finally:
        executions.close()

    schedules, schedule_store_path = acquire_schedule_store()
    try:
        assert schedule_store_path == ".grumo/application.grumo"
        assert schedules.list_all() == []
    finally:
        schedules.close()

    assert list(tmp_path.rglob("*.db")) == []


@pytest.mark.asyncio
async def test_store_backed_agent_registry_round_trip(tmp_path: Path) -> None:
    runtime = RuntimeStore(StoreConfig(path=tmp_path / "application.grumo"))
    runtime.start()
    bind_active_runtime_store(runtime)
    try:
        registry = GrumoStoreAgentRegistry()
        agent = AgentEntity(agent_id="agent-1", name="Planner", model="mock:default")
        await registry.register(agent)

        restored = await registry.get("agent-1")
        assert restored is not None
        assert restored.name == "Planner"

        run = AgentRunRecord(
            run_id="run-1",
            agent_id="agent-1",
            prompt="plan",
            output="done",
            tokens_in=10,
            tokens_out=4,
        )
        await registry.record_run(run)
        runs = await registry.get_runs("agent-1")
        assert [item.run_id for item in runs] == ["run-1"]
        assert await registry.count_agents() == 1
        assert await registry.count_runs("agent-1") == 1

        assert await registry.delete("agent-1") is True
        assert await registry.get("agent-1") is None
        assert await registry.count_runs("agent-1") == 0
    finally:
        bind_active_runtime_store(None)
        runtime.stop()


def test_status_json_exposes_store_first_application_contract(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["status", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["store"]["provider"] == "grumo"
    assert payload["store"]["path"] == ".grumo/application.grumo"
    from grumo.config import get_config

    cfg = get_config()
    assert payload["providers"]["database"] == "grumo"
    assert payload["providers"]["queue"] == cfg.queue.provider
    assert payload["providers"]["objects"] == "grumo"
    assert payload["runtime"]["requests_total"] >= 0


def test_doctor_json_is_store_first_and_side_effect_free(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["doctor", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["application"]["store"]["provider"] == "grumo"
    assert payload["integrity"]["legacy_sqlite"] == []
    assert payload["integrity"]["store_first_clean"] is True
    assert not Path(".grumo/application.grumo").exists()
    assert list(tmp_path.rglob("*.db")) == []
