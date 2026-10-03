# Vireo Audio Support Data Audit Report

**Date of Audit**: October 2026  
**Analyst / System**: Antigravity AI Autonomous Data Pipeline  
**Source Location**: `Given/`  
**Dataset Scope**: Support operations data spanning June 2024 to June 2026 (11,780 tickets, 44 agents, 9,500 customers, 15,000 orders, 14 products).

---

## 1. Executive Summary

A comprehensive data audit was conducted across all five source tables (`tickets.csv`, `agents.csv`, `customers.csv`, `orders.csv`, `products.csv`) and accompanying documentation (`support-policy.pdf`, `README.txt`, `email-thread.txt`). 

The primary findings demonstrate that while relational integrity across foreign keys is **100% intact** (zero orphan records), there are critical **operational and system artifacts** that distort management's perception of workload:
1. **Intake Bot Misclassification & Routing Artifact**: Initial ticket category was assigned entirely by an intake bot. Every ticket tagged `Billing & Payments` was automatically assigned to the Billing team (2,564 tickets). Over 42% of these tickets are in fact **Delivery & Shipping** tracking inquiries triggered because the customer mentioned words like *"paid"* or quoted payment dates.
2. **The "Other" Category Dumping Ground**: 1,622 tickets (13.8% of all tickets) were tagged as `Other` and routed to frontline tiers. These tickets contain clear, actionable intents: pre-dispatch order cancellations (303 tickets), battery drain, and Bluetooth issues.
3. **Logistics Bottleneck & Hidden Workload**: While Billing appears to have the highest assigned queue (2,564 tickets vs Logistics' 1,905), Logistics actually resolved **2,673 tickets** (second only to Chat Frontline) due to receiving **795 ticket hand-offs from Billing**. Logistics' median resolution time is **24.5 hours** (mean 41.1 hours), compared to Billing's median resolution time of **23 minutes**.
4. **Legacy UTC Timestamp Skew**: In 2,379 legacy Freshdesk tickets, `resolved_at` appears earlier than `created_at`. This is an artifact of Freshdesk event logs storing resolution in UTC while creation is in IST. Adding +5:30 resolves 100% of these anomalies.
5. **Support Policy Compliance Violations**: Support Policy §5 explicitly states: *"In no case is a customer to receive both a refund and a replacement for the same order."* The audit discovered **2 tickets** (`TK-241926` and `TK-248344`) where both a refund and a replacement were processed.
6. **Agent Roster Display Name Collision**: Two distinct agents share the display name *"Om Sharma"* (Agent ID `A3006` in Indore, Morning Shift; Agent ID `A3029` in Bengaluru, Morning Shift). System logic must strictly use `agent_id`.

---

## 2. Table-by-Table Structural Profile

| Table Name | Total Rows | Total Columns | Primary Key | Key Relationships / Foreign Keys | Null Columns |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `tickets.csv` | 11,780 | 21 | `ticket_id` | `customer_id`, `order_id`, `product_sku`, `agent_id` | `order_id` (4,017), `resolved_at` (583), `transfers` (4,052), `csat_score` (6,435), `refund_amount_inr` (9,886), `refund_reason_code` (9,886) |
| `agents.csv` | 44 | 8 | `agent_id` | Roster entries | `to_date` (44 nulls - all currently active) |
| `customers.csv` | 9,500 | 6 | `customer_id` | Referenced by tickets & orders | None (100% complete) |
| `orders.csv` | 15,000 | 8 | `order_id` | `customer_id`, `sku` | None (100% complete) |
| `products.csv` | 14 | 7 | `sku` | Catalog definitions | None (100% complete) |

---

## 3. Relational & Foreign Key Integrity Audit

| Relationship | Child Table.Field | Parent Table.Field | Total Child Records | Matched Records | Orphan Records | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Customer Reference | `tickets.customer_id` | `customers.customer_id` | 11,780 | 11,780 | 0 | **PASS (100%)** |
| Order Reference | `tickets.order_id` | `orders.order_id` | 7,763 (non-null) | 7,763 | 0 | **PASS (100%)** |
| Fallback Order Join | `tickets.(customer_id + sku)` | `orders.(customer_id + sku)` | 4,017 (null order_id) | 4,017 | 0 | **PASS (100% recoverable)** |
| Product Reference | `tickets.product_sku` | `products.sku` | 11,780 | 11,780 | 0 | **PASS (100%)** |
| Agent Reference | `tickets.agent_id` | `agents.agent_id` | 11,780 | 11,780 | 0 | **PASS (100%)** |
| Order Customer | `orders.customer_id` | `customers.customer_id` | 15,000 | 15,000 | 0 | **PASS (100%)** |
| Order Product | `orders.sku` | `products.sku` | 15,000 | 15,000 | 0 | **PASS (100%)** |

---

## 4. Key Data Quality Findings & Anomalies

### 4.1. The Intake Bot Misclassification & Routing Failure
- **Finding**: Initial category was determined exclusively by the intake bot's opening prompt. The routing rule was deterministic:
  - `Billing & Payments` (2,564) -> 100% routed to Billing
  - `Delivery & Shipping` (1,905) -> 100% routed to Logistics
  - `Returns & Refunds` (1,049) -> 100% routed to Returns Desk
  - `Warranty & Repair` (525) -> 100% routed to Escalations & Warranty
  - Technical & General categories -> split by channel to Frontline teams.
- **Root Cause**: Customers writing *"I paid on 19 Jun, where is my tracking"* triggered the keyword *"paid"*, leading the bot to categorize them as `Billing & Payments`.
- **Operational Consequence**: Billing's initial queue was inflated to 2,564 tickets (21.8% of total volume). However, Billing agents transferred 795 of these tickets to Logistics.

### 4.2. Workload Reality: Assigned vs. Resolving Queue
Comparing assigned queue to resolving team proves where work was actually performed:

| Team | Assigned Queue Volume | Resolving Agent Volume | Net Shift | % of Total Work Resolved |
| :--- | :--- | :--- | :--- | :--- |
| **Chat Frontline** | 3,030 | 3,078 | +48 | 26.1% |
| **Logistics** | 1,905 | **2,673** | **+768 (+40.3%)** | **22.7%** |
| **Billing** | 2,564 | **1,838** | **-726 (-28.3%)** | **15.6%** |
| **Email Frontline** | 1,807 | 1,658 | -149 | 14.1% |
| **Returns Desk** | 1,049 | 1,117 | +68 | 9.5% |
| **Voice Frontline** | 900 | 766 | -134 | 6.5% |
| **Escalations & Warranty** | 525 | 650 | +125 | 5.5% |
| **Total** | **11,780** | **11,780** | **0** | **100.0%** |

### 4.3. Freshdesk Legacy Migration Timestamps (UTC vs. IST)
- Tickets prior to 14 September 2025 were migrated from Freshdesk (`legacy_fd`, 4,052 tickets).
- `created_at` and `first_response_at` were recorded in IST.
- `resolved_at` was reconstructed from legacy event logs which recorded timestamps in UTC.
- Because IST is UTC + 5:30, 2,379 legacy tickets had `resolved_at < created_at` in raw data.
- **Remediation**: The data pipeline applies a +5:30 timedelta correction to `legacy_fd` resolution timestamps, completely resolving negative handle times.

### 4.4. Internal Ticket Transfers
- Helpdesk period (7,728 tickets) recorded 1,299 internal transfers across 1,090 transferred tickets.
- At the policy-mandated re-handling cost of Rs 305 per transfer, internal hand-offs cost **Rs 396,195**.
- 61.2% of transfers originated from Billing transferring misclassified tracking/delivery tickets to Logistics.

### 4.5. Support Policy Compliance Violations
- **Support Policy §5 Rule**: Double recovery (receiving both refund and replacement for the same order) is strictly prohibited and must be escalated to Team Lead and Finance.
- **Audit Discovery**:
  1. `TK-241926` (Order VR888747, Strata 2): Refund of Rs 6,999 + Replacement unit issued.
  2. `TK-248344` (Order VR906727, Orbit Mini): Refund of Rs 250 + Replacement unit issued.
- **Action Required**: Flagged in data quality report for immediate Finance reconciliation.

### 4.6. First-Response SLA Performance & Breach Penalties
- Target: Chat (15 min), Voice (120 min), Social (240 min), Email (480 min).
- **Observed Breaches**: 1,340 tickets breached SLA (11.38% overall breach rate).
  - Chat: 720 breaches (13.37%)
  - Email: 430 breaches (12.10%)
  - Voice: 99 breaches (5.82%)
  - Social: 91 breaches (8.01%)
- **Financial Liability**: Support Policy §3 mandates a Rs 350 automatic store credit per breach. Total incurred SLA credits equal **Rs 469,000**.

---

## 5. Conclusion & Pipeline Recommendations

1. **Do not use `category` as ground truth**: The intake bot category is heavily biased by naive keyword triggers.
2. **Do not staff based on initial assigned queue**: Basing headcount on `assigned_team` rewards poor routing rather than true operational workload.
3. **Use resolving agent (`agent_id`) and true ticket intent** to measure genuine team demand.
4. **Standardize legacy timestamps**: Always apply the +5:30 UTC-to-IST correction when calculating handle times.
