import logging
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from textwrap import dedent

from rich.progress import Progress

from grumo.security.redaction import redact_string

logger = logging.getLogger(__name__)

AI_DOCS_BASE_URL = (
    "https://raw.githubusercontent.com/helderperez-dev/grumo/main/docs/ai"
)
AI_TRAE_SKILL_URL = "https://raw.githubusercontent.com/helderperez-dev/grumo/main/.trae/skills/grumo-builder/SKILL.md"


def _write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _fetch_text(url: str, timeout: int = 3) -> str | None:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            if isinstance(data, bytes):
                return data.decode("utf-8")
            if isinstance(data, str):
                return data
    except (OSError, TimeoutError, UnicodeError, ValueError, urllib.error.URLError) as error:
        logger.warning(
            "remote AI asset fetch failed url=%s error=%s",
            redact_string(url),
            redact_string(str(error)),
        )
    return None


def _build_workspace_rules() -> str:
    return (
        dedent(
            """
        # Grumo AI Workspace

        This project uses the Grumo Framework.

        Start by reading these local files in order:
        1. `.grumo/ai/README.md`
        2. `.grumo/ai/RULES.md`
        3. `.grumo/ai/ARCHITECTURE.md`
        4. `.grumo/ai/ROUTING.md`
        5. `.grumo/ai/COMPONENTS.md`
        6. `.grumo/ai/STATE.md`
        7. `.grumo/ai/DATABASE.md`
        8. `.grumo/ai/SKILLS.md`
        9. `.grumo/ai/MESH.md`
        10. `.grumo/ai/SEO.md`

        Core rules:
        - Use public components from `grumo.ui` instead of raw HTML templates.
        - Prefer `async def` for handlers and I/O.
        - Use Grumo's `A` component with a normal internal `href`; the client runtime handles navigation.
        - Keep app code in `app/`; durable application data belongs in Grumo Store.
        - Use Grumo `Model` and the application Store by default; SQL adapters are explicit.
        - Preserve the large-cookie websocket settings in `grumo dev`.

        If Trae skills are available, use `.trae/skills/grumo-builder/SKILL.md`.
        """
        ).strip()
        + "\n"
    )


def _build_cursor_rules() -> str:
    return (
        "---\n"
        "description: Grumo framework guidance for Cursor.\n"
        "globs:\n"
        '  - "**/*.py"\n'
        '  - "**/*.md"\n'
        "alwaysApply: true\n"
        "---\n\n" + _build_workspace_rules()
    )


