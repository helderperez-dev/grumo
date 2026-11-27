"""Release gates for the Store-only default installation."""

from __future__ import annotations

import subprocess
import sys


def test_import_grumo_does_not_require_aiosqlite() -> None:
    code = r"""
import importlib.abc
import sys

class BlockAioSQLite(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "aiosqlite" or fullname.startswith("aiosqlite."):
            raise ImportError("aiosqlite intentionally blocked by release gate")
        return None

sys.meta_path.insert(0, BlockAioSQLite())
import grumo
assert grumo.Model is not None
assert grumo.__version__
assert "aiosqlite" not in sys.modules
assert "grumo.storage.database.sqlite" not in sys.modules
assert "grumo.storage.events.sqlite" not in sys.modules
assert "grumo.storage.queue.sqlite" not in sys.modules
assert "grumo.storage.execution.sqlite" not in sys.modules
assert "grumo.storage.scheduler.sqlite" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_runtime_startup_does_not_require_aiosqlite(tmp_path) -> None:
    code = r"""
import importlib.abc
import sys

class BlockAioSQLite(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "aiosqlite" or fullname.startswith("aiosqlite."):
            raise ImportError("aiosqlite intentionally blocked by startup release gate")
        return None

sys.meta_path.insert(0, BlockAioSQLite())

from starlette.testclient import TestClient
from grumo.core import create_app

with TestClient(create_app()) as client:
    assert client is not None

assert "aiosqlite" not in sys.modules
assert "grumo.data.base" not in sys.modules
assert "grumo.storage.database.sqlite" not in sys.modules
assert "grumo.storage.scheduler.sqlite" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_public_model_module_has_no_sql_fallback_import() -> None:
    code = r"""
import sys
from grumo import Model

assert Model.__module__ == "grumo.data.store_facade"
assert "grumo.data.base" not in sys.modules
assert "grumo.data.model" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
