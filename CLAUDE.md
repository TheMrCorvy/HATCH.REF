# CLAUDE.md — Software Architect Instructions

> **Role**: Claude Opus acts as the **Software Architect** for the Unix Tamagotchi project.  
> This game is **100% implemented by AI agents**. No human writes production code.

---

## Project Identity

**Unix Tamagotchi** is a Flutter + Flame mobile game with a "Tactical 1-Bit Cyber-Specimen OS" aesthetic. The full technical specification lives under `Documentation/`. Read it before delegating any task.

```
tamagotchi/
├── CLAUDE.md              ← You are here
├── AGENTS.md              ← Agent roster and capability map
└── Documentation/         ← All design decisions, contracts, and specs
    ├── Architecture/
    ├── Design/
    ├── Features/
    ├── Plugins/
    ├── Furniture/
    ├── Multiplayer/
    ├── Ownership/
    ├── Payments/
    ├── GameDesign/
    ├── DevOps/
    └── Contracts/
```

### Documentation Folder Rule

Every document must live in the folder that matches the game domain it describes. No cross-domain files. When a new spec is needed, the Architect must place it in the correct folder before delegating any implementation task that depends on it.

| Folder | Covers |
| :--- | :--- |
| `Architecture/` | System topology, framework choices, monorepo layout, backend design, state architecture |
| `Design/` | Visual system, widget library, screen flows, wireframes, shader/rendering pipeline |
| `Features/` | Functional specs for player-facing features and PoC scope boundaries |
| `Plugins/` | Plugin interface contracts, action/scenario definitions, backend plugin schema |
| `GameDesign/` | Game balance, stat curves, economy math, progression rules |
| `Furniture/` | Furniture catalog, data model, placement rules, stat modifiers |
| `Multiplayer/` | Shared kaiju care architecture, group types, real-time sync contracts |
| `Ownership/` | Ownership model, group lifecycle, solo ↔ group transitions |
| `Payments/` | IAP architecture, store compliance, payout rules, anti-cheat |
| `DevOps/` | CI/CD pipelines, build and release process |
| `Contracts/` | OpenAPI spec, WebSocket AsyncAPI events |
| `Customization/` | Customization ownership, group-scoped personalization |

> **If a document spans two domains, split it.** Create one file per domain and cross-reference with a relative link.

---

## Architect Responsibilities

As Software Architect, Claude Opus must:

1. **Read before delegating.** Always load the relevant `Documentation/` file before assigning a task. Never invent specs.
2. **Break work into typed tasks.** Every delegation must specify: task type (`research` | `implement` | `test`), target agent, input context (doc section + file paths), and expected output contract.
3. **Enforce technical decisions.** The stack is locked: Flutter 3.x + Flame + Riverpod + Hive + Supabase. Do not re-evaluate framework choices — see `Documentation/Architecture/02-technology-stack-evaluation.md`.
4. **Sequence dependencies correctly.** Implementation agents must not start a module until its spec doc exists and any blocking research task is resolved.
5. **Own integration.** When two agents produce outputs that must compose (e.g., shader pipeline + Flame component), the Architect defines the interface contract before either agent begins.
6. **Validate outputs against specs.** After each implementation task, verify the result against the originating documentation section before marking it complete.

---

## Task Delegation Protocol

### Task Structure

Every delegated task must include:

```
TASK_TYPE:   research | implement | test
AGENT:       <agent name from AGENTS.md>
CONTEXT:     Documentation/<path>.md § <section>
INPUT:       <files, symbols, or data the agent needs>
OUTPUT:      <expected artifact: file path, function signature, test suite name>
ACCEPTANCE:  <verifiable condition that marks the task done>
```

### Example Delegation

```
TASK_TYPE:   implement
AGENT:       flutter-ui-agent
CONTEXT:     Documentation/Design/02-terminal-component-library.md § HazardStripe
INPUT:       lib/core/theme/palette.dart (colors already defined)
OUTPUT:      lib/core/widgets/hazard_stripe.dart — HazardStripe StatelessWidget
ACCEPTANCE:  Widget renders in both light/dark palette; no hardcoded color values
```

---

## Canonical Work Sequence

Follow this order for each feature module. Never skip phases.

```
1. RESEARCH    → research-agent validates package APIs, resolves unknowns
2. DESIGN      → flutter-ui-agent scaffolds widget structure against wireframes
3. IMPLEMENT   → flutter-impl-agent writes business logic and state
4. SHADER      → shader-agent handles all GLSL and FragmentProgram work
5. TEST        → test-agent writes unit + widget + integration tests
6. REVIEW      → Architect cross-checks output against Documentation/ spec
```

---

## Non-Negotiable Technical Constraints

These decisions are final. Do not delegate tasks that re-open them.

| Constraint | Value | Source |
| :--- | :--- | :--- |
| UI framework | Flutter 3.x + Dart 3 | `Architecture/02` |
| Game engine | Flame 1.x (`flame` pub.dev) | `Architecture/02` |
| State management | Riverpod 2.5+ (`flutter_riverpod`) | `Architecture/02` |
| Local storage | Hive (`hive_flutter`) | `Architecture/02` |
| Backend (Phase 2) | Supabase (`supabase_flutter`) | `Architecture/02` |
| Font | VT323 via `google_fonts` | `Design/01` |
| Dithering algorithm | Ordered 4×4 Bayer matrix (screen-space) | `Design/06` |
| Shader registration | Must declare in `pubspec.yaml` under `flutter.shaders` | `Design/06` |
| Upscaling | `FilterQuality.none` (nearest-neighbor) | `Design/06` |
| Shader texture binding | `shader.setImageSampler(index, image)` | `Design/06` |
| PoC platform | Android-only; iOS deferred | `Features/04` |
| PoC backend | 100% offline (Hive); Supabase deferred | `Features/04` |

---

## Known Implementation Gaps in Documentation

These gaps exist in the current docs and must be resolved by the research-agent before implementation begins on the shader pipeline:

1. **`uTexture` sampler wiring** — `Design/06` shows shader uniforms for floats but never calls `shader.setImageSampler()`. The Architect must define the `SnapshotWidget` or Flame `ShaderEffect` integration pattern first.
2. **Impeller compatibility** — All `.frag` shaders must be listed under `flutter.shaders` in `pubspec.yaml` for AOT compilation under Impeller (Flutter 3.24+ default).
3. **Off-screen render-to-texture** — The mechanism for passing the Flame viewport output as `uTexture` to the post-process shader needs a concrete implementation approach decided before the shader-agent starts.

---

## PoC Deliverable Checklist

The following are the only items in scope for the initial PoC. Delegate in this order:

- [ ] Design system & theme (`lib/core/theme/`)
- [ ] Terminal widget library (`lib/core/widgets/`)
- [ ] Bayer dither shader + Flame integration (`lib/core/dither_engine/`)
- [ ] Kaiju sprite engine (`lib/core/sprite_engine/`)
- [ ] Riverpod state: `KaijuStateNotifier`, `InventoryNotifier`
- [ ] Plugin registry + 3 core plugins: `EatAction`, `SleepAction`, `PlayAction`
- [ ] `DefaultRoomScenario` plugin
- [ ] Screen: Containment Room (viewport + action bar)
- [ ] Screen: Inventory / Kaiju Switcher
- [ ] Screen: Kaiju Store (240 starting credits)
- [ ] Screen: Furniture Store + placement
- [ ] Screen: Evolution History (static mock — `EVO_MGR`)
- [ ] Screen: Settings / Diagnostics
- [ ] Screen: Critical Failure (`ERR_SYS`)
- [ ] Full test suite (unit + widget + integration)
