# Canonical package navigation

This page is the contributor-facing map for Grumo 3.x. It answers two
questions before a new module is added: which semantic owner should contain it,
and which public import should applications use?

## Public entry points

| Need | Canonical import | Owner |
| --- | --- | --- |
| Application lifecycle and state | `grumo.App`, `grumo.state` | `grumo.core` |
| Durable application data | `grumo.Model` / `grumo.data` | `grumo.data` + RuntimeStore |
| Canonical execution | `grumo.runtime.Execution*` | `grumo.runtime.execution` |
| Jobs and scheduling | `grumo.task`, `grumo.runtime.scheduling` | Runtime scheduling |
| Events and outbox | `grumo.events`, `grumo.runtime.transaction` | Runtime/events |
| UI and design system | `grumo.ui.*` | `grumo.ui` |
| Authentication and identity | `grumo.auth`, `grumo.runtime.identity` | Auth/Runtime identity |
| Devices and edge state | `grumo.edge.*` | `grumo.edge` |
| AI providers and tools | `grumo.ai.*` | `grumo.ai` |
| External infrastructure | `grumo.storage.*`, `grumo.adapters.*` | Storage/adapters |
| Developer commands | `grumo.cli` and `grumo new` | CLI |

## Ownership rules

1. Use the narrowest existing semantic owner; do not add a package-root module
   for convenience.
2. Runtime owns authority, execution semantics, identity projection and
   lifecycle. Store owns durable mechanics and recovery.
3. `grumo.data` is the application persistence facade; application code must
   not depend on native `grumo_store` types.
4. Provider SDKs belong behind `grumo.integrations` or an explicit storage
   adapter and must remain optional from the semantic core.
5. Compatibility facades are temporary, documented and covered by the public
   API compatibility registry. They are not new semantic owners.

## Choosing a location

When a feature crosses domains, place its contract at the semantic boundary
that owns the decision and keep provider-specific work in the adapter layer.
For example, a durable workflow belongs under `grumo.runtime.workflow` while
its native persistence adapter belongs under Store-backed runtime storage; a
button belongs under `grumo.ui`, not under a product or application module.

See [repository architecture](repository.md), [architecture governance](governance.md),
and the [public API law](../public-api-3.md) for the rules enforced by CI.
