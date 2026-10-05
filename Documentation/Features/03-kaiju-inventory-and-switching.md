# Features: 03 Kaiju Inventory and Switching

This document specifies the Kaiju specimen inventory architecture, companion switching mechanics, and stat preservation rules for the **Unix Tamagotchi**.

---

## 1. Dynamic Inventory Model

The player's inventory dynamically accommodates all adopted Kaijus:

```text
┌─────────────────────────────────────────────────────────────┐
│ SUB_SYS: KAIJU INVENTORY (DYNAMIC CAPACITY)                 │
├─────────────────────────────────────────────────────────────┤
│ SPECIMEN #01: [ ACTIVE COMPANION ]                          │
│ PID: kaiju_1714200001 | TYPE: Godzilla | NICK: GODZILLA_01 │
│ HUNGER: 75% | ENERGY: 80% | MOOD: 90%                       │
│ STATUS: Active in Habitat Session Viewport                  │
├─────────────────────────────────────────────────────────────┤
│ SPECIMEN #02: [ STANDBY ]                                   │
│ PID: kaiju_1714200002 | TYPE: Cyber Godzilla | NICK: CYBER_01│
│ HUNGER: 85% | ENERGY: 60% | MOOD: 70%                       │
│ STATUS: Resting in Subterranean Standby Containment         │
├─────────────────────────────────────────────────────────────┤
│ SPECIMEN #03..N: [ STANDBY KAIJUS ]                         │
│ Additional Kaiju titans resting safely in standby memory.   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Active vs. Standby Rules

1. **One Active Companion in Room**: Actions (`Eat`, `Sleep`, `Play`, `Crush Tanks`) target the currently designated active companion.
2. **Standby Stat Decay Suppression**: While resting in standby, a kaiju's stats decay at a heavily reduced rate ($0.1\times$ normal rate) so the player is never penalized for rotating companions.
3. **Instant Switching**: Switching between companions is instantaneous with zero loading latency, updating the game state immediately.

---

## 3. Switching Implementation

Switching logic ensures the new kaiju is correctly loaded into the active scene state:

```text
FUNCTION switchActiveKaiju(gameState, targetKaijuId):
  // Find the requested kaiju in the player's inventory
  targetKaiju = FIND kaiju IN gameState.ownedKaijus WHERE kaiju.id == targetKaijuId
  
  IF targetKaiju IS NULL THEN
    THROW ERROR("Kaiju not found in memory")
    
  // Update the active reference in the global state
  gameState.setActiveKaiju(targetKaiju.id)
  
  LOG("> Switched active companion to " + targetKaiju.nickname)
```
