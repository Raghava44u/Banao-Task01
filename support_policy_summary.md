# Vireo Audio Customer Support Operating Policy — Summary & Operational Analysis

**Document Reference**: Customer Support Operating Policy v3.2  
**Effective Date**: 1 April 2025  
**Policy Owner**: Priya Raman, Head of Customer Experience  
**Operational Scope**: Support operations across Bengaluru and Indore sites, covering 44 rostered agents, 3 shifts, and all inbound support channels.

---

## 1. Channels, Hours, and Intake Mechanism

| Channel | Operating Hours | Operational Coverage | Intake & Routing Mechanism |
| :--- | :--- | :--- | :--- |
| **Chat** (Web & App) | 24x7 | Daytime: Bengaluru & Indore; Overnight: Indore Night Shift | Chat bot asks opening questions, assigns initial category tag, routes ticket. |
| **Email** | 24x7 | Worked in queue order | Intake bot opens email ticket, assigns initial category tag based on initial email text. |
| **Voice** | 08:00 – 22:00 IST | Inbound IVR collects callback requests; returned by Voice Frontline | IVR transcript captured; category assigned based on IVR menu / intake. |
| **Social** (IG, X, FB) | Daytime shifts | Handled by Chat Frontline team | Intake bot tags category and routes to Chat Frontline queue. |

> **Operational Insight**: The intake bot sets the initial `category` and determines initial `assigned_team` routing. While agents are permitted to correct tags upon closure, helpdesk logs reveal agents rarely do. Consequently, naive keyword triggers (e.g. *"paid"*, *"bill"*, *"order"*) create massive systematic misrouting.

---

## 2. Service Level Agreements (SLAs) & Financial Penalties

First-response SLA is measured strictly from **ticket creation** to the **first human agent reply**.

| Channel | First-Response Target | Observed Mean Resp. Time | Observed Median Resp. Time | Historical Breach Rate | Breach Penalty Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Chat** | **15 minutes** | 9.0 min | 5.0 min | 13.37% (720 / 5,387) | Rs 350 auto store credit |
| **Voice** | **2 hours (120 min)** | 46.9 min | 33.0 min | 5.82% (99 / 1,702) | Rs 350 auto store credit |
| **Social** | **4 hours (240 min)** | 100.5 min | 67.0 min | 8.01% (91 / 1,136) | Rs 350 auto store credit |
| **Email** | **8 hours (480 min)** | 247.3 min | 162.0 min | 12.10% (430 / 3,555) | Rs 350 auto store credit |
| **Blended Total** | — | — | — | **11.38% (1,340 / 11,780)** | **Total Incurred: Rs 469,000** |

### Penalty Terms (§3):
- Every ticket that misses its first-response target automatically issues a **Rs 350 store credit** to the customer's account upon resolution.
- Credits are issued automatically regardless of reason and charged directly to the SLA credit line in the support P&L.
- Breaches are reported against the resolving agent in standard helpdesk reporting.

---

## 3. Financial Cost Standards (FY26 Planning Figures)

These official figures govern all operational business cases and staffing models:

### 3.1. Contact Costs by Channel (§4)
- **Chat**: Rs 210 per contact
- **Email**: Rs 260 per contact
- **Voice Callback**: Rs 520 per contact
- **Social**: Rs 240 per contact
- **Blended Channel Average**: Rs 290 per contact across current channel mix (actual observed blended cost: Rs 272.77).

### 3.2. Internal Transfer Overhead (§4)
- **Cost per Internal Transfer**: **Rs 305 per transfer** (accounts for re-handling, context-switching, and administrative overhead).
- **Observed Impact**: 1,299 transfers in the helpdesk era generated **Rs 396,195** in unnecessary internal re-handling costs, primarily from misrouted tickets transferred from Billing to Logistics.

### 3.3. Staffing & Headcount Cost Standards (§4 & Email Thread)
- **Fully Loaded Agent Cost**: **Rs 165 per agent-hour**.
- **Shift Duration**: 8 hours (Rs 1,320 per shift).
- **Annual Cost per Full-Time Hire**: **Rs 4,50,000 per year** (confirmed by Finance Controller Arjun Mehta: *"Two hires is about Rs 9 lakh a year"*).

---

## 4. Refunds, Replacements & Warranty Rules (§5)

### 4.1. Resolution Entitlements
1. **Dead On Arrival (DOA)**: Within 7 days of delivery. Customer has sole discretion to choose a full refund or an immediate replacement.
2. **In-Warranty Hardware Fault**: Covered for repair or replacement (12 months for audio/wearables, 6 months for cables/chargers/cases).
3. **Lost or Damaged in Transit**: Re-shipment or full refund.
4. **Goodwill Credits**: Capped at Rs 500 per ticket; strictly requires Team Lead approval.