def _fallback_ai_assets() -> dict[str, str]:
    return {
        ".grumo/ai/README.md": dedent(
            """
            # Grumo AI Kit

            This folder gives AI IDEs high-context guidance for building serious Grumo applications.

            Read these files in order:
            1. `RULES.md`
            2. `ARCHITECTURE.md`
            3. `ROUTING.md`
            4. `COMPONENTS.md`
            5. `STATE.md`
            6. `DATABASE.md`
            7. `SKILLS.md`
            8. `MESH.md`
            9. `SEO.md`

            Recommended behavior:
            - Treat Grumo as a Python-first UI framework.
            - Prefer simple, composable route files and reusable components.
            - Respect Grumo navigation, websocket, and data conventions.
            """
        ).strip()
        + "\n",
        ".grumo/ai/RULES.md": dedent(
            """
            # Grumo Rules

            - Build UI with public components from `grumo.ui`.
            - Prefer `async def` for handlers and I/O.
            - Grumo CSS is the default style adapter: components emit semantic
              `vd-*` classes driven by theme tokens. Prefer semantic props
              (`variant`, `size`, `tone`, `level`) over utility classes. Opt into
              Tailwind only with `set_style_adapter(TailwindAdapter())`.
            - Use `A(..., href=...)` for internal links; do not add inline JavaScript.
            - Use folder-based routing: `app/<segment>/page.py` defines a `page(request)`
              function. `app/pages/` (file-per-page) is supported for backward compat.
            - Use Grumo Store-backed models for persistent application data.
            - Use Grumo `Model` and `.grumo/application.grumo` by default.
            - Preserve `WEBSOCKETS_MAX_LINE_LENGTH="8388608"` and `http="h11"` when working with websocket-heavy apps.
            """
        ).strip()
        + "\n",
        ".grumo/ai/ARCHITECTURE.md": dedent(
            """
            # Grumo Architecture

            Grumo is a Starlette-based framework with Python-defined UI and file-based routing.

            Main conventions:
            - `app/` contains routes and app-facing code.
            - `grumo dev` boots the app (`main.py` is optional).
            - `grumo.components` is the primary UI surface.
            - Internal framework API routes remain mounted automatically.
            """
        ).strip()
        + "\n",
        ".grumo/ai/ROUTING.md": dedent(
            """
            # Grumo Routing

            Folder-based routing (the scaffold default): each directory under `app/`
            containing a `page.py` maps to a route.

            - `app/page.py` -> `/`
            - `app/about/page.py` -> `/about`
            - `app/dashboard/settings/page.py` -> `/dashboard/settings`
            - Dynamic segments use bracket folders such as `app/users/[id]/page.py` -> `/users/{id}`

            Each `page.py` defines a `page(request, ...)` function. Path parameters
            are injected by name and coerced to their annotation.

            Return `(SEO, Component)` or `(Component, SEO)` tuples to inject head metadata.

            `app/pages/` (one file per page) is supported for backward compatibility.

            Internal links must use Grumo navigation:

            ```python
            from grumo.components import A

            A("Dashboard", href="/dashboard")
            ```
            """
        ).strip()
        + "\n",
        ".grumo/ai/COMPONENTS.md": dedent(
            """
            # Grumo Components

            Import UI primitives from `grumo.components` (or the `grumo` top level).

            Common components:
            - `Div`, `Text`, `Heading`, `Button`, `A`, `Input`, `Form`
            - Layout: `Page`, `Container`, `Stack`, `Flex`, `Grid`, `Box`
            - Semantic HTML: `Nav`, `Header`, `Footer`, `Main`, `Section`, `Article`, `Aside`, `Figure`, `FigCaption`, `Time`, `Address`, `Img`, `Paragraph`

            Grumo CSS (the default adapter) generates semantic `vd-*` classes from
            each component's style key and props, all driven by `--vd-*` theme tokens.
            Prefer semantic props over utility classes:

            ```python
            from grumo import Button, Heading, Stack, Text, Card

            Stack(
                Heading("Hello, Grumo!", level=1, size="xl"),
                Text("Build your UI in Python.", tone="muted"),
                Button("Get Started", variant="primary"),
                Card(Heading("Folder-based routing", level=3), Text("app/page.py → /")),
            )
            ```

            Use `className` only for one-off overrides. Swap to Tailwind with
            `set_style_adapter(TailwindAdapter())`. Build reusable components as
            small Python functions.
            """
        ).strip()
        + "\n",
        ".grumo/ai/STATE.md": dedent(
            """
            # Grumo State

            Grumo does not use React-style client state hooks.

            Preferred patterns:
            - Form posts for mutations
            - Async route handlers for derived UI
            - Store-backed Model state for persistence
            - WebSockets only when real-time behavior is truly needed
            """
        ).strip()
        + "\n",
        ".grumo/ai/DATABASE.md": dedent(
            """
            # Grumo Persistence

            Default stack:
            - Grumo `Model`
            - Grumo Store at `.grumo/application.grumo`
            - no external database required

            Example:

            ```python
            from grumo import Model

            class Item(Model):
                name: str

            item = await Item.create(name="First item")
            items = await Item.all()
            ```

            SQLite/PostgreSQL are explicit adapters for applications that
            deliberately need external SQL infrastructure.
            """
        ).strip()
        + "\n",
        ".grumo/ai/SKILLS.md": dedent(
            """
            # Grumo AI Skills

            ## Scaffold a Route
            - Create the correct `app/.../page.py` file
            - Export `page(request, ...)`
            - Return public `grumo.ui` components

            ## Create a Component
            - Build a reusable Python function
            - Accept meaningful arguments
            - Style through `className`

            ## Add Data
            - Define durable data with `grumo.Model`
            - Use the application Store at `.grumo/application.grumo`
            - Add SQL adapters only when explicitly required

            ## Debug Navigation
            - Check file-based route placement
            - Check the `A(..., href=...)` target and client navigation runtime

            ## Debug Cookies / WebSockets
            - Check `WEBSOCKETS_MAX_LINE_LENGTH`
            - Check `http="h11"`
            """
        ).strip()
        + "\n",
        ".grumo/ai/MESH.md": dedent(
            """
            # Grumo Mesh

            The Grumo Mesh (`grumo.mesh`) enables real-time WebSocket events and automatic MCP tool registration.

            - Use `@mesh.expose()` to expose functions to RPC and MCP tools.
            - Use `@mesh.on(event)` to listen for local and remote broadcast events.
            - Use `await mesh.broadcast(event, payload)` to push data to all connected clients.
            """
        ).strip()
        + "\n",
        ".grumo/ai/SEO.md": dedent(
            """
            # Grumo SEO & GEO

            Grumo supports native SEO metadata and Generative Engine Optimization (GEO).

            - Return `(SEO(...), Component)` from route handlers.
            - Configure defaults in `grumo.yaml`.
            - Dynamic `sitemap.xml` and `robots.txt` are served automatically.
            - Supports JSON-LD structured data and OpenGraph / Twitter cards.
            """
        ).strip()
        + "\n",
        ".trae/skills/grumo-builder/SKILL.md": dedent(
            """
            ---
            name: "grumo-builder"
            description: "Builds and refactors Grumo apps. Invoke when creating routes, components, data flows, or debugging Grumo-specific behavior."
            ---

            # Grumo Builder

            Use this skill when working on Grumo Framework applications.

            Read these local files before making major changes:
            1. `.grumo/ai/README.md`
            2. `.grumo/ai/RULES.md`
            3. `.grumo/ai/ARCHITECTURE.md`
            4. `.grumo/ai/ROUTING.md`
            5. `.grumo/ai/COMPONENTS.md`
            6. `.grumo/ai/STATE.md`
            7. `.grumo/ai/DATABASE.md`
            8. `.grumo/ai/SKILLS.md`
            9. `.grumo/ai/MESH.md`
            10. `.grumo/ai/SEO.md`

            Follow these Grumo rules:
            - Build UI from `grumo.ui`
            - Prefer `async def` for handlers and I/O
            - Use Grumo navigation primitives for internal links
            - Persist application data through `grumo.Model` and Grumo Store
            - Never add SQLite unless the application explicitly selects it
            - Preserve websocket large-cookie configuration
            """
        ).lstrip(),
    }


