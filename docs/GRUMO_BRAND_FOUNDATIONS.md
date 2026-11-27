# Grumo brand foundations

Status: approved **direction**, not an assertion that final logo vectors have
passed production asset review.

## Brand position

**Grumo** is the name of the programmable runtime and application ecosystem
previously developed as Grumo. It builds and orchestrates applications,
APIs, reactive interfaces, durable jobs and workflows, AI agents, distributed
nodes and connected devices. Its embedded Store is a first-class low-dependency
foundation; local-first is an option, not the whole product.

### Brand attributes

- Clear, approachable, technically credible, durable and restrained.
- Friendly without mascots, imitation of Python, or playful toy styling.
- A product used by developers and trusted by businesses.
- Minimal instead of futuristic gradients, glows, illustrations of AI brains,
  arbitrary floating blocks or generic infrastructure icons.

## Approved visual direction

- **Master logo is monochromatic:** black mark and lowercase `grumo` on
  light backgrounds; white reverse on dark backgrounds.
- **No mixing black and green inside the master logo.**
- Preserve approved symbol geometry. Recoloring, layout and responsive
  scaling do not authorize redrawing the symbol.
- Keep the website navigation lockup small and unobtrusive.
- Use ample whitespace, crisp typography, accessible contrast, product-led
  examples and clear UI copy.
- The type direction is **Satoshi** for brand/display and UI; monospace
  for code (JetBrains Mono is a candidate). Verify font licensing before
  bundling or deployment. Do not commit vendor font binaries casually.
- Light theme first, with considered dark-theme support.

## Supporting palette (exploratory tokens)

The following palette is a **design starting point**, not a finalized
accessible UI token system:

| Role | Token | Hex |
| --- | --- | --- |
| Logo / text on light | `--grumo-ink` | `#1B1B16` |
| Warm surface | `--grumo-canvas` | `#F8F7F2` |
| Leaf green | `--grumo-leaf` | `#6EA61F` |
| Deep green | `--grumo-forest` | `#294D31` |
| Sand | `--grumo-sand` | `#D8C8A8` |
| Ochre accent | `--grumo-ochre` | `#D4A017` |
| Stone / muted | `--grumo-stone` | `#8B8B82` |

Use black/white for the logo regardless of secondary color scheme. Leaf green
can be used for emphasis, buttons, product highlights and illustration details;
verify all actual UI foreground/background combinations for WCAG contrast.

## Product family

- **Grumo** — framework and coherent Runtime.
- **Grumo Store** — embedded data, messaging, scheduling and durable state.
- **Grumo Fabric** — distributed execution with bounded failure semantics.
- **Grumo Edge** — device integration.
- **Grumo Sync** — future synchronization; do not claim it ships today.
- **Grumo Cloud** — future hosted product; do not imply a production service.

## Homepage guidance

Use a lightweight wordmark in header; lead with product value, not a massive
emblem or decorative 3D hero. Show a real Grumo API example or meaningful
application/runtime UI. Recommended concise line:

**Build. Run. Orchestrate.**

Supporting copy should reference APIs, jobs, workflows, AI and distributed
systems, with capability and maturity claims limited to verified features.

## Assets and deliverables required before website cutover

- Reviewed master symbol and lowercase wordmark as clean SVG outlines.
- Horizontal lockup, icon-only mark, black/white reverses, favicon at 16–48px.
- Brand spacing, sizing and minimum clear-space rules.
- Light/dark components and contrast validation.
- Developer documentation and release-template treatments.
- Website screenshots across mobile/desktop, accessibility/visual CI.
- Black and white merchandise options; use brand green as an optional accent.
