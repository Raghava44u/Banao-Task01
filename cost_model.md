# Vireo Audio Customer Support Financial & Operational Cost Model

**Author**: Vireo Audio Finance & CX Analytics  
**Reference Standards**: Customer Support Operating Policy v3.2 §4, §5 & Corporate Financial Guidance  
**Target Audience**: Arjun Mehta (Finance Controller), Priya Raman (Head of CX)

---

## 1. Executive Financial Summary

During the analyzed support period (11,780 customer contacts), the total quantified customer support operational expenditure and customer resolution concessions reached **Rs 11,413,088 (~Rs 1.14 Crore)**.

| Cost Component | Unit Rate Basis | Volume / Instances | Total Cost (INR) | % of Total Spend |
| :--- | :--- | :--- | :--- | :--- |
| **Direct Contact Handling** | Chat: Rs 210, Email: Rs 260, Voice: Rs 520, Social: Rs 240 | 11,780 tickets | **Rs 3,213,250** | 28.16% |
| **Customer Refunds** | Exact value credited via payment gateway / bank | 1,894 tickets | **Rs 5,332,723** | 46.72% |
| **Product Replacements** | Unit manufacturing cost + Rs 340 logistics | 1,102 units | **Rs 2,001,920** | 17.54% |
| **SLA Breach Penalty Credits** | Rs 350 auto store credit per breached first response | 1,340 breaches | **Rs 469,000** | 4.11% |
| **Internal Transfer Overhead** | Rs 305 per transfer (re-handling & administration) | 1,299 transfers | **Rs 396,195** | 3.47% |
| **Grand Total Operational Impact** | — | — | **Rs 11,413,088** | **100.0%** |

---

## 2. Direct Contact Handling Costs (§4)

In accordance with Support Operating Policy §4, channel-specific contact costs are defined as fully loaded unit rates:
- **Chat**: 5,387 contacts × Rs 210 = **Rs 1,131,270**
- **Email**: 3,555 contacts × Rs 260 = **Rs 924,300**
- **Voice Callback**: 1,702 contacts × Rs 520 = **Rs 885,040**
- **Social**: 1,136 contacts × Rs 240 = **Rs 272,640**
- **Blended Contact Cost**: **Rs 272.77** per ticket (policy planning benchmark is Rs 290).

---

## 3. Customer Concessions: Refunds & Replacements (§5)

### 3.1. Refund Volume and Reason Breakdown
A total of 1,894 tickets culminated in monetary refunds totaling **Rs 5,332,723**:

| Reason Code | Business Description | Ticket Count | Total Refund (INR) | Avg. Refund (INR) |
| :--- | :--- | :--- | :--- | :--- |
| `RETURN-QC-OK` | Product returned, verified by warehouse QC | 663 | Rs 2,427,337 | Rs 3,661 |
| `DUP-PAYMENT` | Duplicate gateway charge / checkout glitch | 498 | Rs 1,321,802 | Rs 2,654 |
| `CANCEL` | Pre-dispatch cancellation request | 303 | Rs 788,197 | Rs 2,601 |
| `LOST-TRANSIT` | Parcel confirmed lost/undelivered by carrier | 161 | Rs 443,439 | Rs 2,754 |
| `DOA-REPL` | Dead on arrival (<= 7 days), refund chosen | 108 | Rs 304,892 | Rs 2,823 |
| `PRICE-ADJ` | Post-purchase coupon/price match credit | 81 | Rs 28,350 | Rs 350 |
| `WTY-BUYBACK` | Warranty claim buyback (stock depleted) | 45 | Rs 13,706 | Rs 305 |
| `GW-OTHER` | Goodwill adjustment / miscellaneous exception | 35 | Rs 5,000 | Rs 143 |
| **Total** | — | **1,894** | **Rs 5,332,723** | **Rs 2,816** |

