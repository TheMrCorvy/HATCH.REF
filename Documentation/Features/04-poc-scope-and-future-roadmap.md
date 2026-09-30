# Features: 04 PoC Scope and Future Roadmap

This document establishes the strict boundaries of the Initial Proof of Concept (PoC) versus the multi-phase product roadmap for the **Unix Tamagotchi**.

---

## 1. Scope Boundary Matrix

| Feature Domain | Included in Initial PoC | Deferred to Future Roadmap | Rationale |
| :--- | :---: | :---: | :--- |
| **Framework** | 🟢 **Flutter + Flame Engine** | — | Single codebase prevents costly migrations; Flame drives pet viewport. |
| **Plugin Subsystem** | 🟢 **3 core actions (Eat, Sleep, Play) hardcoded as plugins + Default Room scenario. Code structured for easy dynamic manifest swap.** | 🟡 Dynamic remote manifest sync | Validates modular action & scenario contracts early. |
| **Backend & Cloud** | 🔴 100% Offline (Local Hive) | 🟢 Supabase PostgreSQL & Realtime | Zero cloud infrastructure required on Day 1. |
| **Pet Capacity** | 🟢 **Dynamic (Credit-bound)** | 🟡 Backend-enforced quota limits | Avoids hardcoding arbitrary pet ceilings. |
| **Starting Economy** | 🟢 Fixed 240 Credits | 🟡 In-App Purchases, daily quests | Pre-calculates exact initial acquisition testing. |
| **Core Actions** | 🟢 Eat, Sleep, Play (As Plugins) | 🟡 Basketball, Relic Search, Careers | Core loop proven with zero friction. |
| **Scenarios** | 🟢 Default Room Plugin | 🟡 Hospital Bed, Sports Arena | Proves scenario viewport rendering. |
| **Pet Lifecycle** | 🟡 **Static UI teaser with mock data (EVO_MGR screen)** | 🟢 **Aging, Autonomous Work, Illness logic** | Keeps early state models minimal. |
| **Visual System** | 🟢 1-Bit Dithered Visual System | 🟡 Additional stippling effects | Proves the core dithering and terminal UI aesthetics. |
| **Social** | 🔴 Solo play only | 🟢 Collaborative Multiplayer Care | Delays complex state sync (couples, families, friends) to Phase 4. |
| **Furniture & Habitat** | 🟢 **Furniture Store, catalog, placement, and stat modifiers** | 🟡 **Advanced room layouts, seasonal furniture** | Core habitat customization validated early. |
| **Customization** | 🟢 **Room palette themes, boot messages** | 🟡 **Pet accessories, skins** | Per-user visual personalization. |
| **Ownership Model** | 🟢 **Solo-as-group-of-1 data model** | 🟡 **Multiplayer group creation UI** | Foundation for seamless solo ↔ multiplayer transition. |
| **iOS Platform** | 🔴 Excluded | — **Android-first for PoC. iOS deferred to future phase.** | Android-only reduces Day 1 complexity. |

---

## 2. Multi-Phase Product Roadmap

```mermaid
gantt
    title Unix Tamagotchi Product Roadmap
    dateFormat  YYYY-MM
    section Phase 1: Core Flutter & Flame PoC
    Flame Viewport & Dithering Shader :done, p1_1, 2026-09, 2026-10
    Eat / Sleep / Play Plugins       :done, p1_2, 2026-09, 2026-10
    Terminal UI Implementation       :done, p1_3, 2026-10, 2026-10
    Android & iOS Verification       :active, p1_4, 2026-10, 2026-11

    section Phase 2: Cloud & Dynamic Plugins
    Supabase DB & Plugin Tables      :p2_1, 2026-11, 2026-12
    Social Auth (Google/Apple)       :p2_2, 2026-12, 2027-01
    Remote Plugin Manifest Sync      :p2_3, 2027-01, 2027-02

    section Phase 3: Autonomous Actions
    Pet Aging & Career Studying      :p3_1, 2027-02, 2027-03
    Office Work Shift Plugin         :p3_2, 2027-03, 2027-04
    Hospital Bed Recovery Scenario   :p3_3, 2027-03, 2027-04

    section Phase 4: Multiplayer & IAP
    Multiplayer Group Creation       :p4_1, 2027-04, 2027-05
    Shared Pet Care Sync             :p4_2, 2027-05, 2027-06
    Flutter in_app_purchase          :p4_3, 2027-06, 2027-07
    Argentine SWIFT Repatriation     :p4_4, 2027-07, 2027-08
```
