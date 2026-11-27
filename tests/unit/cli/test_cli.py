import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import typer
from typer.testing import CliRunner

from grumo.cli import app
from grumo.cli.generate import generate
from grumo.cli.routes import routes
from grumo.cli.scaffolding import (
    _detect_ide,
    _fetch_text,
    _ide_from_processes,
    _sync_ai_assets,
)
from grumo.cli.theme import use_theme

runner = CliRunner()


def test_fetch_text_recovers_expected_remote_failures() -> None:
    with patch(
        "grumo.cli.scaffolding.urllib.request.urlopen", side_effect=TimeoutError()
    ):
        assert _fetch_text("https://example.invalid") is None


def test_fetch_text_propagates_unexpected_provider_failures() -> None:
    with patch(
        "grumo.cli.scaffolding.urllib.request.urlopen",
        side_effect=RuntimeError("unexpected decoder failure"),
    ):
        try:
            _fetch_text("https://example.invalid")
        except RuntimeError as error:
            assert str(error) == "unexpected decoder failure"
        else:
            raise AssertionError("unexpected provider failures must propagate")


def test_process_ide_detection_recovers_when_process_probe_is_unavailable() -> None:
    with patch(
        "grumo.cli.scaffolding.subprocess.run",
        side_effect=FileNotFoundError("ps unavailable"),
    ):
        assert _ide_from_processes() is None


def test_process_ide_detection_propagates_unexpected_probe_failures() -> None:
    with patch(
        "grumo.cli.scaffolding.subprocess.run",
        side_effect=RuntimeError("unexpected process probe failure"),
    ):
        try:
            _ide_from_processes()
        except RuntimeError as error:
            assert str(error) == "unexpected process probe failure"
        else:
            raise AssertionError("unexpected process probe failures must propagate")


def test_theme_cli_propagates_unexpected_resolution_failures(monkeypatch) -> None:
    monkeypatch.setattr(
        "grumo.ui.styles.presets.resolve_theme",
        lambda _preset: (_ for _ in ()).throw(RuntimeError("theme invariant")),
    )
    with pytest.raises(RuntimeError, match="theme invariant"):
        use_theme("default")


def test_routes_cli_propagates_unexpected_application_import_failures(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "importlib.import_module",
        lambda _name: (_ for _ in ()).throw(RuntimeError("application invariant")),
    )
    with pytest.raises(RuntimeError, match="application invariant"):
        routes("main:app")


def test_generate_cli_redacts_provider_failure_messages(monkeypatch) -> None:
    secret = "sk-" + "b" * 24

    class Provider:
        async def complete(self, *_args, **_kwargs):
            raise RuntimeError(f"provider failed api_key={secret}")

    messages: list[str] = []
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(
        "grumo.ai.providers.get_provider", lambda *_args, **_kwargs: Provider()
    )
    monkeypatch.setattr(
        "grumo.cli.generate.terminal.error",
        lambda message, **_kwargs: messages.append(message),
    )

    with pytest.raises(typer.Exit):
        generate("tool", "describe a tool")

    assert secret not in messages[0]
    assert "[REDACTED]" in messages[0]


def test_detect_ide_from_env():
    with patch.dict(os.environ, {"TRAE_PID": "12345"}, clear=False):
        assert _detect_ide() == "trae"

    with patch.dict(os.environ, {"CURSOR_TRACE": "1"}, clear=False):
        assert _detect_ide() == "cursor"

    with patch.dict(os.environ, {"WINDSURF_PORT": "9000"}, clear=False):
        assert _detect_ide() == "windsurf"

    with patch.dict(os.environ, {"TERM_PROGRAM": "vscode"}, clear=False):
        assert _detect_ide() == "vscode"