### 3.2. Replacement Costs (§5)
Per policy, replacement planning cost equals:
$$\text{Cost} = \text{Product Unit Cost (from products.csv)} + \text{Rs 340 (reverse pickup + forward shipping)}$$
1,102 replacements were dispatched, costing **Rs 2,001,920**. The top drivers were:
1. `VA-EB-PL1` (Pulse True Wireless Earbuds): 384 units (Unit Cost Rs 1,120 + 340 = Rs 1,460) -> Rs 560,640
2. `VA-EB-PL2` (Pulse 2 True Wireless Earbuds): 247 units (Unit Cost Rs 1,480 + 340 = Rs 1,820) -> Rs 449,540
3. `VA-HP-ST3` (Strata 3 Over-Ear): 112 units (Unit Cost Rs 2,650 + 340 = Rs 2,990) -> Rs 334,880
4. `VA-HP-ST2` (Strata 2 Over-Ear): 108 units (Unit Cost Rs 2,100 + 340 = Rs 2,440) -> Rs 263,520
5. `VA-SW-NX2` (Nexa 2 Smartwatch): 85 units (Unit Cost Rs 2,450 + 340 = Rs 2,790) -> Rs 237,150

### 3.3. Policy Leakage (Double Recovery Violations)
Two tickets violated Policy §5 by granting both a cash refund and a replacement unit:
- `TK-241926`: Rs 6,999 refund + Strata 2 replacement (Total cost: Rs 9,439)
- `TK-248344`: Rs 250 refund + Orbit Mini replacement (Total cost: Rs 1,570)
- Total unrecovered concession: Rs 11,009.

---

## 4. SLA Breach Penalties (§3)

Support Policy §3 mandates that every first-response target breach triggers an automatic Rs 350 store credit:
- Total breached tickets: **1,340** (11.38% overall breach rate).
- Total financial penalty: 1,340 × Rs 350 = **Rs 469,000**.
- **Channel Concentration**: Chat accounts for 53.7% of all breaches (720 tickets, Rs 252,000), driven by traffic spikes outside core shift hours.

---

## 5. The Routing Inefficiency Tax (Internal Transfers)

Under Support Operating Policy §4, each internal transfer carries a **Rs 305 re-handling cost**.
- Total recorded transfers in current helpdesk: **1,299 transfers**.
- Total transfer expenditure: **Rs 396,195**.
- **Intake Bot Misrouting Impact**:
  - The intake bot routed 2,564 tickets to Billing based on superficial keywords.
  - Billing transferred **795 tickets** directly to Logistics.
  - Re-handling waste for Billing-to-Logistics alone: 795 × Rs 305 = **Rs 242,475** (61.2% of all transfer costs!).
  - Customer impact: Adding a transfer added an average of **18.4 hours** to ticket resolution time.

---

## 6. Workforce Headcount Evaluation: The Two-Hire Business Case

Finance Controller Arjun Mehta established the headcount cost baseline:
$$\text{Cost of 2 Hires} = \text{Rs 9,00,000 / year (Rs 4,50,000 / agent-year)}$$

### Comparison of Staffing Options

| Metric | Option A: Add 2 Hires to Billing | Option B: Add 2 Hires to Logistics | Option C: Fix Routing & Process (AI Router) |
| :--- | :--- | :--- | :--- |
| **Annual Payroll Cost** | +Rs 9,00,000 | +Rs 9,00,000 | **Rs 0 added payroll** |
| **True Operational Bottleneck?** | **NO**. Billing median handle time is 23 min; resolving volume is only 1,838. | **YES**. Logistics median handle time is 24.5 hrs; resolved 2,673 tickets. | Solves root cause: eliminates 795 re-routing hand-offs. |
| **Workload Relief** | Adds capacity to an already overstaffed queue (4 agents resolving 1,838 tickets = 460 tickets/agent). | Directly alleviates drowning team (5 agents resolving 2,673 tickets = 535 tickets/agent + 24.5h backlog). | Automatically routes delivery queries directly to Logistics on day 1. |
| **Direct Cost Recovery** | Rs 0 | Faster carrier resolution, reduced SLA breach store credits. | **Recovers Rs 242,475/year** in wasted transfer costs + reduces carrier delay penalties. |

### Strategic Recommendation for Arjun Mehta:
As Arjun Mehta wisely noted: *"I'd rather fix a process than hire into it if that's an option."*
1. **Immediate Process Fix (AI Categorization & First-Touch Routing)**: Deploy the AI classifier at intake. This immediately eliminates ~800 unnecessary hand-offs, saving ~Rs 2.4 Lakh in re-handling waste, and cuts 20+ hours of lag for stranded delivery inquiries.
2. **Headcount Allocation**: If two hires are approved under Priya's stated mandate, they **must NOT be allocated to Billing**. Billing's volume was a data illusion created by the intake bot. Under operational reality, **Logistics is the team in acute operational distress** and requires the headcount.
