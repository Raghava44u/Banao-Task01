# Vireo Audio CX Analytics — Source Traceability Matrix

This document provides complete, line-by-line auditability and source traceability for every business finding, metric, and financial figure presented in `memo_to_priya.md`, `cost_model.md`, and the analytical outputs.

---

## 1. Population & Structural Metrics

### Finding 1.1: Total Ticket Population = 11,780 tickets
- **Source File**: `Given/tickets.csv`
- **Relevant Columns**: `ticket_id`
- **Transformation**: Count distinct primary keys.
- **Calculation**: `len(tickets['ticket_id'].unique()) = 11,780`.
- **Validation**: Reconciles with helpdesk export count (7,728 helpdesk + 4,052 legacy_fd).

### Finding 1.2: Total Agents = 44 agents (25 Bengaluru, 19 Indore)
- **Source File**: `Given/agents.csv`
- **Relevant Columns**: `agent_id`, `site`, `team`, `shift`
- **Transformation**: Group by `site` and count distinct `agent_id`.
- **Calculation**: 
  - Total: `len(agents['agent_id'].unique()) = 44`
  - Bengaluru: `sum(agents['site'] == 'Bengaluru') = 25`
  - Indore: `sum(agents['site'] == 'Indore') = 19`.

### Finding 1.3: Customer & Order Counts = 9,500 Customers, 15,000 Orders
- **Source Files**: `Given/customers.csv`, `Given/orders.csv`
- **Relevant Columns**: `customers.customer_id`, `orders.order_id`
- **Transformation**: Unique row count of primary keys.
- **Calculation**: `len(customers) = 9,500`, `len(orders) = 15,000`.

---

## 2. Categorization & Routing Metrics

### Finding 2.1: Legacy Intake Bot Assigned Queue to Billing = 2,564 tickets (21.77%)
- **Source File**: `Given/tickets.csv`
- **Relevant Columns**: `assigned_team`, `category`
- **Transformation**: Group by `assigned_team` and count rows.
- **Calculation**: `sum(tickets['assigned_team'] == 'Billing') = 2,564` (2,564 / 11,780 = 21.77%).
- **Cross-Check**: Matches exactly `sum(tickets['category'] == 'Billing & Payments') = 2,564`.

### Finding 2.2: True AI Delivery & Shipping Volume = 3,266 tickets (27.73%)
- **Source File**: `outputs/categorized_tickets.csv`
- **Relevant Columns**: `category` (AI predicted)
- **Transformation**: Frequency count of `category` column.
- **Calculation**: `sum(categorized_tickets['category'] == 'Delivery & Shipping') = 3,266` (3,266 / 11,780 = 27.73%).

### Finding 2.3: True AI Billing & Payments Volume = 1,266 tickets (10.75%)
- **Source File**: `outputs/categorized_tickets.csv`
- **Relevant Columns**: `category` (AI predicted)
- **Transformation**: Frequency count of `category` column.
- **Calculation**: `sum(categorized_tickets['category'] == 'Billing & Payments') = 1,266` (1,266 / 11,780 = 10.75%).

### Finding 2.4: Misrouted Tickets from Billing to Logistics = 795 tickets
- **Source Files**: `Given/tickets.csv`, `Given/agents.csv`
- **Relevant Columns**: `tickets.assigned_team`, `tickets.agent_id`, `agents.team`
- **Transformation**: Inner join on `agent_id`; filter for `assigned_team == 'Billing'` and resolving agent `agents.team == 'Logistics'`.
- **Calculation**: `len(df[(df['assigned_team'] == 'Billing') & (df['resolving_team'] == 'Logistics')]) = 795`.

---

## 3. Team Workload & Productivity Metrics

### Finding 3.1: Actual Resolved Workload by Team
- **Source Files**: `Given/tickets.csv`, `Given/agents.csv`
- **Relevant Columns**: `tickets.agent_id`, `agents.team`
- **Transformation**: Join `tickets` with `agents` on `agent_id`; count distinct `ticket_id` grouped by `agents.team`.
- **Calculation**:
  - `Chat Frontline`: 3,078 (26.13%)
  - `Logistics`: 2,673 (22.69%)
  - `Billing`: 1,838 (15.60%)
  - `Email Frontline`: 1,658 (14.07%)
  - `Returns Desk`: 1,117 (9.48%)
  - `Voice Frontline`: 766 (6.50%)
  - `Escalations & Warranty`: 650 (5.52%)
  - Total: 11,780 (100.0%).