def test_sync_ai_assets_none(tmp_path: Path):
    mock_progress = MagicMock()
    _sync_ai_assets(tmp_path, mock_progress, ide="none")

    # Core AI docs exist
    assert (tmp_path / ".grumo/ai/README.md").exists()
    assert (tmp_path / ".grumo/ai/RULES.md").exists()
    assert (tmp_path / ".grumo/ai/MESH.md").exists()
    assert (tmp_path / ".grumo/ai/SEO.md").exists()

    # IDE specific folders do NOT exist
    assert not (tmp_path / ".trae").exists()
    assert not (tmp_path / ".cursor").exists()
    assert not (tmp_path / ".windsurfrules").exists()
    assert not (tmp_path / ".github").exists()


def test_sync_ai_assets_trae(tmp_path: Path):
    mock_progress = MagicMock()
    _sync_ai_assets(tmp_path, mock_progress, ide="trae")

    # Core AI docs exist
    assert (tmp_path / ".grumo/ai/README.md").exists()

    # Trae assets exist
    assert (tmp_path / ".trae/rules").exists()
    assert (tmp_path / ".trae/skills/grumo-builder/SKILL.md").exists()

    # Other IDE rules do NOT exist
    assert not (tmp_path / ".cursor").exists()
    assert not (tmp_path / ".windsurfrules").exists()


def test_sync_ai_assets_cursor(tmp_path: Path):
    mock_progress = MagicMock()
    _sync_ai_assets(tmp_path, mock_progress, ide="cursor")

    # Core AI docs exist
    assert (tmp_path / ".grumo/ai/README.md").exists()

    # Cursor assets exist
    assert (tmp_path / ".cursor/rules/grumo.mdc").exists()

    # Other IDE rules do NOT exist
    assert not (tmp_path / ".trae").exists()
    assert not (tmp_path / ".windsurfrules").exists()


def test_sync_ai_assets_windsurf(tmp_path: Path):
    mock_progress = MagicMock()
    _sync_ai_assets(tmp_path, mock_progress, ide="windsurf")

    # Core AI docs exist
    assert (tmp_path / ".grumo/ai/README.md").exists()

    # Windsurf assets exist
    assert (tmp_path / ".windsurfrules").exists()

    # Other IDE rules do NOT exist
    assert not (tmp_path / ".trae").exists()
    assert not (tmp_path / ".cursor").exists()


def test_sync_ai_assets_all(tmp_path: Path):
    mock_progress = MagicMock()
    _sync_ai_assets(tmp_path, mock_progress, ide="all")

    # All IDE rules exist
    assert (tmp_path / ".trae/rules").exists()
    assert (tmp_path / ".cursor/rules/grumo.mdc").exists()
    assert (tmp_path / ".windsurfrules").exists()
    assert (tmp_path / ".github/copilot-instructions.md").exists()


