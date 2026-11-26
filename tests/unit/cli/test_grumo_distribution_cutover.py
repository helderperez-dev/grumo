"""Release-candidate metadata contracts for the Grumo package cutover."""

from __future__ import annotations

import tomllib
from pathlib import Path

import grumo
import voodoo


def test_grumo_distribution_metadata_matches_release_identity() -> None:
    root = Path(__file__).resolve().parents[3]
    with (root / "pyproject.toml").open("rb") as stream:
        project_file = tomllib.load(stream)

    project = project_file["project"]
    assert project["name"] == "grumo"
    assert "grumo-store>=0.3.2,<0.4" in project["dependencies"]
    assert not any(
        dependency.startswith("voodoo-store")
        for dependency in project["dependencies"]
    )
    assert project["scripts"]["grumo"] == "grumo.cli:app"
    assert project["scripts"]["voodoo"] == "voodoo.cli:app"
    assert (
        project_file["tool"]["setuptools"]["dynamic"]["version"]["attr"]
        == "grumo.__version__"
    )
    assert set(project_file["tool"]["setuptools"]["packages"]["find"]["include"]) == {
        "grumo*",
        "voodoo*",
    }


def test_legacy_python_imports_keep_exact_runtime_identity() -> None:
    assert grumo.App is voodoo.App
    assert grumo.Agent is voodoo.Agent
    assert grumo.__version__ == voodoo.__version__
