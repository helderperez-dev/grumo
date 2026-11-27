"""Fresh-project smoke test for the official ``grumo create`` template."""

from __future__ import annotations

from pathlib import Path

from grumo.cli.new import _scaffold_offline


def test_generated_project_boots_and_creates_application_store(tmp_path: Path) -> None:
    project = tmp_path / "generated"
    _scaffold_offline(project, "generated")
    assert (project / "app" / "page.py").exists()
    assert (project / "app" / "about" / "page.py").exists()
    assert (project / "app" / "users" / "[id]" / "page.py").exists()
    assert "generated" in (project / "pyproject.toml").read_text()
    assert "generated" in (project / "grumo.toml").read_text()
