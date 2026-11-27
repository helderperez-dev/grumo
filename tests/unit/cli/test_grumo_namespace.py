"""Canonical Grumo package and CLI identity."""
import importlib.util
import tomllib
from pathlib import Path
from typer.testing import CliRunner

import grumo
from grumo.cli import app


def test_canonical_package_exports() -> None:
    assert grumo.App.__module__.startswith("grumo.")
    assert grumo.Agent.__module__.startswith("grumo.")
    assert importlib.util.find_spec("voodoo") is None
    assert importlib.util.find_spec("voodoo_store") is None

def test_canonical_console_script() -> None:
    with (Path(__file__).resolve().parents[3] / "pyproject.toml").open("rb") as stream:
        scripts = tomllib.load(stream)["project"]["scripts"]
    assert scripts == {"grumo": "grumo.cli:app"}
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("new", "dev", "start", "doctor", "fabric"):
        assert command in result.output
