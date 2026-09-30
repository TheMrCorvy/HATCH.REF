# Features: 02 Pet Store and Credits

This document specifies the in-game pet store, credit balance economics, and dynamic acquisition rules for the **Unix Tamagotchi**.

---

## 1. Credit Economy & Dynamic Capacity Rules

1. **Starting Capital**: The player begins the game with **240 credits**.
2. **Dynamic Pet Capacity (No Hardcoded 2-Pet Limit)**:
   - The player is **not restricted** to a hardcoded limit of 2 pets.
   - Any limits on pet ownership are managed dynamically by the backend (`profiles.max_pets_allowed`). If this setting is `NULL`, the player can adopt as many pets as their credits allow.
   - With the initial 240 credits and pets priced at 120 credits, a new player can adopt up to 2 pets immediately ($2 \times 120 = 240$). If more credits are earned through future work actions or IAP, the player can expand their companion family without code modifications.
3. **PoC Fixed Recharge**: For Day 1 PoC, there are no credit top-ups; players spend from their initial 240 credit grant.

---

## 2. Store Catalog

| Item ID | Pet Type | Display Name | Cost | Traits |
| :--- | :--- | :--- | :--- | :--- |
| `item_bunny` | `bunny` | **Bunny** | 120 Credits | Gentle companion, balanced stats, 1-bit dithered pixel sprite. |
| `item_cat` | `cat` | **Cyber Cat** | 120 Credits | Playful hacker feline, purring animations, higher energy drain, 1-bit dithered pixel sprite. |

---

## 3. Transaction Logic

The core logic for processing a pet adoption in the store ensures that players meet both capacity and financial requirements. This can be expressed in the following pseudocode:

```text
FUNCTION processStorePurchase(currentCredits, ownedPets, backendMaxPetsLimit, catalogItem, customNickname):

  // Check 1: Backend dynamic limit (if configured)
  IF backendMaxPetsLimit IS NOT NULL AND count(ownedPets) >= backendMaxPetsLimit THEN
    RETURN Failure("Store notice: You have reached the maximum allowed pet capacity.")

  // Check 2: Available credits
  IF currentCredits < catalogItem.priceCredits THEN
    RETURN Failure("Insufficient credits! Need " + catalogItem.priceCredits + ", available: " + currentCredits + ".")

  // Determine nickname
  IF customNickname IS PROVIDED AND NOT EMPTY THEN
    nickname = uppercase(customNickname)
  ELSE
    nickname = uppercase(catalogItem.petType) + "_0" + (count(ownedPets) + 1)

  // Create new pet instance
  newPet = CREATE PetInstance WITH:
    id = GENERATE_UNIQUE_ID()
    petType = catalogItem.petType
    nickname = nickname
    lastInteractionTimestamp = CURRENT_TIME()

  RETURN Success("Adopted " + nickname + " for " + catalogItem.priceCredits + " credits!", newPet)
```