def _ide_from_environment() -> str | None:
    env_keys = " ".join(os.environ.keys()).lower()
    term_program = os.getenv("TERM_PROGRAM", "").lower()
    signatures = {
        "trae": ("trae_pid", "trae_resources_path", "__trae_app_dir__"),
        "cursor": ("cursor_trace", "cursor_port", "cursor_session_id"),
        "windsurf": ("windsurf_port", "windsurf_initial_cwd"),
        "vscode": ("vscode_pid", "vscode_injection"),
    }
    return next(
        (
            ide
            for ide, keys in signatures.items()
            if ide in term_program or any(key in env_keys for key in keys)
        ),
        None,
    )


def _ide_from_workspace() -> str | None:
    markers = (
        (".trae", "trae"),
        (".cursor", "cursor"),
        (".windsurfrules", "windsurf"),
        (".vscode", "vscode"),
    )
    directories = [Path.cwd(), *Path.cwd().parents[:3]]
    return next(
        (
            ide
            for directory in directories
            for marker, ide in markers
            if (directory / marker).exists()
        ),
        None,
    )


def _ide_from_processes() -> str | None:
    markers = (
        ("trae", "trae"),
        ("cursor", "cursor"),
        ("windsurf", "windsurf"),
        ("vscode", "vscode"),
        ("code", "vscode"),
    )
    try:
        curr_pid = os.getppid()
        for _ in range(4):
            if curr_pid <= 1:
                return None
            res = subprocess.run(
                ["ps", "-p", str(curr_pid), "-o", "comm="],
                capture_output=True,
                text=True,
                timeout=1,
            )
            comm = res.stdout.strip().lower()
            match = next((ide for marker, ide in markers if marker in comm), None)
            if match:
                return match
            ppid_res = subprocess.run(
                ["ps", "-p", str(curr_pid), "-o", "ppid="],
                capture_output=True,
                text=True,
                timeout=1,
            )
            ppid = ppid_res.stdout.strip()
            if not ppid.isdigit():
                return None
            curr_pid = int(ppid)
    except (OSError, subprocess.SubprocessError, TimeoutError, ValueError) as error:
        logger.debug(
            "IDE process detection unavailable error=%s", redact_string(str(error))
        )
        return None
    return None


def _detect_ide() -> str | None:
    """Auto-detect the active AI IDE/editor."""
    return _ide_from_environment() or _ide_from_workspace() or _ide_from_processes()


def _remote_ai_assets(ide: str) -> dict[str, str]:
    names = [
        "README",
        "RULES",
        "ARCHITECTURE",
        "ROUTING",
        "COMPONENTS",
        "STATE",
        "DATABASE",
        "SKILLS",
        "MESH",
        "SEO",
        "AUTH",
        "SECURITY",
    ]
    assets = {
        f".grumo/ai/{name}.md": f"{AI_DOCS_BASE_URL}/{name}.md" for name in names
    }
    if ide in ("trae", "all"):
        assets[".trae/skills/grumo-builder/SKILL.md"] = AI_TRAE_SKILL_URL
    return assets


def _ide_rule_assets(ide: str) -> dict[str, str]:
    builders = {
        "trae": (".trae/rules", _build_workspace_rules),
        "windsurf": (".windsurfrules", _build_workspace_rules),
        "cursor": (".cursor/rules/grumo.mdc", _build_cursor_rules),
        "vscode": (".github/copilot-instructions.md", _build_workspace_rules),
    }
    selected = (
        builders if ide == "all" else {ide: builders[ide]} if ide in builders else {}
    )
    return {path: builder() for path, builder in selected.values()}


def _write_missing_assets(project_dir: Path, assets: dict[str, str]) -> None:
    for relative_path, content in assets.items():
        target = project_dir / relative_path
        if not target.exists() and content:
            _write_text_file(target, content)


def _sync_ai_assets(project_dir: Path, progress: Progress, ide: str = "none") -> None:
    progress.add_task(description=f"Setting up AI assets ({ide})...", total=None)
    time.sleep(0.2)
    fallback_assets = _fallback_ai_assets()
    fetched = {
        path: _fetch_text(url, timeout=3) or fallback_assets.get(path, "")
        for path, url in _remote_ai_assets(ide).items()
    }
    _write_missing_assets(project_dir, fetched)
    _write_missing_assets(project_dir, _ide_rule_assets(ide))
