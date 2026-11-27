"""Readiness must not load an optional SQL backend for Store-only apps."""

import subprocess
import sys


def test_migration_health_without_sql_backend() -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.modules['aiosqlite'] = None; "
            "from grumo.data.base import migration_health; "
            "assert migration_health()['status'] == 'unknown'",
        ],
        check=True,
    )
