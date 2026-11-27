"""Event bus capability with Grumo Store as the dependency-light default."""

from __future__ import annotations

from importlib import import_module
from typing import Any

from grumo.storage.events.interfaces import EventBusCapabilities, GrumoEventBus
from grumo.storage.events.local import LocalEventBus
from grumo.storage.events.store import GrumoStoreEventBus

__all__ = [
    "EventBusCapabilities",
    "GrumoEventBus",
    "GrumoStoreEventBus",
    "LocalEventBus",
    "PostgresEventStore",
    "SQLiteEventBus",
]

_LAZY_EXPORTS = {
    "PostgresEventStore": ("grumo.storage.events.postgres", "PostgresEventStore"),
    "SQLiteEventBus": ("grumo.storage.events.sqlite", "SQLiteEventBus"),
}


def __getattr__(name: str) -> Any:
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module 'grumo.storage.events' has no attribute {name!r}")
    module_name, symbol = target
    value = getattr(import_module(module_name), symbol)
    globals()[name] = value
    return value
