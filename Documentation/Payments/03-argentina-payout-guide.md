# Payments: 03 Argentine Developer Payout & Banking Guide

This guide provides step-by-step instructions for extracting earnings from **Google Play Console** and **Apple App Store Connect** directly into a **local Argentine bank account (`cuenta en dólares`) via SWIFT international wire transfer**, complying with Argentine Central Bank (BCRA) regulations and ARCA (ex AFIP) fiscal requirements.

---

## 1. Payout Pipeline Overview

```mermaid
flowchart LR
    GoogleStore["Google Play Console / App Store"]
    SWIFT["SWIFT Network (International Wire)"]
    Corresp["US Intermediary Bank (e.g. JPMorgan/Citi)"]
    LocalBank["Argentine Local Bank (Galicia, Santander, BBVA)"]
    USDAccount["Local USD Bank Account (CBU en Dólares)"]

    GoogleStore -->|Monthly Wire (USD)| Corresp
    Corresp -->|SWIFT Transfer| LocalBank
    LocalBank -->|Presents Factura E + Boleto COMEX| USDAccount
```

---

## 2. Setting Up Developer Consoles (Google & Apple)

### A. Google Play Console Setup
1. Navigate to **Google Play Console** $\to$ **Settings** $\to$ **Payment profile**.
2. **Account Type**: Select **Individual** (*Persona Humana*) or **Business** (*Empresa*).
3. **Tax Information (US W-8BEN Form)**:
   - Fill out the digital W-8BEN form to certify you are a non-US resident operating from Argentina.
   - Enter your Argentine **CUIT** under "Foreign Tax Identifying Number (FTIN)".
   - This prevents the 30% IRS default withholding on non-US source revenue.
4. **Payout Method**:
   - Select **Add Bank Account** $\to$ **Wire transfer to bank account**.
   - **Bank Name**: Name of your Argentine bank (e.g., *Banco Santander Argentina S.A.*, *Banco Galicia S.A.*).
   - **SWIFT / BIC Code**: Your Argentine bank's 8-character or 11-character SWIFT code:
     - Santander: `BSANARBA`
     - Banco Galicia: `GALIARBA`
     - BBVA Argentina: `BBVAARBA`
     - Banco Macro: `BMAAARBA`
     - Banco Nación: `NACNARBA`
   - **Account Number**: Enter your **22-digit CBU** (Clave Bancaria Uniforme) of your **USD savings account** (*Caja de Ahorro en Dólares*).

### B. Apple App Store Connect Setup
1. Navigate to **App Store Connect** $\to$ **Agreements, Tax, and Banking**.
2. Accept the **Paid Applications Agreement**.
3. **Tax Forms**: Submit the **U.S. Tax Form (W-8BEN)** with your CUIT.
4. **Banking Details**:
   - Country: Argentina.
   - Currency: USD (United States Dollar).
   - SWIFT / BIC Code and 22-digit CBU for your Argentine USD account.

---

## 3. Argentine Central Bank (BCRA) Regulations

Exporting software/services as an independent developer from Argentina is regulated under the **Régimen de Exportación de Servicios**:

### Key Regulatory Framework (BCRA Com. "A" 7518 / Com. "A" 8330):
1. **Direct USD Accreditation Without Forced ARS Liquidation**:
   - Under current regulations, independent individuals (*personas humanas*) exporting digital services and receiving developer royalties can deposit incoming foreign currency directly into their **local USD account** up to **USD 24,000 per calendar year** (or under applicable updated limits) without forced conversion to Argentine Pesos at the official MULC exchange rate.
2. **20 Business Days Rule**:
   - The funds must be transferred and credited to your local Argentine bank within **20 business days** from the date the payment was issued by Google or Apple.
3. **Exemptions for MiPyME**:
   - Developers registered as **MiPyME** (Micro, Pequeña y Mediana Empresa) are exempt from export duties (*derechos de exportación*). Registration is free via the Argentine government portal.

---

## 4. Tax Compliance & Invoicing (ARCA / ex AFIP)

To release international funds held by your Argentine bank's Foreign Trade (*Comercio Exterior / COMEX*) department, you must provide a valid **Factura E**:

### Step-by-Step Factura E Generation:
1. Log in to **ARCA (ex AFIP)** with your Fiscal Key (*Clave Fiscal Nivel 3*).
2. Go to **Administración de Puntos de Venta y Domicilios**:
   - Add a new Point of Sale designated for **"Comprobantes de Exportación - Web Services / Facturación en Línea"**.
3. Open **Comprobantes en Línea**:
   - Select your Export Point of Sale.
   - Document type: **Factura de Exportación E**.
4. **Recipient Information**:
   - **For Google Play Earnings**:
     - Name: `Google LLC`
     - Country: United States (`Estados Unidos`)
     - Tax ID: Not applicable / Foreign Tax ID
     - Address: `1600 Amphitheatre Parkway, Mountain View, CA 94043, USA`
   - **For Apple Store Earnings**:
     - Name: `Apple Inc.`
     - Country: United States (`Estados Unidos`)
     - Address: `One Apple Park Way, Cupertino, CA 95014, USA`
5. **Invoice Details**:
   - Concept: **Servicios** (Exportación de servicios de software / regalías de aplicaciones).
   - Currency: **Dólar Estadounidense (USD)**.
   - Amount: The exact gross/net payout amount reported on your Google Play / Apple monthly statement.
   - Exchange rate: Official Banco Nación selling rate (*tipo de cambio vendedor*) from the preceding business day.
   - **IVA**: 0% (Exportation of services is exempt from Argentine Value-Added Tax).

---

## 5. Bank Ingress & Clearing Procedure (COMEX)

When Google or Apple triggers the monthly SWIFT transfer:

1. **Arrival Notice**:
   Your local bank's Foreign Trade department notifies you (via email or Home Banking COMEX tab) that an international wire has arrived in your name.
2. **Form Submission (Boleto de Ingreso de Fondos)**:
   In your bank's online portal (e.g., *Santander Comercio Exterior*, *Galicia Comex*):
   - Select Concept Code: **`S13` (Servicios de informática y telecomunicaciones)** or **`I07` (Regalías / Derechos de autor)**.
   - Upload the generated **Factura E (PDF)**.
   - Upload the **Google Play / Apple Store Earnings Report** (the monthly statement showing net developer proceeds).
   - Select destination account: **Caja de Ahorro en USD**.
3. **Accreditation**:
   Within 24–48 business hours, the bank clears the transfer, and the USD balance reflects directly in your local bank account.

---

## 6. Bank Fee Considerations

- **US Intermediary Bank Fee**: Between **$15 and $30 USD** is typically deducted by US correspondent banks (e.g., Citibank, Wells Fargo) along the SWIFT transit route.
- **Local Bank Reception Fee**:
  - Argentine banks charge a COMEX reception commission (typically $10–$50 USD or a fixed percentage, e.g. 0.25%, with minimums).
  - *Tip*: Review the tariff schedules of different banks (Banco Santander, Galicia, BBVA, Banco Nación) as some offer reduced or zero COMEX commissions for low-volume export of services.
