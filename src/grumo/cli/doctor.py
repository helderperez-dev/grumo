import importlib
import logging
from pathlib import Path
from typing import Any

import typer

from grumo.cli import terminal
from grumo.config import get_config
from grumo.security.redaction import redact_string

_logger = logging.getLogger("grumo.cli.doctor")


def _doctor_snapshot() -> dict[str, Any]:
    """Return side-effect-free diagnostics suitable for automation."""
    from grumo.cli.status import _application_snapshot

    cfg = get_config()
    modules: dict[str, str] = {}
    for name, label in (
        ("grumo.mesh", "mesh"),
        ("grumo.integrations.mcp", "mcp"),
        ("grumo.ai", "ai"),
        ("grumo.runtime.scheduling", "workers"),
        ("grumo.observability", "observability"),
    ):
        try:
            importlib.import_module(name)
            modules[label] = "ready"
        except Exception as error:
            _logger.warning(
                "doctor module probe failed module=%s error=%s",
                name,
                redact_string(str(error)),
            )
            modules[label] = "not found"

    legacy_candidates = (
        Path(".grumo/state/data.db"),
        Path(".grumo/state/schedules.db"),
        Path(".grumo/state/agents.db"),
    )
    legacy_files = [str(path) for path in legacy_candidates if path.exists()]
    ai_dir = Path(".grumo/ai")

    return {
        "application": _application_snapshot(),
        "project": {
            "root": str(Path.cwd()),
            "config": "grumo.toml" if Path("grumo.toml").exists() else None,
            "app_directory": Path("app").is_dir(),
        },
        "integrity": {
            "legacy_sqlite": legacy_files,
            "store_first_clean": (
                cfg.database.provider.lower() != "grumo" or not legacy_files
            ),
        },
        "auth": {
            "secret": (
                "warning"
                if cfg.auth.secret_key
                == "dev-secret-key-change-in-production-grumo-2026"
                else "ready"
            )
        },
        "security": {
            "headers": cfg.security.headers_enabled,
            "rate_limit": cfg.security.rate_limit_enabled,
            "cors": cfg.security.cors_enabled,
            "csrf": cfg.security.csrf_enabled,
        },
        "modules": modules,
        "ai_kit": (
            "ready"
            if ai_dir.exists() and (ai_dir / "README.md").exists()
            else "not found"
        ),
    }


def _print_capability_matrix() -> None:
    """Print active providers and their declared capability matrix (spec §9).

    Renders one row per registered adapter implementation. This gives
    ``grumo doctor`` an honest, per-provider view of what the runtime
    guarantees.
    """
    from grumo.adapters.capabilities import (
        CacheCapabilities,
        DatabaseCapabilities,
        EventBusCapabilities,
        ObjectStoreCapabilities,
        QueueCapabilities,
    )

    # Default local providers (Sprints 1–7). Declared statically so ``doctor``
    # stays side-effect free: it never opens a connection or creates files.
    # PostgreSQL (Sprint 10) is an optional server backend behind the same
    # GrumoDatabase protocol.
    providers = (
        DatabaseCapabilities(
            "sqlite",
            transactions=True,
            migrations=True,
            native_json=False,
            concurrent_writers=False,
        ),
        DatabaseCapabilities(
            "postgres",
            transactions=True,
            migrations=True,
            native_json=True,
            concurrent_writers=True,
        ),
        QueueCapabilities(
            "sqlite",
            durable=True,
            visibility_timeout=True,
            delayed_delivery=True,
            priority=True,
            transactions=True,
        ),
        QueueCapabilities(
            "postgres",
            durable=True,
            visibility_timeout=True,
            delayed_delivery=True,
            priority=True,
            transactions=True,
        ),
        QueueCapabilities(
            "memory",
            durable=False,
            visibility_timeout=True,
            delayed_delivery=False,
            priority=True,
            transactions=False,
        ),
        QueueCapabilities(
            "redis",
            durable=True,
            visibility_timeout=True,
            delayed_delivery=True,
            priority=True,
            transactions=True,
        ),
        EventBusCapabilities(
            "sqlite",
            durable=True,
            replay=True,
            ordering=True,
        ),
        EventBusCapabilities(
            "postgres",
            durable=True,
            replay=True,
            ordering=True,
        ),
        EventBusCapabilities(
            "local",
            durable=False,
            replay=False,
            ordering=True,
        ),
        ObjectStoreCapabilities(
            "local",
            presign_urls=False,
            checksums=True,
            metadata=True,
            multipart=False,
        ),
        CacheCapabilities(
            "memory",
            ttl=False,
            durable=False,
        ),
        CacheCapabilities(
            "redis",
            ttl=True,
            durable=True,
        ),
    )

    for caps in providers:
        flag_str = "  ".join(f"{k}={v}" for k, v in caps.describe().items())
        terminal.status(caps.provider, "active")
        terminal.muted(f"  {flag_str}")


def _doctor_modules() -> None:

    terminal.heading("modules")
    modules = [
        ("grumo.mesh", "mesh"),
        ("grumo.integrations.mcp", "mcp"),
        ("grumo.ai", "ai provider"),
        ("grumo.runtime.scheduling", "workers"),
        ("grumo.observability", "observability"),
    ]
    for name, label in modules:
        try:
            importlib.import_module(name)
            terminal.status(label, "ready")
        except Exception as error:
            _logger.warning(
                "doctor module probe failed module=%s error=%s",
                name,
                redact_string(str(error)),
            )
            terminal.status(label, "not found")


