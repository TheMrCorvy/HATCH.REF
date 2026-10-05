# Features: 02 Kaiju Store and Credits

This document specifies the in-game Kaiju store, credit balance economics, and dynamic acquisition rules for the **Unix Tamagotchi**.

---

## 1. Credit Economy & Dynamic Capacity Rules

1. **Starting Capital**: The player begins the game with **240 credits**.
2. **Unbounded Kaiju Ownership (Credit-Bound Only)**:
   - There is no server-side limit on how many Kaiju specimens a player can own.
   - A player may adopt as many Kaijus as their credit balance allows. With 240 starting credits and Kaijus at 120 each, a new player can adopt up to 2 specimens immediately ($2 \times 120 = 240$). As credits accumulate through city destruction work actions or IAP, the roster grows without any code changes.
3. **PoC Fixed Recharge**: For Day 1 PoC, there are no credit top-ups; players spend from their initial 240 credit grant.

---

## 2. Store Catalog

| Item ID | Kaiju Type | Display Name | Cost | Traits |
| :--- | :--- | :--- | :--- | :--- |
| `item_godzilla` | `godzilla` | **Godzilla** | 120 Credits | Apex saurian titan, dorsal plates, atomic breath animations, balanced stats, 1-bit dithered pixel sprite (see `Desing References/Godzila.webp`). |
| `item_cyber_godzilla` | `cyber_godzilla` | **Cyber Godzilla** | 120 Credits | Cybernetic apex titan, steel hull, laser blast animations, higher energy drain, 1-bit dithered pixel sprite. |

---

## 3. Transaction Logic

The core logic for processing a kaiju acquisition in the store ensures that players meet both capacity and financial requirements. This can be expressed in the following pseudocode:

```text
FUNCTION processStorePurchase(currentCredits, ownedKaijus, catalogItem, customNickname):

  // Check: Available credits
  IF currentCredits < catalogItem.priceCredits THEN
    RETURN Failure("Insufficient credits! Need " + catalogItem.priceCredits + ", available: " + currentCredits + ".")

  // Determine nickname
  IF customNickname IS PROVIDED AND NOT EMPTY THEN
    nickname = uppercase(customNickname)
  ELSE
    nickname = uppercase(catalogItem.kaijuType) + "_0" + (count(ownedKaijus) + 1)

  // Create new kaiju instance
  newKaiju = CREATE KaijuInstance WITH:
    id = GENERATE_UNIQUE_ID()
    kaijuType = catalogItem.kaijuType
    nickname = nickname
    lastInteractionTimestamp = CURRENT_TIME()

  RETURN Success("Acquired " + nickname + " for " + catalogItem.priceCredits + " credits!", newKaiju)
```
