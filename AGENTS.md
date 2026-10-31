# AGENTS.md — Universal Agent Protocol & Roster

> **Methodology**: **AI-First, Human-in-the-Loop**.  
> **Harness-Agnostic**: These rules apply to **every AI agent and harness** that touches this repository — including **Claude Code / Claude Opus**, **Google Antigravity (AGY CLI / IDE)**, **Devin**, **Hermes**, **Cursor**, **Windsurf**, or any custom agent runner.

---

## Universal Laws (Mandatory for Every Agent)

### Law 1: `Documentation/` is the Single Source of Truth
The `Documentation/` directory is the canonical, living specification of the **Unix Tamagotchi** project. The codebase must strictly mirror `Documentation/` at all times, and `Documentation/` must strictly mirror the codebase.

- **Before writing or modifying code**: Always read the corresponding specification in `Documentation/<Domain>/`. Never guess or invent unapproved behavior.
- **Whenever anything changes or deviates**: At **any moment** that a bug is fixed, a technical constraint changes, an edge case is discovered, or something is implemented that diverges from or is not yet covered by `Documentation/`, **you MUST update the corresponding file(s) in `Documentation/` in the exact same task/commit**.
- **Zero Drift Tolerance**: Leaving a code change, schema tweak, or bugfix undocumented — or fixing code in a way that contradicts `Documentation/` without updating `Documentation/` — is a critical protocol violation.

### Law 2: AI-First, Human-in-the-Loop
- This project is built using an **AI-First, Human-in-the-Loop** workflow.
- Every architectural decision, prompt chain, schema change, and technical tradeoff must be explicitly documented in Markdown so that the human operator can review it and any future AI model (regardless of vendor or harness) can pick up the exact context with zero ambiguity.
- If a requirement is ambiguous, contradictory, or requires a product decision not covered in `Documentation/`, pause and ask the human operator before guessing.

### Law 3: The `agent_prompts/` Chained Execution Protocol
All implementation plans, phase rollouts, and bugfix instructions passed to AI models live in the root `agent_prompts/` directory.

1. **Folder Organization**:
   - `agent_prompts/PoC/` — Milestone 1.1: Initial PoC (Android offline, 3 core stats, 3 direct actions, `default_room`, Kaiju Store, Kaiju Switcher, Palette/Boot-Message customization, local JSON manifest).
   - `agent_prompts/Phase-1/` — Milestone 1.2: Late Phase 1 (Kaiju Exhaustion state when vital stats reach `0` and offline polish).
   - `agent_prompts/Phase-2/` — Cloud Backend (Self-hosted Supabase, Auth, dynamic plugin manifest sync, base Furniture Store for core stats, Kaiju rename).
   - `agent_prompts/Phase-3/` — iOS Launch, Kaiju Aging, Extended Stats (`INTEL`, `COMFORT`, `HYDRATION`, `HP`) + gated furniture (`WORK_STN` / `itm_desk`), and Clinic Recovery (`hospital_recovery`).
   - `agent_prompts/Phase-4/` — Multiplayer Shared Care (`COUPLE` & `FRIENDS` groups, per-group active Kaiju, first-time physical NFC/BLE phone-touch pairing + single-use fallback code) & Native IAP.
   - `agent_prompts/Phase-5/` — Minigame Plugins (`stomp_skyscraper`, `atomic_sweep`, `skyline_demolition_race`) & Late-stage Permanent Death (`ERR_SYS`).
   - `agent_prompts/Bugfix-<feature-name>/` — Dedicated folder for any bugfix or post-implementation adjustment.

