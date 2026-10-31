# `agent_prompts/Phase-3/` — iOS Launch, Kaiju Aging, Extended Stats + Study Desk & Clinic Recovery

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md) and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the chained technical prompts for **Phase 3**:
- **iOS Build & Impeller Validation**: iOS target configuration, Metal/Impeller shader verification, and APNs setup.
- **Kaiju Lifecycle & Aging (`EVO_MGR`)**: `kaiju_lifecycle_config`, `age_in_days` progression, stage transitions (`Hatchling` → `Juvenile` → `Titan` → `Elder` → `Ancient`), and dynamic sprite/decay scaling.
- **Extended Stats (`extended_stats`) + Gated Furniture (`WORK_STN` / `itm_desk`)**:
  - Introduces `intel`, `comfort`, `hydration`, and `hp` in `kaijus.extended_stats`.
  - Ships the furniture items that modify or unlock those exact stats/actions alongside them — specifically **`WORK_STN` (`itm_desk`, Desktop & Chair)** which unlocks the `destruction_study` (`required_furniture: ["itm_desk"]`) plugin to raise `intel`.
- **Clinic Recovery (`hospital_recovery` / `hospital_bed`)**: Autonomous medical containment scenario triggered on severe exhaustion or low `hp`.

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Features/05-kaiju-lifecycle-and-aging.md`](../../Documentation/Features/05-kaiju-lifecycle-and-aging.md)
- [`Documentation/GameDesign/02-balance-curves-and-math.md`](../../Documentation/GameDesign/02-balance-curves-and-math.md)
- [`Documentation/Plugins/03-non-user-triggered-actions.md`](../../Documentation/Plugins/03-non-user-triggered-actions.md)
- [`Documentation/Furniture/01-furniture-catalog-and-store.md`](../../Documentation/Furniture/01-furniture-catalog-and-store.md)
- [`Documentation/DevOps/01-ci-cd-and-build-pipeline.md`](../../Documentation/DevOps/01-ci-cd-and-build-pipeline.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below:

1. **`01-ios-and-impeller-setup.md`** → Start at **Step 1** (iOS project config, shader verification, and CI build target)
2. **`02-kaiju-aging-and-lifecycle.md`** → `kaiju_lifecycle_config`, `age_progression` plugin, and live `EVO_MGR` screen
3. **`03-extended-stats-and-study-desk.md`** → `extended_stats` (`intel`, `comfort`, `hydration`, `hp`), `WORK_STN` (`itm_desk`) furniture plugin, and `destruction_study` (`required_furniture` check)
4. **`04-clinic-recovery-and-tests.md`** → `hospital_recovery` autonomous action, `hospital_bed` scenario, tests, and mandatory `Documentation/` sync check

> **ENTRYPOINT FOR AGENT**: Begin at **`01-ios-and-impeller-setup.md` → Step 1** once the technical implementation files are added to this folder.
