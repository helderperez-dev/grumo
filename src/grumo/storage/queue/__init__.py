"""Grumo queue capability with Grumo Store as the default backend."""

from __future__ import annotations

from importlib import import_module
from typing import Any

from grumo.storage.queue.interfaces import (
    ACTIVE_STATUSES,
    GrumoQueue,
    QueueCapabilities,
    QueueStats,
    TaskRecord,
    TaskStatus,
)
from grumo.storage.queue.memory import MemoryQueue
from grumo.storage.queue.store import GrumoStoreQueue

__all__ = [
    "ACTIVE_STATUSES",
    "MemoryQueue",
    "PostgresQueue",
    "QueueCapabilities",
    "QueueStats",
    "RedisQueue",
    "SQLiteQueue",
    "TASKS_MIGRATION",
    "TASKS_TABLE",
    "TaskRecord",
    "TaskStatus",
    "GrumoQueue",
    "GrumoStoreQueue",
]

_LAZY_EXPORTS = {
    "PostgresQueue": ("grumo.storage.queue.postgres", "PostgresQueue"),
    "RedisQueue": ("grumo.storage.queue.redis", "RedisQueue"),
    "SQLiteQueue": ("grumo.storage.queue.sqlite", "SQLiteQueue"),
    "TASKS_MIGRATION": ("grumo.storage.queue.sqlite", "TASKS_MIGRATION"),
    "TASKS_TABLE": ("grumo.storage.queue.sqlite", "TASKS_TABLE"),
}


def __getattr__(name: str) -> Any:
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module 'grumo.storage.queue' has no attribute {name!r}")
    module_name, symbol = target
    value = getattr(import_module(module_name), symbol)
    globals()[name] = value
    return value
