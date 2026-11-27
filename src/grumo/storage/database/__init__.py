"""Optional SQL database adapters.

The core interfaces are import-safe without SQL dependencies. SQLite and
PostgreSQL implementations are loaded only when their adapter symbols are
requested explicitly.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from grumo.storage.database.interfaces import (
    DatabaseCapabilities,
    GrumoDatabase,
    Migration,
)

__all__ = [
    "DatabaseCapabilities",
    "Migration",
    "GrumoDatabase",
    "FRAMEWORK_MIGRATIONS",
    "LEDGER_TABLE",
    "PostgresDatabase",
    "SQLiteDatabase",
    "register_framework_migration",
]

_LAZY_EXPORTS = {
    "PostgresDatabase": ("grumo.storage.database.postgres", "PostgresDatabase"),
    "SQLiteDatabase": ("grumo.storage.database.sqlite", "SQLiteDatabase"),
    "FRAMEWORK_MIGRATIONS": ("grumo.storage.database.sqlite", "FRAMEWORK_MIGRATIONS"),
    "LEDGER_TABLE": ("grumo.storage.database.sqlite", "LEDGER_TABLE"),
    "register_framework_migration": (
        "grumo.storage.database.sqlite",
        "register_framework_migration",
    ),
}


def __getattr__(name: str) -> Any:
    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(
            f"module 'grumo.storage.database' has no attribute {name!r}"
        )
    module_name, symbol = target
    value = getattr(import_module(module_name), symbol)
    globals()[name] = value
    return value
