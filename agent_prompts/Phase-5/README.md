# `agent_prompts/Phase-5/` — Minigame Plugins & Late-Stage Permanent Death (`ERR_SYS`)

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md) and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the chained technical prompts for **Phase 5+ (Late Roadmap)**:
- **Minigame Plugin Subsystem (`SOLO`, `SOLO_VS_PC`, `PVP` Async Ghost)**:
  - `minigame_plugins`, `minigame_sessions`, and `minigame_ghost_pool` tables.
  - `MinigamePlugin` engine, deterministic `GhostRecorder` / `GhostPlayer`, and Kaiju minigames (`stomp_skyscraper`, `atomic_sweep`, `skyline_demolition_race`).
- **Late-Stage Permanent Kaiju Death (`ERR_SYS`)**:
  - Pushed to the latest stage of the roadmap: crimson emergency palette (`#B72828`) `ERR_SYS // CRITICAL FAILURE DETECTED` screen when unrecovered critical failure timers expire.

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Plugins/Minigames/01-minigame-overview.md`](../../Documentation/Plugins/Minigames/01-minigame-overview.md)
- [`Documentation/Plugins/Minigames/02-session-lifecycle-and-categories.md`](../../Documentation/Plugins/Minigames/02-session-lifecycle-and-categories.md)
- [`Documentation/Plugins/Minigames/03-backend-schema-and-rewards.md`](../../Documentation/Plugins/Minigames/03-backend-schema-and-rewards.md)
- [`Documentation/Design/05-1bit-terminal-wireframes.md`](../../Documentation/Design/05-1bit-terminal-wireframes.md)
- [`Documentation/Features/04-poc-scope-and-future-roadmap.md`](../../Documentation/Features/04-poc-scope-and-future-roadmap.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below:

1. **`01-minigame-schema-and-engine.md`** → Start at **Step 1** (`minigame_plugins` DDL, `MinigameSessionNotifier`, `GhostRecorder`, and `GhostPlayer`)
2. **`02-kaiju-minigames-implementation.md`** → `stomp_skyscraper` (`SOLO`), `atomic_sweep` (`SOLO_VS_PC`), and `skyline_demolition_race` (`PVP` Ghost)
3. **`03-err-sys-critical-failure-and-tests.md`** → `ERR_SYS` crimson emergency screen, end-to-end tests, and mandatory `Documentation/` sync check

> **ENTRYPOINT FOR AGENT**: Begin at **`01-err-sys-and-minigame-schema.md` / `01-minigame-schema-and-engine.md` → Step 1** once the technical implementation files are added to this folder.