### Finding 3.2: Tickets per Agent (Workload Intensity)
- **Source Files**: `outputs/team_workload_summary.csv`, `Given/agents.csv`
- **Relevant Columns**: `resolving_volume`, `agent_headcount`
- **Transformation**: Ratio of `resolving_volume / agent_headcount`.
- **Calculation**:
  - `Logistics`: 2,673 tickets / 5 agents = **534.6 tickets/agent**
  - `Billing`: 1,838 tickets / 4 agents = **459.5 tickets/agent**
  - `Returns Desk`: 1,117 tickets / 3 agents = **372.3 tickets/agent**
  - `Email Frontline`: 1,658 tickets / 7 agents = **236.9 tickets/agent**
  - `Chat Frontline`: 3,078 tickets / 15 agents = **205.2 tickets/agent**
  - `Voice Frontline`: 766 tickets / 4 agents = **191.5 tickets/agent**
  - `Escalations & Warranty`: 650 tickets / 6 agents = **108.3 tickets/agent**.

### Finding 3.3: Median Resolution Time (Handle Time)
- **Source File**: `outputs/categorized_tickets.csv`
- **Relevant Columns**: `created_at`, `resolved_at`, `source_system`, `resolving_team`
- **Transformation**: Parse dates; apply +5:30 offset to `legacy_fd` resolution dates; calculate `(resolved_dt - first_resp_dt)` in hours; group by `resolving_team` and compute median.
- **Calculation**:
  - `Logistics`: **24.47 hours** (mean 41.06 hours)
  - `Returns Desk`: **24.55 hours** (mean 37.10 hours)
  - `Billing`: **0.38 hours (23.0 min)** (mean 11.03 hours)
  - `Chat Frontline`: **0.35 hours (21.0 min)** (mean 4.84 hours)
  - `Email Frontline`: **0.33 hours (20.0 min)** (mean 5.19 hours)
  - `Voice Frontline`: **0.35 hours (21.0 min)** (mean 3.69 hours)
  - `Escalations & Warranty`: **122.0 hours (5.1 days)** (mean 141.63 hours).

---

## 4. Evaluation & Accuracy Metrics

### Finding 4.1: AI Model Accuracy = 83.25% vs Baseline 61.75%
- **Source Files**: `evaluation/benchmark.csv`, `evaluation/predictions.csv`, `evaluation/metrics.json`
- **Relevant Columns**: `gold_category`, `ai_predicted_category`, `baseline_bot_category`
- **Transformation**: `sklearn.metrics.accuracy_score` on 400 stratified samples.
- **Calculation**:
  - `AI Model Accuracy`: 333 / 400 = **0.8325 (83.25%)**
  - `Baseline Bot Accuracy`: 247 / 400 = **0.6175 (61.75%)**
  - `Absolute Gain`: 83.25% - 61.75% = **+21.50%**.

### Finding 4.2: High-Confidence Subset Accuracy = 94.54%
- **Source File**: `evaluation/predictions.csv`
- **Relevant Columns**: `confidence`, `review_required`, `ai_correct`
- **Transformation**: Filter for `review_required == False` (confidence >= 0.75); compute mean of `ai_correct`.
- **Calculation**: 225 correct / 238 high-confidence tickets = **0.9454 (94.54%)**.

---

## 5. Financial Cost Model & Policy Concessions

### Finding 5.1: Total Concession P&L Impact = Rs 11,413,088
- **Source Files**: `outputs/categorized_tickets.csv`, `Given/support-policy.pdf` §3, §4, §5
- **Transformation**: Sum of Contact Costs, Refunds, Replacements, SLA Credits, and Transfers.
- **Calculation**:
  - Contact Handling Costs: Rs 3,213,250
  - Customer Cash Refunds: Rs 5,332,723
  - Product Replacements: Rs 2,001,920
  - SLA Breach Penalty Credits: Rs 469,000
  - Internal Transfer Costs: Rs 396,195
  - **Sum Total**: **Rs 11,413,088**.

### Finding 5.2: Wasted Billing-to-Logistics Transfer Overhead = Rs 242,475
- **Source Files**: `Given/tickets.csv`, `Given/support-policy.pdf` §4
- **Relevant Columns**: `assigned_team`, `agent_id`
- **Transformation**: 795 misrouted transfers × policy transfer standard of Rs 305/transfer.
- **Calculation**: `795 × 305 = Rs 242,475`.

### Finding 5.3: Annual Cost of 2 Hires = Rs 9,00,000 (Rs 4,50,000 / hire)
- **Source File**: `Given/email-thread.txt`
- **Source Text**: Statement by Finance Controller Arjun Mehta: *"Two hires is about Rs 9 lakh a year."*
- **Calculation**: `Rs 9,00,000 / 2 = Rs 4,50,000 / FTE-year`.
