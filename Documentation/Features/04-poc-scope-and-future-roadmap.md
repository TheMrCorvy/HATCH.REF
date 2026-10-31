# Features: 04 PoC Scope and Future Roadmap

This document establishes the strict boundaries of the Initial Proof of Concept (PoC) versus the multi-phase product roadmap for the **Unix Tamagotchi**.

---

## 1. Scope Boundary Matrix

| Feature Domain | Included in Initial PoC (Milestone 1.1) | Deferred to Post-PoC Phases | Rationale |
| :--- | :---: | :---: | :--- |
| **Framework** | 🟢 **Flutter + Flame Engine** | — | Single codebase prevents costly migrations; Flame drives kaiju viewport. |
| **Plugin Subsystem** | 🟢 **100% generic data-driven frontend engine reading bundled PoC JSON manifest (`eat`, `sleep`, `play`, `default_room`, palettes)** | 🟡 **Phase 2+**: Remote backend plugin bundles (scenarios, actions, auto-actions, customizations) | Frontend is purely data-driven from Day 1 so product team can add events/features in Phase 2+ with zero code changes. |
| **Backend & Cloud** | 🔴 100% Offline (Local Hive) | 🟢 **Phase 2+**: Supabase PostgreSQL, Storage & Realtime | Zero cloud infrastructure required on Day 1. |
| **Kaiju Stats** | 🟢 **3 Core Stats only (`Hunger`, `Energy`, `Happiness`)** | 🟢 **Phase 3+**: Extended stats (`INTEL`, `COMFORT`, `HYDRATION`, `HP`, `LUME`) | Extra stats ship only when their paired actions and furniture are implemented. |
| **Failure / Recovery States** | 🔴 **None (Stats clamp at 0)** | 🟡 **Milestone 1.2**: Exhaustion state<br>🟢 **Phase 3**: Clinic Recovery (`hospital_recovery`)<br>🔴 **Phase 5+**: Permanent Death (`ERR_SYS`, pushed as late as possible) | Keeps initial PoC stress-free while progressively introducing stakes. |
| **Kaiju Capacity** | 🟢 **Unbounded (Credit-bound only — no server quota)** | — | Players may own as many kaijus as their credits allow. No backend limit field exists. |
| **Starting Economy** | 🟢 Fixed 240 Credits | 🟡 **Phase 3**: Autonomous work payouts<br>🟢 **Phase 4**: In-App Purchases | Pre-calculates exact initial acquisition testing. |
| **Core Actions** | 🟢 Eat, Sleep, Play (Data-driven plugins) | 🟡 **Phase 2+**: Event actions (`Crush Tanks`)<br>🟢 **Phase 3**: `Demolition Study`, `City Rampage` shifts | Core loop proven with zero friction. |
| **Scenarios** | 🟢 Default Room Scenario | 🟡 **Phase 2/3+**: Metropolis Ruins, Clinic Recovery Ward | Proves generic scenario layer rendering. |
| **Kaiju Lifecycle** | 🟡 **Static UI teaser with mock data (`EVO_MGR` screen)** | 🟢 **Phase 3**: 5-phase Aging, Autonomous Work & Study, Illness logic | Keeps early state models minimal. |
| **Visual System** | 🟢 1-Bit Dithered Visual System | 🟡 Additional stippling effects | Proves the core dithering and terminal UI aesthetics. |
| **Social & Multiplayer** | 🔴 Solo play only | 🟢 **Phase 4**: Collaborative Multiplayer Care for **Couples (`COUPLE`) & Friends (`FRIENDS`)** | Flagship selling point launched in Phase 4 with one-time phone-touch pairing + single-use invite code fallback. |
| **Furniture & Habitat** | 🔴 **Excluded** | 🟢 **Phase 2**: Base furniture (for 3 core stats)<br>🟢 **Phase 3**: Stat/Action-paired furniture (e.g. Desk & Chair `WORK_STN` for Study/`INTEL`) | Furniture that modifies or gates a specific stat is implemented only when that stat is implemented. |
| **Consumable Item Bags** | 🔴 **Excluded** | 🔴 Deferred (actions execute directly without item bag management) | Avoids inventory bloat; actions are direct plugin buttons. |
| **Customization** | 🟢 **Room palette themes, boot messages** | 🟡 **Phase 2+**: Kaiju clothing/accessories, skins, manual rename | Per-user and group-scoped visual personalization via customization plugins. |
| **Ownership Model** | 🟢 **Solo-as-group-of-1 data model** | 🟢 **Phase 4**: `COUPLE` & `FRIENDS` group transitions & per-group active Kaiju | Foundation for seamless solo ↔ multiplayer transition. |
| **iOS Platform** | 🔴 Excluded | 🟢 **Phase 3** — before Couple & Friends Mode | Android-first for PoC. iOS ships in Phase 3 before multiplayer launch. |

---

## 2. Multi-Phase Product Roadmap

```mermaid
gantt
    title Unix Tamagotchi Product Roadmap
    dateFormat  YYYY-MM
    section Phase 1: Core Flutter & Flame Foundation (Offline)
    Milestone 1.1 - Flame Viewport & Dithering Shader      :done, p1_1, 2026-09, 2026-10
    Milestone 1.1 - Generic Data-Driven Plugin Engine (PoC) :done, p1_2, 2026-09, 2026-10
    Milestone 1.1 - Terminal UI, Store & Palette Custom     :done, p1_3, 2026-10, 2026-11
    Milestone 1.2 - Kaiju Exhaustion State (Zero-Stat Lock) :active, p1_4, 2026-11, 2026-12

    section Phase 2: Cloud Backend, Dynamic Plugins & Base Customizations
    Supabase DB & Unified Plugin Bundle Tables              :p2_1, 2026-12, 2027-01
    Social Auth (Google/Apple) & Manual Rename              :p2_2, 2027-01, 2027-02
    Remote Plugin Manifest Sync & Base Furniture/Clothing   :p2_3, 2027-02, 2027-03

    section Phase 3: iOS, Lifecycle, Extended Stats & Autonomous Actions
    iOS Platform Support                                    :p3_0, 2027-03, 2027-04
    5-Phase Kaiju Aging & Extended Stats (INTEL, COMFORT)   :p3_1, 2027-04, 2027-05
    Study Furniture (Desk/Chair) & Demolition Study Plugin  :p3_2, 2027-05, 2027-06
    City Destruction Work & Clinic Recovery Scenario        :p3_3, 2027-05, 2027-06

    section Phase 4: Couple & Friends Mode (Flagship) & IAP
    Couple & Friends Mode — One-Time Touch Pairing + Codes  :crit, p4_0, 2027-06, 2027-07
    Couple Anniversaries & Group Milestones                 :crit, p4_1, 2027-07, 2027-08
    Shared Kaiju Care Realtime Sync (Per-Group Active Kaiju):crit, p4_2, 2027-08, 2027-09
    Flutter in_app_purchase & Argentine SWIFT Repatriation  :p4_3, 2027-09, 2027-10

    section Phase 5+: Post-Launch Expansions
    Minigame Plugins (SOLO, SOLO_VS_PC, PVP Ghost)          :p5_1, 2027-10, 2027-12
    Optional Critical Failure / Permanent Death (ERR_SYS)   :p5_2, 2027-12, 2028-01
```
