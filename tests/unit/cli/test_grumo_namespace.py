"""Grumo public namespace compatibility before the distribution cutover."""

from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

from typer.testing import CliRunner

import grumo
import voodoo
from grumo.cli import app as grumo_cli
from voodoo.cli import app as voodoo_cli


def test_public_grumo_exports_are_identical_to_legacy_exports() -> None:
    assert grumo.__version__ == voodoo.__version__
    for name in grumo.__all__:
        assert getattr(grumo, name) is getattr(voodoo, name)


def test_grumo_import_can_be_loaded_independently() -> None:
    assert importlib.import_module("grumo").App is voodoo.App


def test_console_scripts_use_same_runtime_without_duplicated_state() -> None:
    project = Path(__file__).resolve().parents[3] / "pyproject.toml"
    with project.open("rb") as stream:
        metadata = tomllib.load(stream)
    assert metadata["project"]["scripts"]["grumo"] == "grumo.cli:app"
    assert metadata["project"]["scripts"]["voodoo"] == "voodoo.cli:app"
    assert grumo_cli is voodoo_cli
    result = CliRunner().invoke(grumo_cli, ["--help"])
    assert result.exit_code == 0
    for command in ("new", "dev", "start", "doctor", "fabric"):
        assert command in result.output
