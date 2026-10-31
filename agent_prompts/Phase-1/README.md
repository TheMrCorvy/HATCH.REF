# `agent_prompts/Phase-1/` — Milestone 1.2: Late Phase 1 (Kaiju Exhaustion & Polish)

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md) and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the chained technical prompts for **Milestone 1.2 (Late Phase 1)**, immediately following the initial PoC:
- **Kaiju Exhaustion State (`statusFlags['is_exhausted']`)**:
  - When `hunger == 0` or `energy == 0`, the Kaiju transitions into a non-destructive **Exhausted** state (`is_exhausted = true`).
  - While exhausted, energy-consuming actions (`play`, work shifts) are disabled in `GenericUserActionExecutor`, the Kaiju renders its exhausted sprite/animation, and a terminal warning banner appears in `RoomScreen`.
  - Feeding (`eat`) and resting (`sleep`) until both `hunger >= 20` and `energy >= 20` clears `is_exhausted` back to `false`.

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Features/04-poc-scope-and-future-roadmap.md`](../../Documentation/Features/04-poc-scope-and-future-roadmap.md)
- [`Documentation/GameDesign/01-game-design-document.md`](../../Documentation/GameDesign/01-game-design-document.md)
- [`Documentation/GameDesign/02-balance-curves-and-math.md`](../../Documentation/GameDesign/02-balance-curves-and-math.md)
- [`Documentation/Architecture/06-offline-first-and-state.md`](../../Documentation/Architecture/06-offline-first-and-state.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below:

1. **`01-exhaustion-state-and-rules.md`** → Start at **Step 1** (`statusFlags['is_exhausted']` transitions in `KaijuStateNotifier` and action gating in `GenericUserActionExecutor`)
2. **`02-exhaustion-ui-and-tests.md`** → Terminal exhaustion banner, sprite state hookup, unit/widget tests, and mandatory `Documentation/` sync check

> **ENTRYPOINT FOR AGENT**: Begin at **`01-exhaustion-state-and-rules.md` → Step 1** once the technical implementation files are added to this folder.
