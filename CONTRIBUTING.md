# Contributing to Grumo

Thank you for contributing to Grumo. This guide describes the development
workflow, architectural contract, quality gates, and release discipline.

## Getting started

Requirements: Python 3.12+, uv, Git, and optionally just.

```bash
git clone https://github.com/helderperez-dev/grumo.git
cd grumo
uv sync --all-extras --dev
just test
```

Create focused branches from `main` and use Conventional Commits.

## Quality gates

A change is merge-ready only when the repository gates relevant to it pass:

```bash
just format
just lint
just typecheck
just test
```

CI additionally validates Python 3.12 and 3.13, the clean Store-first
installation path, and architecture invariants. CodeQL must be green for the
final PR head. Mypy/type checking is a hard CI gate.

Do not add `# noqa` to source to bypass a failure. Refactor the underlying
problem or make a deliberate lint-policy change with architectural rationale.

## Architecture contract

Read these before a structural or cross-domain change:

- [Repository architecture](docs/architecture/repository.md)
- [Architecture governance](docs/architecture/governance.md)
- [Repository migration map](docs/architecture/repository-migration.md)

The dependency direction is:

```text
primitives / protocol
        ↑
world / core contracts
        ↑
runtime
        ↑
application surfaces (ui, data, auth, ai, edge)
        ↑
integrations / cli
```

Runtime implementation ownership:

```text
runtime/
├── execution/
├── reconciliation/
├── scheduling/
├── agency/
├── distributed/
└── inspection/
```

There is one execution authority. Workers, distributed fabric, agents, mesh,
and edge participants must converge on it rather than introduce parallel
execution models.

Vendor-backed implementations belong outside the semantic center. For example,
AI SDK providers live in `integrations/ai`, MCP interoperability in
`integrations/mcp`, and OpenTelemetry export in `integrations/otel.py`.
Vendor-backed Storage implementations can remain in `storage/` when Storage
is their semantic contract.

Existing compatibility facades are not implementation owners. Put new behavior
in the canonical owner and keep facades thin.

## Project structure

The primary semantic domains are:

```text
src/voodoo/
├── core/
├── primitives/
├── protocol/
├── world/
├── runtime/
├── ui/
├── data/
├── auth/
├── ai/
├── edge/
├── integrations/
├── observability/
├── cli/
└── _internal/
```

Other existing namespaces may provide application surfaces, storage contracts,
security mechanics, or compatibility paths. Creating a new top-level domain
requires an explicit architecture decision and documentation update.

## Testing

Tests are owned semantically:

```text
tests/
├── unit/
├── integration/
├── e2e/
├── contracts/
└── architecture/
```

- Unit tests belong to the closest semantic source owner.
- Integration tests cover interactions across domains.
- E2E tests cover developer/user journeys.
- Contract tests define portable provider/protocol behavior.
- Architecture tests enforce repository invariants.
- Compatibility behavior may live in the closest unit/integration domain.
- Do not add flat `tests/test_*.py` files.
- Every durability claim requires failure-path coverage (crash, restart,
  retry/lease expiry, duplicate delivery, or the relevant failure mode).

Use `pytest-asyncio` for async tests and `tmp_path` for filesystem isolation.

## Adding a provider or integration

1. Identify the semantic contract first.
2. Keep vendor-independent contracts in their semantic domain.
3. Put vendor SDK implementation in the appropriate integration/provider
   boundary.
4. Keep third-party packages optional unless they are part of the base runtime
   contract.
5. Add contract tests when implementing a portable infrastructure/provider
   interface.
6. Update capability declarations honestly.
7. Update docs/changelog for material behavior.

Do not introduce vendor imports into `core`, `runtime`, `primitives`,
`protocol`, or `world`.

## Public API and compatibility

`grumo.__init__` exposes the intentionally small application API backed by
`voodoo.__init__`. Advanced imports remain in `voodoo.*` in Grumo 1.0. Advanced APIs belong to their
semantic owners.

Before moving or removing a public symbol:

1. search documented and tested imports;
2. decide whether the change is additive, a documented migration, or a future
   major-version break;
3. update `docs/public-api-3.md` and contract coverage for intentional API changes;
4. do not recreate compatibility-only 2.x namespaces that 3.0 deliberately removed.

Compatibility inside an implementation boundary (for example adapting a
limited Store binding behind a stable Framework contract) is different from
restoring duplicate public import paths.

## Pull request checklist

- [ ] semantic owner is correct;
- [ ] dependency direction is preserved;
- [ ] no duplicate execution/scheduling authority exists;
- [ ] vendor dependencies remain outside semantic Core;
- [ ] public imports are preserved or the breaking change is explicit;
- [ ] tests are in the correct semantic test domain;
- [ ] durability claims have failure-path tests;
- [ ] no source `# noqa` was introduced;
- [ ] Ruff/format, type check, tests, Store-first, and CodeQL are green;
- [ ] architecture tests are updated for deliberate boundary changes;
- [ ] `CHANGELOG.md` and docs are updated for material changes.

## Release process

Publish Grumo through `.github/workflows/publish-grumo.yml` using PyPI Trusted Publishing.

Prepare the version and changelog in a PR, verify all gates, merge to `main`,
then dispatch the publish workflow with the exact version. Verify the PyPI
artifacts and isolated installation before announcing the release.

Minor versions add backward-compatible capability; patches are fixes only;
major versions are reserved for intentional compatibility breaks.