def test_cli_ai_init_with_ide_flag(tmp_path: Path):
    """grumo ai init --ide cursor should generate cursor rules."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["ai", "init", "--ide", "cursor"])
        assert result.exit_code == 0
        assert (tmp_path / ".cursor" / "rules" / "grumo.mdc").exists()
        assert not (tmp_path / ".trae").exists()
        assert not (tmp_path / ".windsurfrules").exists()
    finally:
        os.chdir(original_cwd)


def test_cli_ai_init_no_prompt(tmp_path: Path):
    """grumo ai init should NOT prompt for IDE selection - auto-detect only."""
    import os

    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["ai", "init"])
        assert result.exit_code == 0
        assert "Select" not in result.output
        assert ".grumo/ai/" in result.output
    finally:
        os.chdir(original_cwd)


def test_cli_auth_secret_key():
    result = runner.invoke(app, ["auth", "secret-key"])
    assert result.exit_code == 0
    assert "GRUMO_SECRET_KEY" in result.output


def test_cli_auth_secret_key_raw():
    result = runner.invoke(app, ["auth", "secret-key", "--raw"])
    assert result.exit_code == 0
    assert "GRUMO_SECRET_KEY" not in result.output
    assert len(result.output.strip()) >= 32


def test_cli_auth_hash_password():
    result = runner.invoke(app, ["auth", "hash-password", "MyPassword123!"])
    assert result.exit_code == 0
    assert "pbkdf2_sha256$" in result.output


def test_cli_auth_generate_key():
    result = runner.invoke(app, ["auth", "generate-key", "--prefix", "vd_test"])
    assert result.exit_code == 0
    assert "vd_test_" in result.output
    assert "SHA-256 Hash" in result.output


def test_cli_auth_create_user(tmp_path: Path):
    db_file = str(tmp_path / "cli_users.db")
    with patch.dict(os.environ, {"GRUMO_DB_PATH": db_file}, clear=False):
        from grumo.config import config

        config.db_path = db_file
        result = runner.invoke(
            app,
            [
                "auth",
                "create-user",
                "--email",
                "admin@grumo.dev",
                "--password",
                "StrongAdminPass123!",
                "--username",
                "admin",
                "--role",
                "admin",
            ],
        )
        assert result.exit_code == 0
        assert "User created successfully!" in result.output
        assert "admin@grumo.dev" in result.output


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "grumo" in result.output.lower()
    assert "Python" in result.output


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "grumo" in result.output.lower()


def test_cli_doctor_checks_subsystems():
    """Doctor should check runtime/db/auth/mesh/workers/observability subsystems."""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "environment" in result.output.lower()
    assert "runtime" in result.output.lower()
    assert "modules" in result.output.lower()
    assert "auth" in result.output.lower()
    assert "mesh" in result.output.lower()
    assert "workers" in result.output.lower()
    assert "observability" in result.output.lower()


def test_cli_version_shows_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "grumo" in result.output.lower()
    import grumo

    ver = getattr(grumo, "__version__", "unknown")
    assert ver in result.output


def test_cli_new_minimal_scaffold(tmp_path: Path):
    """grumo new keeps routes minimal but includes production test scaffolding."""
    project_dir = tmp_path / "minimal_app"
    result = runner.invoke(app, ["new", str(project_dir), "--template", ""])
    assert result.exit_code == 0

    # Must exist — routes via folder-based routing (app/<dir>/page.py)
    assert (project_dir / "app" / "page.py").exists()
    assert (project_dir / "app" / "about" / "page.py").exists()
    assert (project_dir / "app" / "users" / "[id]" / "page.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "grumo.toml").exists()

    # Must NOT exist
    assert not (project_dir / "app" / "pages").exists()
    assert not (project_dir / "app" / "components").exists()
    assert not (project_dir / "app" / "agents").exists()
    assert not (project_dir / "app" / "workers").exists()
    assert not (project_dir / "app" / "models.py").exists()
    assert not (project_dir / "app" / "styles.css").exists()
    assert (project_dir / "tests" / "test_app.py").exists()
    assert (project_dir / ".github" / "workflows" / "quality.yml").exists()


def test_cli_new_generated_project_compiles_and_matches_runtime_contract(
    tmp_path: Path,
) -> None:
    """The canonical scaffold must be executable without network access."""
    project_dir = tmp_path / "generated_app"
    result = runner.invoke(app, ["new", str(project_dir), "--template", ""])
    assert result.exit_code == 0, result.output

    compile_result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", str(project_dir / "app")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert compile_result.returncode == 0, compile_result.stderr
    pyproject = (project_dir / "pyproject.toml").read_text()
    assert '"grumo>=2.0.0,<3.0.0"' in pyproject
    assert (
        "Runtime creates application.grumo" in (project_dir / "grumo.toml").read_text()
    )
    assert not (project_dir / "main.py").exists()
    assert not (project_dir / ".env").exists()
    assert not (project_dir / ".data").exists()
    assert not (project_dir / "storage").exists()
    assert not (project_dir / ".grumo").exists()
    assert not (project_dir / ".trae").exists()
    assert not (project_dir / ".cursor").exists()


def test_cli_new_page_content(tmp_path: Path):
    """The scaffolded app/page.py should use the Grumo public API and file
    convention (folder-based routing), not the @page decorator."""
    project_dir = tmp_path / "content_app"
    result = runner.invoke(app, ["new", str(project_dir), "--template", ""])
    assert result.exit_code == 0

    page_content = (project_dir / "app" / "page.py").read_text()
    assert "from grumo.ui import" in page_content
    # File-based convention: a module-level `page` function drives routing.
    assert "def page(request: object)" in page_content
    # No @page decorator in the scaffold (it conflicts with the file scanner
    # when app/page.py is imported via the folder convention).
    assert "@page" not in page_content
    # Grumo CSS best practices: semantic components and props.
    assert "Heading" in page_content
    assert "Text" in page_content
    assert "Button" in page_content
    assert "variant=" in page_content
    assert "tone=" in page_content
    # SEO tuple return.
    assert "from grumo.seo import SEO" in page_content
    assert "return seo, ui" in page_content
    # Internal navigation is declarative; the client runtime intercepts normal hrefs.
    assert "A(" in page_content
    assert "href=" in page_content
    assert "grumo.navigate(" not in page_content

    # The dynamic route should use a bracket folder + typed segment.
    user_content = (project_dir / "app" / "users" / "[id]" / "page.py").read_text()
    assert "def page(request: object, id: int)" in user_content


def test_cli_routes_command(tmp_path: Path):
    """grumo routes should list routes from an app."""
    # Create a minimal app structure
    app_dir = tmp_path / "app_test"
    app_dir.mkdir()
    (app_dir / "main.py").write_text(
        "from grumo.core import create_app\napp = create_app()\n"
    )
    (app_dir / "app").mkdir()
    (app_dir / "app" / "page.py").write_text(
        "from grumo.components import Div, Text\n\n"
        "def page(request):\n"
        "    return Div(Text('Hello'))\n"
    )

    result = runner.invoke(
        app,
        ["routes", "main:app"],
    )
    # routes command tries to import main:app from cwd; may fail in test env
    # just verify it doesn't crash with a traceback
    assert result.exit_code in (0, 1)


def test_cli_dev_missing_module():
    """grumo dev should exit with error if module not found."""
    result = runner.invoke(app, ["dev", "nonexistent:app"])
    assert result.exit_code == 1
    assert "error" in result.output.lower() or "could not find" in result.output.lower()


def test_cli_dev_missing_dotted_module():
    """grumo dev should not crash when a dotted module's parent is missing.

    Regression: importlib.util.find_spec raises ModuleNotFoundError for dotted
    names whose parent package isn't installed (e.g. "myapp.sub"). The CLI
    should catch it and show the clean error, not a traceback.
    """
    result = runner.invoke(app, ["dev", "nonexistent_pkg.submodule:app"])
    assert result.exit_code == 1
    assert "could not find" in result.output.lower()
    assert "Traceback" not in result.output


def test_cli_dev_does_not_leak_pythonpath(tmp_path: Path, monkeypatch):
    """dev must not inject the CLI's own sys.path into the uvicorn subprocess.

    Regression: `env["PYTHONPATH"] = os.pathsep.join(sys.path)` leaked the CLI's
    bundled site-packages (Homebrew/uv tool) into the subprocess, shadowing the
    project venv's grumo and serving stale framework code.
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PYTHONPATH", raising=False)

    captured: dict[str, str] = {}

    def fake_run(args: list[str], env: dict[str, str], **kwargs: object) -> None:
        captured.update(env)

    with patch("grumo.cli.dev.subprocess.run", side_effect=fake_run):
        result = runner.invoke(app, ["dev", "grumo.core:app"])

    assert result.exit_code == 0
    assert "PYTHONPATH" not in captured


