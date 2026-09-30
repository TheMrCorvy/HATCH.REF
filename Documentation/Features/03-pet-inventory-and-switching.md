# Features: 03 Pet Inventory and Switching

This document specifies the pet inventory architecture, companion switching mechanics, and stat preservation rules for the **Unix Tamagotchi**.

---

## 1. Dynamic Inventory Model

The player's inventory dynamically accommodates all adopted pets:

```text
┌─────────────────────────────────────────────────────────────┐
│ SUB_SYS: PET INVENTORY (DYNAMIC CAPACITY)                   │
├─────────────────────────────────────────────────────────────┤
│ PET #01: [ ACTIVE COMPANION ]                               │
│ PID: pet_1714200001 | TYPE: Bunny | NICK: BUNNY_01          │
│ HUNGER: 75% | ENERGY: 80% | MOOD: 90%                       │
│ STATUS: Active in Securing Session Viewport                 │
├─────────────────────────────────────────────────────────────┤
│ PET #02: [ STANDBY ]                                        │
│ PID: pet_1714200002 | TYPE: Cat   | NICK: CYBER_CAT         │
│ HUNGER: 85% | ENERGY: 60% | MOOD: 70%                       │
│ STATUS: Resting in Standby Storage                          │
├─────────────────────────────────────────────────────────────┤
│ PET #03..N: [ STANDBY COMPANIONS ]                          │
│ Additional companions resting safely in standby memory.     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Active vs. Standby Rules

1. **One Active Companion in Room**: Actions (`Eat`, `Sleep`, `Play`, `Basketball`) target the currently designated active companion.
2. **Standby Stat Decay Suppression**: While resting in standby, a pet's stats decay at a heavily reduced rate ($0.1\times$ normal rate) so the player is never penalized for rotating companions.
3. **Instant Switching**: Switching between companions is instantaneous with zero loading latency, updating the game state immediately.

---

## 3. Switching Implementation

Switching logic ensures the new pet is correctly loaded into the active scene state:

```text
FUNCTION switchActivePet(gameState, targetPetId):
  // Find the requested pet in the player's inventory
  targetPet = FIND pet IN gameState.ownedPets WHERE pet.id == targetPetId
  
  IF targetPet IS NULL THEN
    THROW ERROR("Pet not found in memory")
    
  // Update the active reference in the global state
  gameState.setActivePet(targetPet.id)
  
  LOG("> Switched active companion to " + targetPet.nickname)
```
