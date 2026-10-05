# Payments: 01 App Store & Google Play In-App Purchase Rules

This document outlines the policy requirements, fee tiers, and compliance rules imposed by **Google Play** and the **Apple App Store** for selling digital kaijus and currency in the **Unix Tamagotchi**.

---

## 1. Digital Goods Compliance Mandate

Both Google and Apple enforce strict rules regarding in-app monetization:

> [!IMPORTANT]
> **Mandatory In-App Billing for In-Game Currency**:
> Any currency, digital kaiju, skin, or consumable item used exclusively within a mobile app **MUST** be processed using the platform's proprietary billing system:
> - **Android**: Google Play Billing Library.
> - **iOS**: Apple StoreKit 2.
>
> Using external web checkouts (such as Stripe, PayPal, or Mercado Pago) inside the mobile app to sell digital game credits is a direct violation of developer policies and results in immediate app suspension or rejection.

---

## 2. Platform Commission & Fee Structures

Both platforms provide reduced fee programs for independent and small-scale developers:

| Platform | Standard Commission Rate | Small Business Program Rate | Eligibility Criteria |
| :--- | :---: | :---: | :--- |
| **Google Play** | 30% | **15%** | First **$1,000,000 USD** in annual developer earnings across all associated accounts. Requires enrollment in Play Console. |
| **Apple App Store** | 30% | **15%** | Developers earning under **$1,000,000 USD** in the previous calendar year. Requires enrollment in App Store Small Business Program. |

---

## 3. Product Catalog SKU Classification

In-app products in mobile stores belong to one of four categories. For the **Unix Tamagotchi**, products are classified as follows:

```
┌────────────────────────────────────────────────────────┐
│ Product Type            │ Tamagotchi Implementation   │
├─────────────────────────┼─────────────────────────────┤
│ 1. Consumable           │ Credit Packs (e.g., 500 $)  │
│    (Can be bought       │ - Used to buy kaijus          │
│     multiple times)     │ - Consumed upon spending    │
├─────────────────────────┼─────────────────────────────┤
│ 2. Non-Consumable       │ Exclusive Kaiju Unlock        │
│    (Purchased once,     │ - e.g. "Godzilla 1-bit Kaiju"   │
│     restorable across   │ - Restored via              │
│     devices)            │   "Restore Purchases"       │
├─────────────────────────┼─────────────────────────────┤
│ 3. Auto-Renewing Sub    │ VIP Hacker Pass (Future)    │
│    (Recurring billing)  │ - Monthly credit stipend    │
│                         │ - Exclusive 1-bit dithered palette themes │
└────────────────────────────────────────────────────────┘
```

---

## 4. Mandatory Store Requirements

To pass store review when IAP is activated in Phase 4:

1. **Restore Purchases Button**:
   Apple and Google require an explicit, easily accessible button in the Settings screen titled **"Restore Purchases"** for any non-consumable items or subscriptions.
2. **Clear Price and Currency Presentation**:
   Product prices must be dynamically retrieved from the platform SDK so they display in the user's localized currency (e.g., `ARS $`, `USD $`, `EUR €`). Never hardcode dollar signs in production IAP screens.
3. **Terms of Service & Privacy Policy**:
   Direct links to the Privacy Policy and Terms of Use (EULA) must be present in the app settings and the store listing.
