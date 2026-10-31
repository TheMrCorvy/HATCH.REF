# CLAUDE.md — Architect & Universal Agent Instructions

> **Methodology**: **AI-First, Human-in-the-Loop**.  
> **Universal Applicability**: While named `CLAUDE.md` for automatic ingestion by Claude harnesses, this file and [`AGENTS.md`](AGENTS.md) govern **every AI agent and harness** working on this repository (Claude Code, Google Antigravity CLI/IDE, Devin, Hermes, Cursor, etc.).

---

## 1. Golden Rules for Every Agent

1. **`Documentation/` is the Single Source of Truth**:
   - Everything built in the codebase must strictly mirror `Documentation/`.
   - **Mandatory Sync Rule**: At any moment that something has to be fixed, adjusted, or implemented in a way that differs from or is not yet covered by `Documentation/`, **you MUST update the relevant Markdown file(s) inside `Documentation/` alongside the code change**. Never allow the codebase and `Documentation/` to drift apart.
2. **Follow the `agent_prompts/` Chained Execution Protocol**:
   - All implementation prompts for features, phases, and bugfixes live in [`agent_prompts/`](agent_prompts/README.md).
   - Each subfolder (`PoC/`, `Phase-1/`, `Phase-2/`, `Phase-3/`, `Phase-4/`, `Phase-5/`, `Bugfix-<feature-name>/`) contains one `README.md` entrypoint guide and one or more technical `.md` files.
   - Always begin by reading the subfolder's `README.md`, which points to **Implementation File 1, Step 1**, and follow the explicit step-by-step chain (`README.md` → `File 1, Step 1` → `File 1, Step 2` → `File 2, Step 1` → ... → `Final Verification & Documentation Sync`).
3. **Human-in-the-Loop Clarity**:
   - Keep all documentation, prompt chains, and architectural decisions clean, explicit, and well-structured so the human operator can inspect, steer, and hand off tasks across different AI models effortlessly.

---

## 2. Project Identity & Repository Layout

**Unix Tamagotchi** is a Flutter + Flame mobile Kaiju-Tamagotchi game with a "Tactical 1-Bit Cyber-Specimen OS" aesthetic. Its main selling point is **online multiplayer shared Kaiju care for Couples (`COUPLE`) and Friends (`FRIENDS`)**, alongside Solo (`SOLO`) play, powered by a **100% generic, data-driven plugin engine**.

```text
tamagotchi/
├── CLAUDE.md              ← Architect & universal agent instructions (you are here)
├── AGENTS.md              ← Universal agent laws, domain roster, and capability map
├── agent_prompts/         ← Chained implementation prompts for AI models (by Phase / Bugfix)
│   ├── README.md          ← Master guide & rules for authoring/executing agent prompts
│   ├── PoC/               ← Milestone 1.1: Initial offline PoC prompts
│   ├── Phase-1/           ← Milestone 1.2: Late Phase 1 (Kaiju Exhaustion) prompts
│   ├── Phase-2/           ← Phase 2: Supabase Cloud, Plugin Sync, Base Furniture Store
│   ├── Phase-3/           ← Phase 3: iOS, Aging, Extended Stats + Study Desk, Clinic
│   ├── Phase-4/           ← Phase 4: Couple & Friends Shared Care + Touch Pairing + IAP
│   ├── Phase-5/           ← Phase 5+: Minigame Plugins & Late-Stage Permanent Death
│   └── _templates/        ← Reusable template for Bugfix-<feature-name> & new phases
└── Documentation/         ← Single Source of Truth: all design decisions, contracts, and specs
    ├── Architecture/
    ├── Contracts/
    ├── Customization/
    ├── Design/
    ├── DevOps/
    ├── Features/
    ├── Furniture/
    ├── GameDesign/
    ├── Multiplayer/
    ├── NameGeneration/
    ├── Notifications/
    ├── Ownership/
    ├── Payments/
    ├── Plugins/
    └── Security/
```