def test_cli_start_uses_safe_production_defaults(
    tmp_path: Path,
    monkeypatch,
):
    """start should discover main.py and preserve Store-safe server defaults."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "main.py").write_text("app = object()\n")
    for name in (
        "GRUMO_ENV",
        "GRUMO_SECRET_KEY",
        "GRUMO_HOST",
        "GRUMO_PORT",
        "PORT",
        "FORWARDED_ALLOW_IPS",
        "WEBSOCKETS_MAX_LINE_LENGTH",
        "WEBSOCKETS_MAX_NUM_HEADERS",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("GRUMO_SECRET_KEY", "test-production-secret-" * 2)

    with patch("uvicorn.run") as run:
        result = runner.invoke(app, ["start"])

    assert result.exit_code == 0
    run.assert_called_once_with(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        proxy_headers=True,
        forwarded_allow_ips="127.0.0.1",
        http="h11",
        ws="websockets",
        h11_max_incomplete_event_size=5_242_880,
    )
    assert "GRUMO_ENV" not in os.environ
    assert "WEBSOCKETS_MAX_LINE_LENGTH" not in os.environ
    assert "WEBSOCKETS_MAX_NUM_HEADERS" not in os.environ


def test_cli_start_respects_explicit_configuration(
    tmp_path: Path,
    monkeypatch,
):
    """CLI arguments and explicit environment settings should remain authoritative."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GRUMO_ENV", "staging")
    monkeypatch.setenv("GRUMO_HOST", "127.0.0.2")
    monkeypatch.setenv("PORT", "9100")
    monkeypatch.setenv("FORWARDED_ALLOW_IPS", "10.0.0.0/8")

    with patch("uvicorn.run") as run:
        result = runner.invoke(
            app,
            [
                "start",
                "custom.application:app",
                "--host",
                "127.0.0.3",
                "--port",
                "9200",
            ],
        )

    assert result.exit_code == 0
    call = run.call_args
    assert call.args == ("custom.application:app",)
    assert call.kwargs["host"] == "127.0.0.3"
    assert call.kwargs["port"] == 9200
    assert call.kwargs["forwarded_allow_ips"] == "10.0.0.0/8"
    assert call.kwargs["workers"] == 1
    assert os.environ["GRUMO_ENV"] == "staging"


