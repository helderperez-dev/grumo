# Grumo — ecosystem migration blueprint

Status: **implementation in phases; not a completed rename**.

## Product identity and scope

**Grumo** is the successor brand for the existing programmable runtime,
application framework and infrastructure engine. Preserve the original Grumo
architecture: application APIs/UI, durable Store, canonical governed Execution,
AI agents, workflows, World model, Runtime Fabric and Edge devices. Local-first
and offline synchronization are deployment options and roadmap features, **not
a narrowing of the runtime's purpose**.

### Intended public surface

| Current | Target |
| --- | --- |
| `helderperez-dev/grumo` | `helderperez-dev/grumo` |
| `helderperez-dev/grumo-store` | `helderperez-dev/grumo-store` |
| `helderperez-dev/grumo-edge` | `helderperez-dev/grumo-edge` |
| `helderperez-dev/grumo-site` | `helderperez-dev/grumo-site` |
| `helderperez-dev/grumo-templates` | `helderperez-dev/grumo-templates` |
| `helderperez-dev/grumo-skills` | `helderperez-dev/grumo-skills` |
| `helderperez-dev/homebrew-grumo` | `helderperez-dev/homebrew-grumo` |
| `grumo-framework` on PyPI | `grumo` (availability/publish gate) |
| `grumo-store` on PyPI | `grumo-store` |
| `from grumo import App` | `from grumo import App` |
| `import grumo_store` | `import grumo_store` |
| `grumo new / dev / start` | `grumo new / dev / start` |
| `.grumo/application.grumo` | `.grumo/application.grumo` |
| `GRUMO_*` | `GRUMO_*` |
| `grumo.toml` | `grumo.toml` |
| `grumo-store-core` crate | `grumo-store-core` |
| `grumo-store-ffi` crate | `grumo-store-ffi` |
| `grumo-store-cli` crate | `grumo-store-cli` |

The exact rename of C ABI symbols, protocol identifiers, websocket routes and
persisted record names requires an explicit compatibility policy; do not bulk
replace those merely because they contain the Grumo prefix.

## Implementation order

1. **Preparation and gates**
   - Inventory references across repositories, scripts, lockfiles, installer,
     deployment and release workflows.
   - Record current test, wheel, fixture and documentation baselines.
   - Validate package namespace ownership, brand rights and domain ownership
     before public releases.
   - Preserve Git history, release tags and supported old installers.

2. **Store compatibility / Rust / Python**
   - Retain the versioned binary Store format; rename only its *default*
     filename and human-facing package identity.
   - Introduce and test `.grumo/application.grumo` using a closed, verified
     copy of the legacy file. Never overwrite the original.
   - Update Rust crate names, C headers/ABI through explicit transition,
     PyO3 module paths, maturin, packages, entry points, tests and CI.
   - Preserve historical fixtures, backup/restore and rollback.

3. **Framework public API**
   - Rename `src/grumo` to `src/grumo` and adjust relative/absolute imports
     as one atomic code change.
   - Update dynamic version attribute, package discovery, scripts, package
     data, type tooling, docs manifest, scaffold engine, tests and lockfiles.
   - Make `GRUMO_*` canonical; handle old variables with an explicit and
     tested deprecation/precedence policy.
   - Preserve one Runtime and one canonical governed Execution lifecycle.

4. **Generated applications / Store path**
   - Fresh apps use `.grumo/application.grumo` and `grumo.toml`.
   - Existing apps use a **separate, explicit migration CLI**:
     stop writer, verify old, make backup, copy into new path, verify Store ID
     and format, smoke-test reads, activate, preserve rollback copy.
   - Never silently change a configured external path or auto-move user data.

5. **Ecosystem**
   - Move Edge SDK namespace, include files, PlatformIO/Arduino manifests and
     device/docs examples without changing wire-protocol semantics accidentally.
   - Update canonical templates and vendored scaffold in lockstep.
   - Update skills, site, documentation, package badges and Homebrew.
   - Apply approved black/white master logo and supporting leaf-green palette.

6. **Publish and rename GitHub repos**
   - Publish Store before Framework; test clean install of both from artifacts.
   - Pass cross-platform CI, legacy data fixture checks, old/new CLI acceptance,
     docs and site smoke tests and supply-chain release gates.
   - Then rename GitHub repositories and update external URL/config consumers.
   - Keep old package names as clearly documented transition surfaces if needed.

## Explicit non-goals

- No rewrite of Store's binary format just to change `.vstore` to `.grumo`.
- No automatic Store replication, global consensus, multi-writer local file,
  global transaction or exactly-once claim.
- No architectural reduction to a local-first-only framework.
- No new features combined with the naming migration.

## Release acceptance

- `pip install grumo-store` and `pip install grumo` from published artifacts.
- `grumo new sample && grumo dev` generates and starts a clean application.
- `from grumo import App, Model, task` and `from grumo_store import Store`
  work from clean environments.
- Example app has no mandatory Redis/PostgreSQL/S3 infrastructure.
- Legacy `.vstore` data is readable from a `.grumo` path with verified
  unchanged Store identity and format.
- Old application rollback and backup/restore drills succeed.
- Web UI sessions, API auth/security, distributed fabric and Edge canaries pass.
- Docs, templates, skills and site agree on one public API and CLI.
- Branch protection, packaging provenance and release gates are satisfied.

## Migration tracker

| Stage | Status |
| --- | --- |
| Store compatibility PR | In review (grumo-store PR #23) |
| Store package / crate rename | Not started |
| Framework code / public API rename | Not started |
| Default Store path + migration CLI | Not started |
| Templates, skills, site, Edge, Homebrew | Not started |
| CI / releases / repository names | Not started |

This file is the migration-specific plan; `ROADMAP.md` and
`SPRINT_PLAN.md` remain the authoritative sources for existing Runtime work
until this rebrand is validated and merged.