### Documentation Folder Rule

Every specification document must live in the `Documentation/` subfolder that matches the game domain it describes. No cross-domain catch-all files. When a new spec is needed or an existing behavior changes, update the matching folder before or alongside implementation:

| Folder | Covers |
| :--- | :--- |
| `Architecture/` | System topology, framework choices, monorepo layout, backend design, state architecture |
| `Design/` | Visual system, widget library, screen flows, wireframes, shader/rendering pipeline |
| `Features/` | Functional specs for player-facing features and PoC/Phase scope boundaries |
| `Plugins/` | Data-driven plugin engine contracts (bundles, scenarios, user actions, autonomous actions, customizations, minigames) |
| `GameDesign/` | Game balance, stat curves, economy math, progression rules, progressive failure states |
| `Furniture/` | Furniture catalog, data model, placement rules, progressive stat modifiers |
| `Multiplayer/` | Shared kaiju care architecture (Couples & Friends), group types, one-time touch pairing, real-time sync |
| `Ownership/` | Unified group ownership model (`SOLO`, `COUPLE`, `FRIENDS`), dissolution, solo ↔ group transitions |
| `Payments/` | IAP architecture, store compliance, payout rules, anti-cheat |
| `DevOps/` | CI/CD pipelines, build and release process |
| `Contracts/` | OpenAPI spec, WebSocket AsyncAPI events |
| `Customization/` | Per-user and group-scoped customizations (palettes, boot messages, clothing, rename) |
| `NameGeneration/` | Automated JoJo-inspired kaiju naming pools and token-bank composition |
| `Notifications/` | FCM/APNs push notification architecture and partner/group alerts |
| `Security/` | Client/backend security hardening, self-hosted Supabase Docker setup, attack prevention |

> **If a document spans two domains, split it.** Create one file per domain and cross-reference with a relative link.

---

## 3. Architect & Agent Responsibilities

1. **Read before implementing or delegating.** Always load the relevant `Documentation/` file and the active `agent_prompts/<Phase>/README.md` before writing code. Never invent specs.
2. **Enforce technical decisions.** The stack is locked: Flutter 3.x + Flame + Riverpod + Hive + Supabase. Do not re-evaluate framework choices — see `Documentation/Architecture/02-technology-stack-evaluation.md`.
3. **Sequence dependencies correctly.** Follow the chained step order in `agent_prompts/<Phase>/README.md`. Do not start a downstream step until its prerequisite step and spec doc are in place.
4. **Keep `Documentation/` synchronized.** If an implementation reveals a bug, a missing field, or a better technical pattern, update `Documentation/<Domain>/` immediately so the documentation remains the Single Source of Truth.

---

## 4. Canonical Work Sequence

Follow this order for each feature module or phase prompt chain:

```text
1. RESEARCH    → Validate package APIs and resolve unknowns in Documentation/
2. DESIGN      → Scaffold terminal widget structure against wireframes & palette tokens
3. IMPLEMENT   → Write Riverpod state notifiers and generic data-driven plugin executors
4. SHADER      → Implement GLSL FragmentProgram and Flame viewport compositing
5. TEST        → Write unit + widget + integration tests
6. DOC SYNC    → Verify output against Documentation/ and update specs if any detail changed
```

---

## 5. Non-Negotiable Technical Constraints

These decisions are final. Do not re-open them without explicit human approval.