### 4.2. Replacement Planning Cost
- **Replacement Cost Formula**: $\text{Unit Cost (from products.csv)} + \text{Rs 340 (reverse pickup + forward shipping)}$.
- **Refurbishment Recovery**: Zero recovery value permitted in planning models.

### 4.3. Refund Reason Codes
Agents must select from the official dropdown codes when initiating a refund:
1. `RETURN-QC-OK`: Return received at warehouse and passed QC inspection (663 tickets, Rs 2,427,337)
2. `DUP-PAYMENT`: Duplicate charge or payment gateway failure (498 tickets, Rs 1,321,802)
3. `CANCEL`: Order cancelled before dispatch (303 tickets, Rs 788,197)
4. `LOST-TRANSIT`: Order lost or confirmed undelivered by carrier (161 tickets, Rs 443,439)
5. `DOA-REPL`: Dead on arrival, refund chosen over replacement (108 tickets, Rs 304,892)
6. `PRICE-ADJ`: Post-purchase price match or coupon adjustment (81 tickets, Rs 28,350)
7. `WTY-BUYBACK`: Warranty buy-back where replacement is unavailable (45 tickets, Rs 13,706)
8. `GW-OTHER`: Goodwill credit / Other approved exception (35 tickets, Rs 5,000)

### 4.4. Double Recovery Prohibition & Violations
- **Strict Rule**: *"In no case is a customer to receive both a refund and a replacement for the same order; where this happens in error it must be escalated to the Team Lead and Finance the same day."*
- **Audit Findings**: Exactly two tickets breached this rule:
  - `TK-241926`: Rs 6,999 refund + Replacement Strata 2.
  - `TK-248344`: Rs 250 refund + Replacement Orbit Mini.
  - Total unauthorized financial leak: Rs 7,249 + replacement costs.

---

## 5. Organizational Structure, Tiers & Roster (§6 & §7)

### 5.1. Team Ownership & Responsibilities
- **Chat Frontline (Tier 1)**: First contact for product queries, accounts, app guidance via chat & social.
- **Email Frontline (Tier 1)**: First contact for product queries, accounts, app guidance via email.
- **Voice Frontline (Tier 1)**: Inbound IVR callback returns for product & account inquiries.
- **Logistics**: Sole ownership of carrier management, delivery tracking, AWB traces, RTO, and reshipment.
- **Billing**: Sole ownership of payment gateway reconciliations, double deductions, and GST invoices.
- **Returns Desk**: Sole ownership of reverse logistics pickups, warehouse QC, and refund issuance.
- **Escalations & Warranty (Tier 2)**: Sole certified ownership of warranty RMA, hardware defects, and service center management.

### 5.2. Tier 2 Performance Standard (§6)
- **Critical Policy Mandate**: *"Tier 2 cases are multi-touch by nature and are measured on resolution in days, not on tickets closed per week. Tier 2 agents are not to be compared with Tier 1 on volume metrics."*
- **Operational Reality**: Escalations & Warranty handles complex hardware issues with a median resolution time of **122 hours** (5.1 days). Evaluating them on raw ticket count would severely misrepresent their workload.

### 5.3. Roster & Shifts (§7)
- **Total Headcount**: 44 agents (25 Bengaluru, 19 Indore).
- **Shift Schedule (IST)**:
  - Morning Shift: 06:00 – 14:00 (27 agents)
  - Day Shift: 14:00 – 22:00 (12 agents)
  - Night Shift: 22:00 – 06:00 (5 agents, based exclusively in Indore)

---

## 6. Helpdesk Systems & Reporting Definitions (§8, §9, §10)

- **System Migration**: Migrated from Freshdesk (`legacy_fd`) to current helpdesk on 14 September 2025.
- **Timestamp Conventions**: Current helpdesk exports IST in standard reports. Migrated legacy resolution timestamps were reconstructed from UTC logs, creating an apparent 5.5-hour backward shift in raw data.
- **Transfers Field**: Available only in current helpdesk exports; legacy Freshdesk records are blank.
- **CSAT Survey**: 1–5 score. Approximately 45% response rate (actual 45.4%). Unanswered surveys are blank and must be excluded from averages.
- **First Contact Resolution (FCR)**: Resolved without the same customer re-contacting about the same issue within 30 days.
- **Handle Time**: Measured from first human response to resolution.
