"""Release gates for the stable ``grumo create`` scaffold."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from grumo.cli import app

__all__: list[str] = []

runner = CliRunner()


@pytest.fixture()
def tmp_cwd(tmp_path: Path):
    old = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old)


class TestCreateScaffold:
    def test_creates_minimal_project(self, tmp_cwd: Path) -> None:
        result = runner.invoke(app, ["create", "myapp"])
        assert result.exit_code == 0
        project = tmp_cwd / "myapp"
        assert (project / "app" / "page.py").exists()
        assert (project / "app" / "about" / "page.py").exists()
        assert (project / "app" / "users" / "[id]" / "page.py").exists()
        assert (project / "grumo.toml").exists()
        assert (project / "pyproject.toml").exists()
        assert (project / "README.md").exists()
        assert "deprecated" in result.output.lower()

    def test_template_tracks_latest_grumo_release(self, tmp_cwd: Path) -> None:
        runner.invoke(app, ["create", "myapp"])
        content = (tmp_cwd / "myapp" / "pyproject.toml").read_text()
        assert '"grumo>=2.0.0,<3.0.0"' in content

    def test_store_first_runtime_guidance(self, tmp_cwd: Path) -> None:
        runner.invoke(app, ["create", "myapp"])
        content = (tmp_cwd / "myapp" / "grumo.toml").read_text()
        assert ".grumo/application.grumo" in content
        assert "Runtime creates application.grumo" in content

    def test_rejects_existing_directory(self, tmp_cwd: Path) -> None:
        (tmp_cwd / "existing").mkdir()
        result = runner.invoke(app, ["create", "existing"])
        assert result.exit_code == 1


class TestRuntimeBanner:
    def test_banner_imports(self) -> None:
        from grumo.cli.dev import _print_runtime_banner

        assert callable(_print_runtime_banner)
