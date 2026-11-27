# Compatibility inventory

This is the maintained inventory for compatibility surfaces in the 3.x
Framework. It complements the [repository migration map](repository-migration.md)
with an explicit disposition and review date. New compatibility code must be
added here in the same change.

| Surface | Disposition | Owner | Review / removal condition |
| --- | --- | --- | --- |
| `grumo.components` | Keep as a thin facade | `grumo.ui` | Reconsider at the next major version after migration telemetry is available |
| `grumo.core.state` and `grumo.core.render` | Keep as import facades | `grumo.ui` | Remove only in a declared major-version migration |
| `grumo.telemetry` | Keep as compatibility aliases | `grumo.observability` | Remove after a major version and documented import migration |
| `grumo.mcp` | Keep as public compatibility imports | `grumo.integrations.mcp` | Remove only with a major-version migration |
| `grumo.mesh` | Keep application-facing transport surface | `grumo.runtime.distributed` for authority | Split/remove only after a separately specified distributed profile |
| `grumo.workers` | Keep application-facing compatibility surface | `grumo.runtime.scheduling` | Remove after a major migration and scheduler API replacement |
| `grumo.tools` | Keep import compatibility | `grumo.ai.tools` | Remove after a major migration |
| `grumo.agents` | Keep semantic participant registry | `grumo.agents` | Not a compatibility shim; change requires architecture review |
| `grumo.data.BaseModel` / SQL adapters | Keep explicit legacy adapter | `grumo.data` and `grumo.storage` | No new framework features; remove only after Store-first migration evidence |
| `grumo.yaml` configuration | Keep parser compatibility | `grumo.config` | Prefer `grumo.toml`; remove only in a major version |
| package-root facades | Freeze existing documented imports | Owning canonical domain | No new exports without public API manifest review |

## Rules

- A compatibility surface delegates to one canonical owner and must not create
  a second lifecycle, execution, persistence, or observability authority.
- Compatibility adapters are explicit at call sites; they are not selected by
  hidden fallback when a native Store path is available.
- New code imports canonical owners. Compatibility imports are covered by a
  focused regression test and documented with their migration direction.
- Removal requires a deprecation entry, a migration note, a major-version
  decision, and a passing public API manifest update.

**Inventory baseline:** 2026-10-06. **Next review:** 2027-01-06 or before the
next major-version release, whichever comes first.