| Constraint | Value | Source |
| :--- | :--- | :--- |
| UI framework | Flutter 3.x + Dart 3 | `Architecture/02` |
| Game engine | Flame 1.x (`flame` pub.dev) | `Architecture/02` |
| State management | Riverpod 2.5+ (`flutter_riverpod`) | `Architecture/02` |
| Local storage | Hive (`hive_flutter`) | `Architecture/02` |
| Backend (Phase 2+) | Self-hosted Supabase (`supabase_flutter`) | `Architecture/02`, `Security/02` |
| Font | VT323 via `google_fonts` | `Design/01` |
| Dithering algorithm | Ordered 4×4 Bayer matrix (screen-space) | `Design/06` |
| Shader registration | Must declare in `pubspec.yaml` under `flutter.shaders` | `Design/06` |
| Upscaling | `FilterQuality.none` (nearest-neighbor) | `Design/06` |
| Shader texture binding | `shader.setImageSampler(index, image)` | `Design/06` |
| PoC platform | Android-only (`PoC` & `Phase-1`); iOS in `Phase-3` | `Features/04` |
| PoC backend | 100% offline (Hive + local JSON manifest); Supabase in `Phase-2` | `Features/04` |

---

## 6. Known Implementation Gaps to Resolve in PoC Shader Research

These gaps are flagged in `Design/06` and must be resolved and documented in `Documentation/Design/06-1bit-dithering-rendering-pipeline.md` during Step 1 of the shader pipeline work:

1. **`uTexture` sampler wiring** — Define the exact `SnapshotWidget` or Flame post-process `setImageSampler(0, image)` wiring.
2. **Impeller compatibility** — Ensure all `.frag` shaders are registered under `flutter.shaders` in `pubspec.yaml` for Impeller AOT compilation.
3. **Off-screen render-to-texture** — Document the exact mechanism for passing the low-res Flame viewport output as `uTexture` to `bayer_dither.frag`.

---

## 7. Phase & Milestone Checklist Overview

### `agent_prompts/PoC/` — Milestone 1.1 (Initial Offline PoC)
Everything in the frontend plugin layer must be **100% generic and data-driven**, reading from `assets/manifests/poc_default_manifest.json`.
- [ ] Design system & dynamic palette theme (`lib/core/theme/`)
- [ ] Terminal widget library (`lib/core/widgets/`)
- [ ] Bayer dither shader + Flame integration (`lib/core/dither_engine/`)
- [ ] Kaiju sprite engine (`lib/core/sprite_engine/`)
- [ ] Riverpod state: `KaijuStateNotifier`, `InventoryNotifier` (3 core stats only: `hunger`, `energy`, `happiness`)
- [ ] Generic data-driven plugin engine + local PoC JSON manifest (`eat`, `sleep`, `play` actions; `default_room` scenario; palette presets)
- [ ] Screen: Containment Room (viewport + dynamic action bar)
- [ ] Screen: Kaiju Switcher / Specimen Roster (`SWAP_MGR`)
- [ ] Screen: Kaiju Store (240 starting credits, auto-generated JoJo-inspired designations)
- [ ] Screen: Evolution History (static mock teaser — `EVO_MGR`)
- [ ] Screen: Settings / Diagnostics & Palette/Boot-Message Customization (`CONF`)
- [ ] Full test suite (unit + widget + integration)

### Subsequent Phases in `agent_prompts/`
- **`agent_prompts/Phase-1/` (Milestone 1.2)**: Kaiju Exhaustion state when vital stats hit `0` + offline polish.
- **`agent_prompts/Phase-2/`**: Self-hosted Supabase backend, Auth, dynamic plugin manifest sync, base Furniture Store (core stats), Kaiju rename.
- **`agent_prompts/Phase-3/`**: iOS build, Kaiju Aging, Extended Stats (`INTEL`, `COMFORT`, `HYDRATION`, `HP`) + gated furniture (`WORK_STN` / `itm_desk`), Clinic Recovery (`hospital_recovery`).
- **`agent_prompts/Phase-4/`**: Multiplayer Shared Care (`COUPLE` & `FRIENDS` groups, shared active Kaiju per group, first-time physical NFC/BLE phone-touch pairing + single-use fallback code) & Native IAP.
- **`agent_prompts/Phase-5/`**: Minigame Plugins (`stomp_skyscraper`, `atomic_sweep`, `skyline_demolition_race`) & Late-stage Permanent Death (`ERR_SYS`).
