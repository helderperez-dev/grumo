from __future__ import annotations

from types import SimpleNamespace

import pytest

from grumo.observability.api import get_metrics
from grumo.observability.store import telemetry_store


@pytest.mark.asyncio
async def test_native_metrics_summary(monkeypatch):
    monkeypatch.setitem(telemetry_store.metrics, "requests_total", 7)
    monkeypatch.setitem(telemetry_store.metrics, "errors_total", 2)
    summary = await get_metrics()
    assert summary["requests_total"] == 7
    assert summary["errors_total"] == 2


@pytest.mark.asyncio
async def test_metrics_projects_sanitized_active_store_health(monkeypatch):
    fake_health = SimpleNamespace(
        provider="grumo",
        opened=True,
        verified=True,
        details={
            "native_health": {
                "store_id": b"must-not-be-exported",
                "queue_ready": 3,
                "metrics": {"commits": 7},
            }
        },
    )
    fake_runtime = SimpleNamespace(health=lambda: fake_health)
    monkeypatch.setattr(
        "grumo.runtime.store.get_active_runtime_store", lambda: fake_runtime
    )

    summary = await get_metrics()
    assert summary["store_health"]["details"]["native_health"]["queue_ready"] == 3
    assert "store_id" not in summary["store_health"]["details"]["native_health"]

    assert summary["store_health"]["details"]["native_health"]["metrics"]["commits"] == 7
    assert "must-not-be-exported" not in repr(summary["store_health"])


@pytest.mark.asyncio
async def test_metrics_json_drops_paths_and_non_numeric_health_payloads(monkeypatch):
    fake_health = SimpleNamespace(
        provider="grumo",
        opened=True,
        verified=True,
        details={
            "path": "/private/store.vstore",
            "secret_token": "password=do-not-export",
            "within_limit": True,
            "queue_ready": 4,
            "nested": {"latency_ms": 2.5, "message": "not a metric"},
        },
    )
    monkeypatch.setattr(
        "grumo.runtime.store.get_active_runtime_store",
        lambda: SimpleNamespace(health=lambda: fake_health),
    )

    summary = await get_metrics()
    details = summary["store_health"]["details"]
    assert details == {
        "within_limit": True,
        "queue_ready": 4,
        "nested": {"latency_ms": 2.5},
    }