2. **Inside Each `agent_prompts/<Folder>/` (The Chained Prompt Structure)**:
   - **One `README.md` (The Entrypoint Guide)**:
     - Explains the high-level objective of what needs to be implemented or fixed.
     - Lists the authoritative `Documentation/` files that govern the work.
     - Defines the **Ordered Execution Chain**, pointing the agent to the first technical implementation file and its first step (`README.md` → `Implementation File 1, Step 1`).
   - **Technical Implementation `.md` Files**:
     - Contain the hardcore technical specifications: exact file paths, code blocks, diffs, SQL migrations, shader code, and test commands.
     - May have any descriptive filename (e.g., `01-theme-and-widgets.md`, `02-dither-shader-pipeline.md`), provided `README.md` indexes all of them.
     - **Strict Step-to-Step Chaining**: Every step inside an implementation file must end with an explicit pointer to the next step:
       ```text
       README.md
         └──► [Implementation File 1] -> Step 1
                └──► [Implementation File 1] -> Step 2
                       └──► [Implementation File 2] -> Step 1
                              └──► ...
                                     └──► Final Step: Verification & Documentation/ Sync Check
       ```
   - **Mandatory Final Step**: Every prompt chain in `agent_prompts/<Folder>/` must conclude with a **Documentation Sync & Verification Step** where the agent verifies that `Documentation/` accurately reflects everything that was built or modified.

---

## Documentation Structure Rule

All project specifications must be stored in `Documentation/` using **one subfolder per game domain**. Agents must write any new spec documents or updates to the correct folder before or alongside implementation. Placing documentation in the wrong folder, or creating a generic catch-all file at the `Documentation/` root, is a scope violation.

| Folder | Game Domain |
| :--- | :--- |
| `Architecture/` | System topology, framework decisions, monorepo layout, backend design, offline state |
| `Design/` | Visual system, widget library, screen flows, wireframes, shader/rendering pipeline |
| `Features/` | Player-facing feature specs and PoC/Phase scope boundaries |
| `Plugins/` | Data-driven plugin engine contracts (bundles, scenarios, user actions, auto actions, customizations, minigames) |
| `GameDesign/` | Balance curves, stat math, economy, progression, progressive failure states |
| `Furniture/` | Furniture catalog, data model, placement, progressive stat modifiers |
| `Multiplayer/` | Shared kaiju care (Couples & Friends), group types, one-time physical pairing, real-time sync |
| `Ownership/` | Unified ownership model (`SOLO`, `COUPLE`, `FRIENDS`), group lifecycle, solo ↔ group transitions |
| `Payments/` | IAP, store compliance, payout rules, anti-cheat |
| `DevOps/` | CI/CD, build pipeline, release process |
| `Contracts/` | OpenAPI spec, WebSocket AsyncAPI events |
| `Customization/` | Per-user and group-scoped personalization (palettes, boot messages, clothing, rename) |
| `NameGeneration/` | Automated JoJo-inspired kaiju naming pools and token-bank composition |
| `Notifications/` | FCM/APNs push notification architecture and partner/group alerts |
| `Security/` | Client/backend security hardening, self-hosted Supabase Docker setup, attack prevention |

When an agent produces a research report, a bugfix root-cause change, or a design decision that must persist, it must be committed to the matching `Documentation/<folder>/` — never left solely in code comments or commit messages.

---

## Domain Roles & Agent Index

Whether an AI harness uses multi-agent delegation (e.g., an Architect agent spawning subagents) or a single agent executing steps sequentially from `agent_prompts/`, work is logically partitioned into the following six specialized domains:

