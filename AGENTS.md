# AGENTS.md — Agent Roster

> **Architect**: Claude Opus — assigns all tasks, owns integration contracts, validates outputs.  
> **Agents**: Specialized AI workers. Each agent operates within a defined domain and must not exceed it without Architect approval.

---

## Documentation Structure Rule

All documentation must be stored in `Documentation/` using **one subfolder per game domain**. Agents must write any new spec documents to the correct folder before or alongside implementation. Placing documentation in the wrong folder, or creating a generic catch-all file at the `Documentation/` root, is a scope violation.

| Folder | Game Domain |
| :--- | :--- |
| `Architecture/` | System topology, framework decisions, monorepo layout, backend design, offline state |
| `Design/` | Visual system, widget library, screen flows, wireframes, shader/rendering pipeline |
| `Features/` | Player-facing feature specs and PoC scope boundaries |
| `Plugins/` | Plugin interfaces, action/scenario contracts, backend plugin schema |
| `GameDesign/` | Balance curves, stat math, economy, progression |
| `Furniture/` | Furniture catalog, data model, placement, stat modifiers |
| `Multiplayer/` | Shared kaiju care, group types, real-time sync |
| `Ownership/` | Ownership model, group lifecycle, solo ↔ group transitions |
| `Payments/` | IAP, store compliance, payout rules, anti-cheat |
| `DevOps/` | CI/CD, build pipeline, release process |
| `Contracts/` | OpenAPI spec, WebSocket AsyncAPI events |
| `Customization/` | Customization ownership, group-scoped personalization |

When an agent produces a research report or a design decision that must persist, it must be committed as a Markdown file in the matching `Documentation/<folder>/` — not stored inline in code comments or left undocumented.

---

## Agent Index