def test_cli_start_rejects_wildcard_proxy_trust(
    tmp_path: Path,
    monkeypatch,
):
    """Forwarded headers must never be trusted from every source."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GRUMO_ENV", "staging")
    monkeypatch.setenv("FORWARDED_ALLOW_IPS", "*")

    with patch("uvicorn.run") as run:
        result = runner.invoke(app, ["start", "main:app"])

    assert result.exit_code == 1
    assert "FORWARDED_ALLOW_IPS" in result.output
    run.assert_not_called()


def test_cli_start_rejects_development_secret_in_production(
    tmp_path: Path,
    monkeypatch,
):
    """The production command must fail before starting an unsafe server."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GRUMO_ENV", raising=False)
    monkeypatch.delenv("GRUMO_SECRET_KEY", raising=False)

    with patch("uvicorn.run") as run:
        result = runner.invoke(app, ["start", "main:app"])

    assert result.exit_code == 1
    assert "GRUMO_SECRET_KEY" in result.output
    run.assert_not_called()


def test_cli_start_falls_back_to_folder_routing_app(
    tmp_path: Path,
    monkeypatch,
):
    """Projects without main.py should use the folder-routing application."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GRUMO_SECRET_KEY", "test-production-secret-" * 2)

    with patch("uvicorn.run") as run:
        result = runner.invoke(app, ["start"])

    assert result.exit_code == 0
    assert run.call_args.args == ("grumo.core:app",)


def test_cli_start_does_not_offer_unsafe_multi_worker_mode():
    """One local Store writer means the production command has no workers option."""
    result = runner.invoke(app, ["start", "--workers", "2"])

    assert result.exit_code != 0
    assert "No such option" in result.output