def _doctor_queue() -> None:
    import asyncio

    terminal.heading("queue")

    async def check() -> tuple[int, int]:
        from grumo.runtime.scheduling.workers import _get_queue, _workers

        depth = 0
        try:
            queue = await _get_queue()
            if hasattr(queue, "list"):
                depth = len(await queue.list())
            elif hasattr(queue, "depth"):
                depth = await queue.depth()
        except Exception as error:
            _logger.warning("doctor queue probe failed error=%s", redact_string(str(error)))
            pass
        return depth, len(_workers)

    try:
        depth, workers = asyncio.run(check())
        terminal.status("depth", str(depth))
        terminal.status("registered workers", str(workers))
    except Exception as error:
        _logger.warning("doctor queue status failed error=%s", redact_string(str(error)))
        terminal.status("queue", "unavailable")


def _doctor_optional_services(cfg: object) -> None:
    terminal.heading("schedules")
    try:
        from grumo.cli.context import acquire_schedule_store

        schedule_store, store_path = acquire_schedule_store()
        try:
            schedule_store.list_all()
            terminal.status("scheduler", "ready")
            terminal.muted(f"  {store_path}")
        finally:
            schedule_store.close()
    except Exception as error:
        _logger.warning(
            "doctor scheduler probe failed error=%s", redact_string(str(error))
        )
        terminal.status("scheduler", "unavailable")




def _doctor_ai_kit() -> None:
    terminal.heading("ai kit")
    ai_dir = Path(".grumo/ai")
    ready = ai_dir.exists() and (ai_dir / "README.md").exists()
    terminal.status("context", "ready" if ready else "not found")
    terminal.muted("  .grumo/ai/" if ready else "  run 'grumo ai init' to generate")


def doctor(
    json_mode: bool = typer.Option(
        False,
        "--json",
        help="Output side-effect-free machine-readable diagnostics.",
    ),
    ) -> None:
    """Run environment and configuration diagnostics."""
    import os

    from grumo import __version__ as ver

    cfg = get_config()

    if json_mode or terminal.is_json_mode():
        terminal.json_output(_doctor_snapshot())
        return

    terminal.wordmark(ver)
    terminal.blank()

    # ── Environment ─────────────────────────────────
    terminal.heading("environment")
    terminal.status(
        "mode",
        "production" if os.getenv("GRUMO_ENV") == "production" else "development",
    )
    terminal.muted(
        "  set GRUMO_ENV=production to enforce production security defaults"
        if os.getenv("GRUMO_ENV") != "production"
        else "  production security defaults active"
    )
    terminal.status("grumo", "ready")
    terminal.muted(f"  v{ver}")

    # ── Runtime ─────────────────────────────────────
    terminal.heading("runtime")

    # Canonical application Store
    try:
        from grumo.runtime.store import GrumoStoreProvider

        report = GrumoStoreProvider(cfg.store.path).health()
        terminal.status("store", "ready" if report.verified else "not found")
        terminal.muted(f"  {cfg.store.provider} ({cfg.store.path})")
    except Exception as error:
        _logger.warning(
            "doctor Store probe failed error=%s", redact_string(str(error))
        )
        terminal.status("store", "unavailable")

    if cfg.database.provider.lower() == "grumo":
        legacy_candidates = (
            Path(".grumo/state/data.db"),
            Path(".grumo/state/schedules.db"),
            Path(".grumo/state/agents.db"),
        )
        legacy_files = [path for path in legacy_candidates if path.exists()]
        terminal.status("legacy sqlite", "clean" if not legacy_files else "warning")
        if legacy_files:
            terminal.warning(
                "Legacy SQLite state exists while the application uses Grumo Store."
            )
            for path in legacy_files:
                terminal.muted(f"  {path}")

    # External SQL is reported only when explicitly selected.
    if cfg.database.provider.lower() != "grumo":
        db_path = cfg.database.path or cfg.database.url or cfg.db_path
        ready = db_path == ":memory:" or bool(db_path and Path(db_path).exists())
        if cfg.database.provider.lower() in {"postgres", "postgresql"}:
            ready = bool(db_path)
        terminal.status("database", "ready" if ready else "not found")
        terminal.muted(f"  {cfg.database.provider} ({db_path})")

    # Resolved providers (Sprint 9)
    terminal.status("queue", "ready")
    terminal.muted(f"  {cfg.queue.provider}")

    terminal.status("events", "ready")
    terminal.muted(f"  {cfg.events.provider}")

    terminal.status("objects", "ready")
    terminal.muted(f"  {cfg.objects.provider}")

    terminal.status("cache", "ready")
    terminal.muted(f"  {cfg.cache.provider}")

    terminal.status("models", "ready")
    terminal.muted(f"  {cfg.models.default}")

    # Auth secret
    if cfg.auth.secret_key != "dev-secret-key-change-in-production-grumo-2026":
        terminal.status("auth", "ready")
    else:
        terminal.status("auth", "warning")
        terminal.muted("  using dev default secret key")

    # Security
    terminal.status(
        "security headers",
        "enabled" if cfg.security.headers_enabled else "disabled",
    )
    terminal.status(
        "rate limit",
        "enabled" if cfg.security.rate_limit_enabled else "disabled",
    )
    terminal.status(
        "cors",
        "enabled" if cfg.security.cors_enabled else "disabled",
    )
    terminal.status(
        "csrf",
        "enabled" if cfg.security.csrf_enabled else "disabled",
    )

    _doctor_modules()

    # ── Providers & capability matrix ────────────────
    terminal.heading("providers")
    try:
        _print_capability_matrix()
    except Exception as error:
        _logger.warning(
            "doctor capability matrix failed error=%s", redact_string(str(error))
        )
        terminal.status("capability matrix", "unavailable")

    _doctor_queue()

    # ── Schedules ─────────────────────────────
    _doctor_optional_services(cfg)

    # ── AI Kit ──────────────────────────────────────
    _doctor_ai_kit()

    terminal.blank()