| Agent | Domain | Primary Output |
| :--- | :--- | :--- |
| [`research-agent`](#research-agent) | Package APIs, Flutter internals, unknown patterns | Research reports, API usage examples |
| [`flutter-ui-agent`](#flutter-ui-agent) | Terminal widgets, design system, screen layouts | `lib/core/widgets/`, `lib/core/theme/`, `lib/features/*/view/` |
| [`flutter-impl-agent`](#flutter-impl-agent) | Business logic, state, plugins, navigation | `lib/state/`, `lib/plugins/`, `lib/features/*/logic/` |
| [`shader-agent`](#shader-agent) | GLSL shaders, Flame integration, dithering pipeline | `assets/shaders/`, `lib/core/dither_engine/` |
| [`test-agent`](#test-agent) | Unit, widget, and integration tests | `test/` |
| [`backend-agent`](#backend-agent) | Supabase schema, RLS, Edge Functions | `apps/backend/supabase/` |

---

## research-agent

**Purpose**: Resolve technical unknowns before implementation begins. Prevents agents from inventing APIs or guessing behavior.

**Triggers**: Architect delegates a `research` task when:
- A `Documentation/` gap is identified (see `CLAUDE.md § Known Implementation Gaps`)
- A package API needs validation against the current pub.dev version
- A Flutter/Flame internal behavior is uncertain (e.g., Impeller shader compilation, `SnapshotWidget` API)
- A new package is proposed and must be evaluated against `Architecture/02`

**Inputs**: A specific question, a documentation section, and optionally a pub.dev package name.

**Outputs**: A concise written report containing:
- The verified API signature or behavior
- A minimal runnable code example
- Any platform caveats (iOS vs Android, Impeller vs Skia)
- A go/no-go recommendation for the Architect

**Constraints**:
- Must cite the actual package version tested (e.g., `flame: ^1.18.0`)
- Must not write production code — only examples for Architect review
- Must flag any deviation from the locked stack in `CLAUDE.md § Non-Negotiable Technical Constraints`

---

## flutter-ui-agent

**Purpose**: Implement all visual Flutter widgets and screen layouts that do not contain business logic or state mutations.

**Domain**:
- `lib/core/theme/` — palette, typography (`VT323`), box decorations
- `lib/core/widgets/` — `HazardStripe`, `BracketButton`, `TerminalBorder`, `StatusBar`, `DottedDivider`, `ProgressBar`
- `lib/features/*/view/` — screen scaffold and layout (StatelessWidget or UI-only StatefulWidget)

**Spec sources**:
- `Documentation/Design/01-design-system-and-theming.md`
- `Documentation/Design/02-terminal-component-library.md`
- `Documentation/Design/04-screens-flow-and-navigation.md`
- `Documentation/Design/05-1bit-terminal-wireframes.md`

**Inputs from Architect**: Target widget name, the Documentation section to follow, any existing theme/color tokens to use.

**Outputs**: Production-ready Dart widget files. No hardcoded colors (use theme tokens). No business logic. No direct Riverpod reads beyond `ref.watch` on display-only providers.

**Constraints**:
- Font must always come from `google_fonts` (`VT323`)
- All colors must reference `AppPalette` constants from `lib/core/theme/palette.dart`
- No `setState` for data that belongs in Riverpod state
- `FilterQuality.none` on any image that renders pixel art

---

## flutter-impl-agent

**Purpose**: Implement business logic, Riverpod state notifiers, plugin contracts, and navigation.

**Domain**:
- `lib/state/` — `KaijuStateNotifier`, `InventoryNotifier`, `CreditsNotifier`
- `lib/plugins/` — plugin registry, interfaces, and all action/scenario plugin classes
- `lib/features/*/logic/` — feature-level controllers and use-case classes
- `lib/app.dart` — router configuration (`go_router` or `Navigator`)

**Spec sources**:
- `Documentation/Architecture/01-system-overview.md`
- `Documentation/Architecture/06-offline-first-and-state.md`
- `Documentation/Plugins/01-plugin-architecture-overview.md`
- `Documentation/Plugins/02-user-triggered-actions.md`
- `Documentation/Plugins/03-non-user-triggered-actions.md`
- `Documentation/Features/01-core-kaiju-actions.md`
- `Documentation/Features/02-kaiju-store-and-credits.md`
- `Documentation/Features/03-kaiju-inventory-and-switching.md`
- `Documentation/GameDesign/02-balance-curves-and-math.md`

**Inputs from Architect**: Feature name, the plugin or state contract to implement, and any interface already defined by another agent.

**Outputs**: Dart source files for state notifiers, plugin classes, and feature logic. Must be testable (no hard dependencies — use Riverpod providers for injection).

**Constraints**:
- All state must be immutable (`freezed` records or `copyWith`)
- Hive adapters required for any persisted model
- No direct `BuildContext` access in notifiers or plugins
- PoC scope only: no Supabase calls, no IAP, no multiplayer logic

---

## shader-agent

**Purpose**: Implement the entire 1-bit dithering rendering pipeline: GLSL fragment shaders, Flame integration, and the off-screen render-to-texture flow.

**Domain**:
- `assets/shaders/bayer_dither.frag` — the Bayer matrix fragment shader
- `lib/core/dither_engine/` — `DitheredViewport`, `KaijuGame` (FlameGame subclass), `BayerDitherPainter`
- `pubspec.yaml § flutter.shaders` — shader AOT registration

**Spec sources**:
- `Documentation/Design/03-kaiju-dithered-sprite-engine.md`
- `Documentation/Design/06-1bit-dithering-rendering-pipeline.md`

**Prerequisite**: The research-agent must have resolved all three gaps listed in `CLAUDE.md § Known Implementation Gaps` before this agent begins.

**Inputs from Architect**: Resolved research reports for `uTexture` wiring, Impeller AOT registration, and the off-screen render-to-texture approach.

**Outputs**:
- `assets/shaders/bayer_dither.frag` — GLSL shader with `uTexture`, `uResolution`, `uColorLight`, `uColorDark` uniforms
- `lib/core/dither_engine/kaiju_game.dart` — `FlameGame` subclass that renders the kaiju scene
- `lib/core/dither_engine/dithered_viewport.dart` — Flutter widget that composites the Flame game through the Bayer shader using `SnapshotWidget` or equivalent
- `pubspec.yaml` update: shader file registered under `flutter.shaders`

**Constraints**:
- Screen-space coordinates (not sprite-space UV) for the Bayer matrix modulo — see `Design/06 § Screen-Space vs Sprite-Space UVs`
- `FilterQuality.none` on all nearest-neighbor upscaling draw calls
- Palette colors (`uColorLight`, `uColorDark`) must be runtime-configurable uniforms, never hardcoded in GLSL
- Shader must compile under Impeller (AOT); test on both Android Impeller and fallback Skia

---

## test-agent

**Purpose**: Write and maintain the full test suite. Ensures every production artifact has verifiable acceptance criteria.

**Domain**:
- `test/unit/` — pure Dart unit tests for state notifiers, plugin logic, balance math
- `test/widget/` — Flutter widget tests for all components in `lib/core/widgets/` and feature screens
- `test/integration/` — end-to-end flows (feed kaiju → state update → UI re-render)

**Spec sources**: Any `Documentation/` file that defines behavior. GameDesign balance curves (`GameDesign/02`) define numeric assertions.

**Inputs from Architect**: The production file path to test, and the acceptance criteria from the delegating task.

**Outputs**: Test files mirroring the production directory structure under `test/`. Each test file maps 1:1 to a production file.

**Constraints**:
- No production code modifications — file bugs to the Architect if a unit is untestable
- Mock all Riverpod providers using `ProviderContainer` overrides
- Flame game components must be tested with `FlameGame.tester` (from `flame_test`)
- Shader tests are golden tests: compare rendered pixel output against reference images

---

## backend-agent

**Purpose**: Implement the Supabase backend: PostgreSQL schema, Row-Level Security policies, and Edge Functions.

> **PoC Note**: This agent is **inactive during Phase 1 (offline PoC)**. The Architect activates it at Phase 2 transition per `Documentation/Features/04-poc-scope-and-future-roadmap.md`.

**Domain**:
- `apps/backend/supabase/migrations/` — PostgreSQL DDL and RLS policies
- `apps/backend/supabase/functions/` — Deno Edge Functions (`verify-iap`, `sync-manifest`)

**Spec sources**:
- `Documentation/Architecture/04-backend-and-realtime.md`
- `Documentation/Architecture/05-database-and-auth.md`
- `Documentation/Plugins/05-backend-control-and-schemas.md`
- `Documentation/Payments/02-native-iap-architecture.md`
- `Documentation/Ownership/01-ownership-model-overview.md`

**Inputs from Architect**: The schema section or Edge Function spec to implement, plus the current migration baseline.

**Outputs**: Numbered migration SQL files and Deno TypeScript Edge Function source.

**Constraints**:
- Every table must have RLS enabled with explicit policies — no `SECURITY DEFINER` shortcuts
- IAP receipt validation must occur server-side only; client trust is forbidden
- All JSONB plugin manifest columns must validate against the schemas in `Plugins/05`

---

## Inter-Agent Communication Rules

1. **Agents do not communicate directly.** All coordination passes through the Architect.
2. **An agent's output becomes another agent's input only after Architect review.**
3. **Interface contracts** (e.g., the `DitheredViewport` widget API consumed by flutter-ui-agent) are defined by the Architect in writing before either dependent agent begins.
4. **Blocking dependencies** must be escalated to the Architect, not resolved unilaterally by an agent.
5. **Out-of-scope work** (e.g., flutter-ui-agent writing state logic) must be flagged and refused; the agent returns a scope violation notice to the Architect instead.
