# Design: 05 1-Bit Terminal Wireframes

This document provides visual wireframe approximations of the core screens in the **Unix Tamagotchi** app, adhering strictly to the industrial terminal UI and 1-bit dithered pixel art aesthetic. 

---

## 1. Pet Room Screen

The primary interaction screen, featuring the two-layer compositing (Flame viewport + UI).

```text
==================================================
SUB_SYS: LEPUS-01           V.1.0.4       14:02:33
==================================================

VITALS.SATUR   [████████░░] 80%
VITALS.ENERGY  [██████░░░░] 60%
VITALS.JOY     [██████████] 100%

      ┌                              ┐
      
         ( Flame GameWidget )
         ( 1-Bit Dithered   )
         ( Bunny Sprite     )
         
      └                              ┘

[ > EAT ]    [ > SLEEP ]    [ > PLAY ]

> INITIALIZING VIRTUAL ENVIRONMENT...
> COMPANION AWAKE.
--------------------------------------------------
MEMORY: 48KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 2. Pet Store Screen (PETS_LAB)

Where players acquire new pets using their credits.

```text
==================================================
SYS: PETS_LAB // ACQUISITION          CR: 1,450
==================================================

AVAILABLE SPECIMENS:

┌──────────────────────────────────────────────┐
│ ID: LEPUS-01   "Terminal Bunny"              │
│ PRICE: 120 CR                                │
│ STATUS: AVAILABLE                            │
│                                              │
│ [ > ACQUIRE ]                 [ > CANCEL ]   │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ ID: FELIS-02   "Cyber Cat"                   │
│ PRICE: 240 CR                                │
│ STATUS: AVAILABLE                            │
│                                              │
│ [ > ACQUIRE ]                 [ > CANCEL ]   │
└──────────────────────────────────────────────┘

--------------------------------------------------
MEMORY: 51KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 3. Inventory Screen (STORAGE_MGR)

Managing items and consumables.

```text
==================================================
SYS: STORAGE_MGR // INVENTORY         CAP: 14/50
==================================================

ITEM_01: NUTRIENT_PELLET
QTY: 14
[ > USE_ITEM ]    [ > DISCARD ]

ITEM_02: CAFFEINE_STIM
QTY: 3
[ > USE_ITEM ]    [ > DISCARD ]

ITEM_03: BANDAGE_KIT
QTY: 1
[ > USE_ITEM ]    [ > DISCARD ]

> STORAGE CAPACITY OPTIMAL.
--------------------------------------------------
MEMORY: 50KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 4. Settings Screen (SYS_DIAG)

Hardware and system configurations.

```text
==================================================
SYS_DIAG // HARDWARE CONFIGURATION
==================================================

AUDIO_OUTPUT
[████████░░] 80%   [ > MUTE ]

LUMINANCE (SHADER THRESHOLD)
[████░░░░░░] 40%

REFRESH_RATE (HZ SIMULATION)
[██████████] 100%

┌──────────────────────────────────────────────┐
│ HARDWARE_INFO                                │
│ OS: UNIX_TAMAGOTCHI V.1.0.4                  │
│ RENDER: FLAME_ENGINE / BAYER_SHADER          │
│ UPTIME: 14h 22m                              │
│ SYNC_STATUS: MULTIPLAYER_OFFLINE             │
└──────────────────────────────────────────────┘

--------------------------------------------------
MEMORY: 48KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 5. Evolution Screen (EVO_MGR)

Tracking pet growth and metrics.

```text
==================================================
EVO_MGR // GROWTH TIMELINE
==================================================

SPECIMEN: LEPUS-01
CURRENT STAGE: ADULT (STAGE_03)

[ EGG ] ---> [ BABY ] ---> [ ADULT ]
             ( 12h )       ( 72h )

METRICS_LOG:
- AVG_JOY: 92%
- FEED_RATE: OPTIMAL
- ILLNESS_EVENTS: 0

DNA INTEGRITY: 99.8% STABLE

[ > VIEW_GENETICS ]    [ > EXPORT_DATA ]

--------------------------------------------------
MEMORY: 55KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 6. Critical Failure (ERR_SYS)

> [!NOTE]
> **Phase 2+ Feature**: This screen is not included in the initial PoC. Pets do not die or reach critical failure states in Phase 1. This wireframe serves as a visual reference for future implementation.

Death or critical state (Rendered entirely with the Crimson emergency palette).

```text
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
ERR_SYS // CRITICAL FAILURE DETECTED
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

FATAL ERROR: VITALS_DEPLETED
SPECIMEN: LEPUS-01

CAUSE: SATURATION = 0%, ENERGY = 0%
TIME_OF_FAILURE: 14:32:11

┌──────────────────────────────────────────────┐
│ SYSTEM HALTED.                               │
│ SPECIMEN CANNOT BE RECOVERED.                │
│                                              │
│ [ > EMERGENCY REBOOT ]                       │
│ [ > ARCHIVE_LOGS ]                           │
└──────────────────────────────────────────────┘

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
WARNING: ACTION CANNOT BE UNDONE.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
```

---

## 7. Furniture Store (STORE_MGR)

Scrollable catalog for habitat customization.

```text
==================================================
SYS: STORE_MGR // HABITAT OUTFITTING   CR: 1,450
==================================================

┌──────────────────────────────────────────────┐
│ ITEM: BASIC_BED                              │
│ TYPE: FURNITURE                              │
│ BOOSTS: +10% ENERGY RECOVERY                 │
│ PRICE: 300 CR                                │
│ [ > ACQUIRE ]                                │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ ITEM: BASKETBALL_HOOP                        │
│ TYPE: TOY                                    │
│ BOOSTS: +15% JOY, -5% ENERGY                 │
│ PRICE: 450 CR                                │
│ [ > ACQUIRE ]                                │
└──────────────────────────────────────────────┘

--------------------------------------------------
MEMORY: 53KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```
