# Installation

## What it is

Grumo is a programmable runtime for adaptive applications and operational systems. It installs as a single package with optional extras for AI providers and MCP integration.

## Quick install

```bash
pip install grumo
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv tool install --python 3.12 grumo
```

## Project installation

```bash
uv add grumo
uv run grumo --help
```

The [Homebrew tap](https://github.com/helderperez-dev/homebrew-grumo) is undergoing installation validation.

## Optional extras

Grumo keeps the core install lean. AI provider SDKs are lazy — install only what you need:

```bash
pip install "grumo[ai]"      # OpenAI, Anthropic, Gemini, Ollama SDKs
pip install "grumo[dev]"     # pytest, ruff, mypy, pre-commit
pip install "grumo[ai,dev]" # combine extras
```

## Verify the install

```bash
grumo version
```

## Scaffold a new project

```bash
grumo new my_app
cd my_app
grumo dev
```

The app starts on `http://localhost:8000` with hot-reloading enabled.

`grumo new` is the canonical scaffold and creates the supported Store-first
application shape. Durable tasks, schedules, events, objects, and agents are
added through the same Runtime as the application grows. The hidden
`grumo create` command remains a compatibility alias for the deprecation
window and emits a warning.

```
my_app/
├── main.py              # App entry point — full runtime demo
├── grumo.toml          # Runtime configuration
├── pyproject.toml       # Python project metadata
├── app/                 # Folder-based routes (add page.py files here)
└── .grumo/
    └── application.grumo  # Local durable Store state
```

> **Tip:** Keep the generated project minimal and add capabilities as they are
> needed; this keeps the first deployment surface understandable.

The generated project includes `main.py` and `grumo.toml`. The default embedded Store requires no external infrastructure.

## AI development context (optional)

```bash
grumo ai init              # auto-detect IDE
grumo ai init --ide cursor # specific IDE
grumo ai init --ide all    # all supported IDEs
```

Generates `.grumo/ai/` context docs and IDE-specific rule files. Removing `.grumo/ai` never breaks the application.

## Python version

Grumo requires Python 3.12 or later.

## Development setup

For contributing to Grumo itself:

```bash
git clone https://github.com/helderperez-dev/grumo.git
cd grumo
pip install -e ".[dev]"
pre-commit install
pytest
```

## Configuration

Grumo 1.0 retains `grumo.toml`, `GRUMO_*` variables, `.grumo/application.grumo` and advanced `grumo.*` imports for compatibility.

Grumo reads configuration from `grumo.toml` (preferred), `grumo.yaml` (compatibility), and environment variables.

**Precedence:** `grumo.toml` > `grumo.yaml` > environment variables > defaults

Minimal `grumo.toml`:

```toml
[app]
name = "my_app"
```

Environment variables:

| Variable | Default | Description |
|---|---|---|
| `GRUMO_ENV` | `development` | Environment name |
| `GRUMO_DEBUG` | `true` (dev) | Debug mode |
| `GRUMO_SECRET_KEY` | dev secret | JWT signing secret |
| `GRUMO_JWT_ISSUER` | unset | Optional exact JWT issuer claim |
| `GRUMO_JWT_AUDIENCE` | unset | Optional exact JWT audience claim |
| `GRUMO_JWT_CLOCK_SKEW` | `0` | Accepted clock drift in seconds, bounded to 300 |
| `GRUMO_JWT_PREVIOUS_SECRETS` | unset | Comma-separated old signing secrets during rotation |
| `GRUMO_JWT_REVOCATION_MAX` | `10000` | Maximum process-local revoked-token entries |
| `GRUMO_DB_PATH` | `.grumo/state/data.db` | SQLite database path |
| `DATABASE_URL` | — | Database URL (overrides path) |
| `GRUMO_HOST` | `0.0.0.0` | Server host |
| `GRUMO_PORT` | `8000` | Server port |

Infrastructure configuration (database provider, storage provider, etc.) is optional — Grumo provides intelligent defaults.
