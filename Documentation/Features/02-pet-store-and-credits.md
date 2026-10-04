# Features: 02 Pet Store and Credits

This document specifies the in-game pet store, credit balance economics, and dynamic acquisition rules for the **Unix Tamagotchi**.

---

## 1. Credit Economy & Dynamic Capacity Rules

1. **Starting Capital**: The player begins the game with **240 credits**.
2. **Unbounded Pet Ownership (Credit-Bound Only)**:
   - There is no server-side limit on how many pets a player can own.
   - A player may adopt as many pets as their credit balance allows. With 240 starting credits and pets at 120 each, a new player can adopt up to 2 pets immediately ($2 \times 120 = 240$). As credits accumulate through future work actions or IAP, the family grows without any code changes.
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
FUNCTION processStorePurchase(currentCredits, ownedPets, catalogItem, customNickname):

  // Check: Available credits
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
