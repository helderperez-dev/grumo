"""Canonical Grumo 3.0 import-law tests."""

from __future__ import annotations


def test_canonical_application_surface_imports() -> None:
    from grumo import Agent, App, Model, page, state, task, tool

    assert all((Agent, App, Model, page, state, task, tool))


def test_canonical_subsystem_namespace_imports() -> None:
    from grumo.edge import DeviceGateway, WorldAwareDeviceGateway
    from grumo.protocol import RemoteExecutionRequest, WorldSnapshot
    from grumo.runtime import ExecutionEngine, Goal, GoalRuntime, Planner
    from grumo.ui import Button, Card, DataTable
    from grumo.world import Entity, Observation, WorldModel

    assert all(
        (
            DeviceGateway,
            WorldAwareDeviceGateway,
            RemoteExecutionRequest,
            WorldSnapshot,
            ExecutionEngine,
            Goal,
            GoalRuntime,
            Planner,
            Button,
            Card,
            DataTable,
            Entity,
            Observation,
            WorldModel,
        )
    )


def test_package_root_is_only_the_application_happy_path() -> None:
    import grumo

    assert set(grumo.__all__) == {
        "Agent",
        "App",
        "Model",
        "page",
        "state",
        "task",
        "tool",
    }
