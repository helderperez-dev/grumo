"""Compatibility coverage for the interim Grumo CLI entrypoint.

The migration must not remove the existing Voodoo command before the new
distribution and installed applications are validated.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from typer.testing import CliRunner

from voodoo.cli import app


def test_grumo_and_voodoo_console_scripts_share_a_stable_entrypoint() -> None:
    project = Path(__file__).parents[3] / "pyproject.toml"
    with project.open("rb") as file:
        scripts = tomllib.load(file)["project"]["scripts"]
    assert scripts["grumo"] == "voodoo.cli:app"
    assert scripts["voodoo"] == scripts["grumo"]


def test_interim_grumo_cli_exposes_help_and_core_commands() -> None:
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("new", "dev", "start", "doctor", "fabric"):
        assert command in result.output