| Role / Agent | Domain | Primary Output |
| :--- | :--- | :--- |
| [`research-agent`](#research-agent) | Package APIs, Flutter internals, unknown patterns | Research reports in `Documentation/`, API usage examples |
| [`flutter-ui-agent`](#flutter-ui-agent) | Terminal widgets, design system, screen layouts | `lib/core/widgets/`, `lib/core/theme/`, `lib/features/*/view/` |
| [`flutter-impl-agent`](#flutter-impl-agent) | Business logic, state, generic plugins, navigation | `lib/state/`, `lib/plugins/`, `lib/features/*/logic/` |
| [`shader-agent`](#shader-agent) | GLSL shaders, Flame integration, dithering pipeline | `assets/shaders/`, `lib/core/dither_engine/` |
| [`test-agent`](#test-agent) | Unit, widget, and integration tests | `test/` |
| [`backend-agent`](#backend-agent) | Supabase schema, RLS, Edge Functions | `apps/backend/supabase/` |

---

## research-agent

**Purpose**: Resolve technical unknowns before implementation begins. Prevents agents from inventing APIs or guessing behavior.

**Triggers**: Executed when:
- A `Documentation/` gap is identified (see `CLAUDE.md § Known Implementation Gaps`)
- A package API needs validation against the current pub.dev version
- A Flutter/Flame internal behavior is uncertain (e.g., Impeller shader compilation, `SnapshotWidget` API)
- A new package is proposed and must be evaluated against `Architecture/02`

**Inputs**: A specific question, a documentation section, and optionally a pub.dev package name.

**Outputs**: A concise written report committed to `Documentation/` containing:
- The verified API signature or behavior
- A minimal runnable code example
- Any platform caveats (iOS vs Android, Impeller vs Skia)
- A recommendation and corresponding update to the relevant `Documentation/` spec

**Constraints**:
- Must cite the actual package version tested (e.g., `flame: ^1.18.0`)
- Must flag any deviation from the locked stack in `CLAUDE.md § Non-Negotiable Technical Constraints`

---

## flutter-ui-agent

**Purpose**: Implement all visual Flutter widgets and screen layouts that do not contain business logic or state mutations.

**Domain**:
- `lib/core/theme/` — palette tokens, typography (`VT323`), box decorations
- `lib/core/widgets/` — `HazardStripe`, `BracketButton`, `TerminalBorder`, `StatusBar`, `DottedDivider`, `ProgressBar`
- `lib/features/*/view/` — screen scaffold and layout (StatelessWidget or UI-only StatefulWidget)

**Spec sources**:
- `Documentation/Design/01-design-system-and-theming.md`
- `Documentation/Design/02-terminal-component-library.md`
- `Documentation/Design/04-screens-flow-and-navigation.md`
- `Documentation/Design/05-1bit-terminal-wireframes.md`

**Outputs**: Production-ready Dart widget files. No hardcoded colors (use theme/palette tokens). No business logic. No direct Riverpod reads beyond `ref.watch` on display-only providers.

**Constraints**:
- Font must always come from `google_fonts` (`VT323`)
- All colors must reference `Theme.of(context)` / `AppPalette` tokens so `PALETTE` customization plugins apply dynamically
- No `setState` for data that belongs in Riverpod state
- `FilterQuality.none` on any image that renders pixel art

---

## flutter-impl-agent

**Purpose**: Implement business logic, Riverpod state notifiers, generic data-driven plugin interpreters, and navigation.

**Domain**:
- `lib/state/` — `KaijuStateNotifier`, `InventoryNotifier`, `CreditsNotifier`
- `lib/plugins/` — generic data-driven plugin registry, manifest parser, and generic executors (`GenericUserActionExecutor`, `GenericAutonomousEvaluator`, `GenericScenarioBuilder`, `GenericCustomizationRenderer`)
- `lib/features/*/logic/` — feature-level controllers and use-case classes
- `lib/app.dart` — router configuration (`go_router` or `Navigator`)

**Spec sources**:
- `Documentation/Architecture/01-system-overview.md`
- `Documentation/Architecture/06-offline-first-and-state.md`
- `Documentation/Plugins/01-plugin-architecture-overview.md`
- `Documentation/Plugins/02-user-triggered-actions.md`
- `Documentation/Plugins/03-non-user-triggered-actions.md`
- `Documentation/Plugins/04-scenarios-and-environments.md`
- `Documentation/Features/01-core-kaiju-actions.md`
- `Documentation/Features/02-kaiju-store-and-credits.md`
- `Documentation/Features/03-kaiju-inventory-and-switching.md`
- `Documentation/GameDesign/02-balance-curves-and-math.md`

**Outputs**: Dart source files for state notifiers, generic plugin executors, and feature logic. Must be testable (no hard dependencies — use Riverpod providers for injection).

**Constraints**:
- All state must be immutable (`freezed` records or `copyWith`)
- Hive adapters required for any persisted model
- No direct `BuildContext` access in notifiers or plugins
- Strictly respect phase boundaries defined in `Documentation/Features/04-poc-scope-and-future-roadmap.md`

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

**Prerequisite**: All three shader gaps listed in `CLAUDE.md § Known Implementation Gaps` must be resolved and documented in `Documentation/Design/06-1bit-dithering-rendering-pipeline.md` before or during Step 1 of shader implementation.

**Outputs**:
- `assets/shaders/bayer_dither.frag` — GLSL shader with `uTexture`, `uResolution`, `uColorLight`, `uColorDark` uniforms
- `lib/core/dither_engine/kaiju_game.dart` — `FlameGame` subclass that renders the kaiju scene
- `lib/core/dither_engine/dithered_viewport.dart` — Flutter widget that composites the Flame game through the Bayer shader
- `pubspec.yaml` update: shader file registered under `flutter.shaders`

**Constraints**:
- Screen-space coordinates (not sprite-space UV) for the Bayer matrix modulo — see `Design/06 § Screen-Space vs Sprite-Space UVs`
- `FilterQuality.none` on all nearest-neighbor upscaling draw calls
- Palette colors (`uColorLight`, `uColorDark`) must be runtime-configurable uniforms driven by the active `PALETTE` customization plugin, never hardcoded in GLSL
- Shader must compile under Impeller (AOT); test on both Android Impeller and fallback Skia

---

## test-agent

**Purpose**: Write and maintain the full test suite. Ensures every production artifact has verifiable acceptance criteria.

**Domain**:
- `test/unit/` — pure Dart unit tests for state notifiers, generic plugin executors, balance math
- `test/widget/` — Flutter widget tests for all components in `lib/core/widgets/` and feature screens
- `test/integration/` — end-to-end flows (feed kaiju → state update → UI re-render)

**Spec sources**: Any `Documentation/` file that defines behavior. GameDesign balance curves (`GameDesign/02`) define numeric assertions.

**Outputs**: Test files mirroring the production directory structure under `test/`. Each test file maps 1:1 to a production file.

**Constraints**:
- Mock all Riverpod providers using `ProviderContainer` overrides
- Flame game components must be tested with `FlameGame.tester` (from `flame_test`)
- Shader tests are golden tests: compare rendered pixel output against reference images

---

## backend-agent

**Purpose**: Implement the Supabase backend: PostgreSQL schema, Row-Level Security policies, and Edge Functions.

> **Phase Note**: This domain is **inactive during `PoC` and `Phase-1` (offline)**. It activates at `Phase-2` per `Documentation/Features/04-poc-scope-and-future-roadmap.md`.

**Domain**:
- `apps/backend/supabase/migrations/` — PostgreSQL DDL and RLS policies
- `apps/backend/supabase/functions/` — Deno Edge Functions (`verify-iap`, `sync-manifest`)

**Spec sources**:
- `Documentation/Architecture/04-backend-and-realtime.md`
- `Documentation/Architecture/05-database-and-auth.md`
- `Documentation/Plugins/05-backend-control-and-schemas.md`
- `Documentation/Payments/02-native-iap-architecture.md`
- `Documentation/Ownership/01-ownership-model-overview.md`
- `Documentation/Security/01-security-overview.md`

**Outputs**: Numbered migration SQL files and Deno TypeScript Edge Function source.

**Constraints**:
- Every table must have RLS enabled with explicit policies (using `public.get_user_group_ids(auth.uid())` for group membership checks)
- IAP receipt validation must occur server-side only; client trust is forbidden
- All JSONB plugin manifest columns must validate against the schemas in `Plugins/05`

---

## Inter-Agent & Multi-Harness Coordination Rules

1. **`Documentation/` is the Contract**: All handoffs between agents, prompts, or sessions are governed by `Documentation/`. If an interface contract changes during implementation, `Documentation/` must be updated immediately.
2. **Follow `agent_prompts/` in Order**: When executing a folder in `agent_prompts/`, always start at that folder's `README.md` and follow the chained steps in exact sequential order (`README.md` → `File 1, Step 1` → `File 1, Step 2` → `File 2, Step 1` → ...).
3. **Never Leave Undocumented Fixes**: If a bug is found or fixed (whether during a phase rollout or in a `Bugfix-<feature-name>` prompt), update the corresponding `Documentation/` file in the same turn/commit.
