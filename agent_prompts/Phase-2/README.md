# `agent_prompts/Phase-2/` — Cloud Backend, Dynamic Plugin Sync & Base Furniture Store

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md) and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the chained technical prompts for **Phase 2**:
- **Self-Hosted Supabase Backend & Security Hardening**: Docker Compose topology, PostgreSQL DDL (`profiles`, `groups`, `group_members`, `kaijus`, `active_group_kaijus`, `plugins`, `scenario_plugins`, `action_plugins`, `customization_plugins`), RLS policies (`get_user_group_ids`), and server-side timestamp/cooldown triggers.
- **Dynamic Plugin Manifest Sync**: Live syncing of `plugins`, `scenario_plugins`, `action_plugins`, and `customization_plugins` from Supabase + Realtime `public:plugins` channel updates (`city_destruction` autonomous work, `crush_tanks` event action).
- **Base Furniture Store & Placement (`FURNITURE` Customization Plugins)**: Purchasing and placing room furniture items that modify the **3 core stats** (`hunger`, `energy`, `happiness`), such as `BASIC_BED` and `CRUSHED_TANK_TOY`.
- **Kaiju Name Customization (`[ RENAME ]`)**: Customizing Kaiju names (`1–16` chars, `pet_name_history` → `kaiju_name_history`) synced to Supabase.

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Architecture/04-backend-and-realtime.md`](../../Documentation/Architecture/04-backend-and-realtime.md)
- [`Documentation/Architecture/05-database-and-auth.md`](../../Documentation/Architecture/05-database-and-auth.md)
- [`Documentation/Plugins/03-non-user-triggered-actions.md`](../../Documentation/Plugins/03-non-user-triggered-actions.md)
- [`Documentation/Plugins/05-backend-control-and-schemas.md`](../../Documentation/Plugins/05-backend-control-and-schemas.md)
- [`Documentation/Furniture/01-furniture-catalog-and-store.md`](../../Documentation/Furniture/01-furniture-catalog-and-store.md)
- [`Documentation/Furniture/02-furniture-data-model.md`](../../Documentation/Furniture/02-furniture-data-model.md)
- [`Documentation/Furniture/03-furniture-placement-and-rendering.md`](../../Documentation/Furniture/03-furniture-placement-and-rendering.md)
- [`Documentation/Customization/03-kaiju-name-customization.md`](../../Documentation/Customization/03-kaiju-name-customization.md)
- [`Documentation/Security/01-security-overview.md`](../../Documentation/Security/01-security-overview.md)
- [`Documentation/Security/02-supabase-self-hosted.md`](../../Documentation/Security/02-supabase-self-hosted.md)
- [`Documentation/Security/03-attack-prevention.md`](../../Documentation/Security/03-attack-prevention.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below:

1. **`01-supabase-schema-and-rls.md`** → Start at **Step 1** (PostgreSQL migrations, RLS policies, triggers, and seed data)
2. **`02-auth-and-cloud-state-sync.md`** → Supabase Auth (`flutter_secure_storage`), offline-to-cloud migration, and `active_group_kaijus` sync
3. **`03-remote-plugin-manifest-and-realtime.md`** → `pluginSyncProvider`, Realtime `PLUGIN_MANIFEST_UPDATED`, and `GenericAutonomousEvaluator`
4. **`04-base-furniture-store-and-placement.md`** → `STORE_MGR` Furniture Store UI, `user_furniture_inventory`, and room anchor rendering
5. **`05-kaiju-rename-and-phase2-tests.md`** → `[ RENAME ]` modal flow, integration tests, and mandatory `Documentation/` sync check

> **ENTRYPOINT FOR AGENT**: Begin at **`01-supabase-schema-and-rls.md` → Step 1** once the technical implementation files are added to this folder.
