# Furniture: 01 Catalog & Store

## 1. Store UI Specification

The Furniture Store module (accessible via `STORE_MGR // FURNITURE.DAT`) adheres strictly to the **Unix Tamagotchi** tactical 1-bit dithered pixel art aesthetic. The UI utilizes VT323 monospace typography, blocky layout structures, hazard caution stripes, and bracketed action buttons `[ ACTION ]`. 

> [!NOTE] 
> The UI must convey an industrial, CLI-driven procurement system rather than a friendly retail store.
>
> In keeping with the retro-surreal Tamagotchi concept, giant Kaijus (like Godzilla) reside inside their terminal habitat room alongside their furniture — an oversized bed (`SLEEP_POD`), chair/couch (`COUCH_MOD`), desktop workstation (`WORK_STN`), kitchen (`KITCH_UNIT`), lamp (`NEON_LAMP`), and hydration dispenser (`HYDRA_DISP`). The furniture serves as functional, scaled furnishings for the massive titan living in the room.

## 2. Furniture Catalog

The current Proof of Concept (PoC) catalog features six distinct items categorized into Comfort, Utility, and Decorative.

| Item ID | Display Name | ASCII Icon | Price (C) | Stat Modifiers | Category |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `itm_couch` | `COUCH_MOD` | `[===]` | 450 | +15 COMFORT // -5 ENERGY | Comfort |
| `itm_pod` | `SLEEP_POD` | `( Z )` | 800 | +40 ENERGY // +10 HP | Comfort |
| `itm_desk` | `WORK_STN` | `+---+` | 320 | +25 INTEL // -10 JOY | Utility |
| `itm_kit` | `KITCH_UNIT` | `[|O|]` | 1200 | +30 SATUR // +5 HP | Utility |
| `itm_lamp` | `NEON_LAMP` | `  |  ` | 150 | +10 JOY // +2 LUME | Decorative |
| `itm_disp` | `HYDRA_DISP` | `[ ~ ]` | 280 | +20 HYDRA // +5 SATUR | Utility |

## 3. Storage Capacity System

To balance screen density and gameplay, each group habitat (room) has a maximum storage capacity for furniture.
*   **Base Capacity:** The prototype limits the starting room to **12 UNITS** (`STG_CAP: 04/12 UNITS`).
*   **Usage Tracking:** Every item placed in the room consumes 1 unit of storage capacity, regardless of physical dimension.

## 4. Purchase Flow

The purchase flow treats transactions as secure terminal data links. 

```mermaid
flowchart TD
    A[User Opens STORE_MGR] --> B[Fetch Item Catalog]
    B --> C[Display Available Credits & STG_CAP]
    C --> D{User selects [ BUY ]}
    D --> E{Check Credits}
    E -- Sufficient --> F{Check STG_CAP}
    E -- Insufficient --> G[Show 'ERR_INSUFFICIENT_FUNDS']
    F -- Available --> H[Deduct Credits]
    F -- Full --> I[Show 'ERR_HABITAT_CAPACITY_MAX']
    H --> J[Insert into Furniture Inventory]
    J --> K[Update STG_CAP Display]
    K --> L[Render 'PROCUREMENT_SUCCESS_SYS']
```

## 5. Store Interface Wireframe

The ASCII wireframe below demonstrates the terminal rendering target.

```text
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
> STORE_MGR // FURNITURE.DAT [v1.0.4]           <
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  [ SYS_BALANCE: 3450C ]                        
  [ HABITAT_CAP: 04/12 UNITS ]                  
-------------------------------------------------
 [#] ASSET_ID     COST     MODIFIERS
 >1< COUCH_MOD    450C     +15 CMF, -5 ENG
 [2] SLEEP_POD    800C     +40 ENG, +10 HP
 [3] WORK_STN     320C     +25 INT, -10 JOY
 [4] KITCH_UNIT   1200C    +30 SAT, +5 HP
 [5] NEON_LAMP    150C     +10 JOY, +2 LUM
 [6] HYDRA_DISP   280C     +20 HYD, +5 SAT
-------------------------------------------------
  [ BUY 1 ]  [ BUY 2 ]  [ BUY 3 ]  [ EXIT ]     
=================================================
```
