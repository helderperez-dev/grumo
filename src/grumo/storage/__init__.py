"""Grumo storage namespace.

The default package import is dependency-light. Store-native runtime paths do
not import SQLite, PostgreSQL, Redis, or S3 adapters. Compatibility adapters are
resolved lazily only when their public symbols are requested explicitly.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from grumo.storage.manager import StorageManager, storage

__all__ = [
    "StorageManager",
    "storage",
    "EventBusCapabilities",
    "GrumoEventBus",
    "GrumoStoreEventBus",
    "LocalEventBus",
    "SQLiteEventBus",
    "PostgresEventStore",
    "SQLiteExecutionStore",
    "PostgresExecutionStore",
    "GrumoStoreExecutionStore",
    "GrumoQueue",
    "GrumoStoreQueue",
    "MemoryQueue",
    "SQLiteQueue",
    "PostgresQueue",
    "RedisQueue",
    "CacheCapabilities",
    "GrumoCache",
    "MemoryCache",
    "RedisCache",
]

_LAZY_EXPORTS = {
    "EventBusCapabilities": (
        "grumo.storage.events.interfaces",
        "EventBusCapabilities",
    ),
    "GrumoEventBus": ("grumo.storage.events.interfaces", "GrumoEventBus"),
    "GrumoStoreEventBus": ("grumo.storage.events.store", "GrumoStoreEventBus"),
    "LocalEventBus": ("grumo.storage.events.local", "LocalEventBus"),
    "SQLiteEventBus": ("grumo.storage.events.sqlite", "SQLiteEventBus"),
    "PostgresEventStore": ("grumo.storage.events.postgres", "PostgresEventStore"),
    "SQLiteExecutionStore": (
        "grumo.storage.execution.sqlite",
        "SQLiteExecutionStore",
    ),
    "PostgresExecutionStore": (
        "grumo.storage.execution.postgres",
        "PostgresExecutionStore",
    ),
    "GrumoStoreExecutionStore": (
        "grumo.storage.execution.store",
        "GrumoStoreExecutionStore",
    ),
    "GrumoQueue": ("grumo.storage.queue.interfaces", "GrumoQueue"),
    "GrumoStoreQueue": ("grumo.storage.queue.store", "GrumoStoreQueue"),
    "MemoryQueue": ("grumo.storage.queue.memory", "MemoryQueue"),
    "SQLiteQueue": ("grumo.storage.queue.sqlite", "SQLiteQueue"),
    "PostgresQueue": ("grumo.storage.queue.postgres", "PostgresQueue"),
    "RedisQueue": ("grumo.storage.queue.redis", "RedisQueue"),
    "CacheCapabilities": ("grumo.storage.cache.interfaces", "CacheCapabilities"),
    "GrumoCache": ("grumo.storage.cache.interfaces", "GrumoCache"),
    "MemoryCache": ("grumo.storage.cache.memory", "MemoryCache"),
    "RedisCache": ("grumo.storage.cache.redis", "RedisCache"),
}


def __getattr__(name: str) -> Any:
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module 'grumo.storage' has no attribute {name!r}")
    module_name, symbol = target
    value = getattr(import_module(module_name), symbol)
    globals()[name] = value
    return value
