# Grumo PyPI release cutover

This is the public package migration plan for Grumo → Grumo. The existing
distribution `grumo-framework==3.2.2` and Store `grumo-store==0.3.2`
remain live until the replacement packages build, publish, and pass validation.

## Required new packages

| Distribution | Python import | Owner repository | Publisher workflow |
| --- | --- | --- | --- |
| `grumo-store` | `grumo_store` | `helderperez-dev/grumo-store` | `.github/workflows/publish-grumo-store.yml` |
| `grumo` | `grumo` | `helderperez-dev/grumo` | `.github/workflows/publish-grumo.yml` |

The project names are *targets only*: do not assume availability/ownership
until checked in a fresh PyPI authenticated session or official JSON endpoint.

## Before adding a trusted publisher

1. Rename the repositories **after** branch CI and cross-repo package tests.
2. Use the new OIDC workflows `publish-grumo.yml` and
   `publish-grumo-store.yml`, which gate publishing on canonical package
   identity and release artifacts.
3. On PyPI, create a **pending Trusted Publisher** for each new distribution
   and provide exact GitHub owner, repo, workflow filename, and environment
   (recommended `pypi`).
4. Align `environment.name`, `id-token: write` and artifact provenance in
   each release workflow. Keep secrets out of the repository.
5. If the GitHub repository is renamed again, update the PyPI trusted
   publisher configuration; the old repository name does not authorize the
   new repository automatically.

Official guide: https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/

## Store first

- [ ] Rename Rust workspace packages, internal dependencies and Cargo.lock
      consistently. Keep persisted file magic/version/schema unchanged.
- [ ] Rename `python/grumo_store` to `python/grumo_store` and update
      PyO3/maturin extension path.
- [ ] Update Python imports across package, tests, scripts and release jobs.
- [ ] Build all Rust and wheel targets, including supported Python 3.9–3.13.
- [ ] Preserve fixture `legacy-0.2.2.vstore` and retention/rollback evidence.
- [ ] Publish signed/attested Grumo Store artifacts; validate exact installed
      wheel and sdist from clean environments.

## Framework second

- [ ] Rename module directory to `src/grumo`, package discovery and dynamic
      version config, preserving public behavior.
- [ ] Depend on the published compatible `grumo-store` release.
- [ ] Update CLI to `grumo`, leaving `grumo` as a deliberate transition
      entrypoint where necessary.
- [ ] Ensure scaffold creates `grumo.toml` and new Store path for new apps.
- [ ] Verify generated apps do not rely on old import/package names.
- [ ] Verify installed wheel and sdist independently (not only editable mode).
- [ ] Publish with GitHub OIDC Trusted Publishing after the Store release.

## Compatibility and migration guidance

- Do not silently reinterpret legacy `.vstore` files as a new data format.
- Do not claim automatic distributed Store replication or local-first as the
  entire Grumo positioning.
- Announce the new PyPI package names and document uninstall/reinstall
  behavior. Installing both old and new packages may produce console-script
  conflicts; explicitly test them in isolated environments.
- Do not delete existing PyPI projects or their historical releases. Existing
  installs must continue resolving consistent artifacts.
- Do not change Homebrew `grumo` formula until both new PyPI distributions
  exist. Homebrew formula name `grumo` and tap rename are a separate cutover.

## Final smoke commands

```sh
python -m venv /tmp/grumo-clean
/tmp/grumo-clean/bin/python -m pip install --upgrade pip
/tmp/grumo-clean/bin/python -m pip install grumo-store grumo
/tmp/grumo-clean/bin/python -c "import grumo, grumo_store; print(grumo.__version__)"
/tmp/grumo-clean/bin/grumo --help
/tmp/grumo-clean/bin/grumo new example-grumo --no-install
```

The above commands are **acceptance criteria, not evidence that these
packages exist today**.
