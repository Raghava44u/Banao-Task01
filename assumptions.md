# Operational & Analytical Assumptions

This document explicitly details all business, operational, and data modeling assumptions utilized throughout the Vireo Audio CX analysis.

---

## 1. Workforce & Financial Cost Assumptions

1. **Annual Headcount Cost**:
   - **Assumption**: A full-time support hire carries an annual fully loaded employment cost of **Rs 4,50,000 / year** (Rs 37,500 / month).
   - **Source**: Statement by Finance Controller Arjun Mehta in `Given/email-thread.txt`: *"Two hires is about Rs 9 lakh a year."*
   - **Reconciliation**: Aligns closely with Support Operating Policy §4 loaded rate of Rs 165/agent-hour across ~260 standard 8-hour shifts plus benefits and overhead.

2. **Internal Transfer Overhead**:
   - **Assumption**: Every internal transfer between support teams incurs a re-handling and administrative cost of **Rs 305 per transfer**.
   - **Source**: Customer Support Operating Policy v3.2 §4.

3. **Direct Contact Handling Rates**:
   - **Assumption**: Fully loaded costs per contact are fixed by channel per Policy §4:
     - Chat: Rs 210
     - Social: Rs 240
     - Email: Rs 260
     - Voice Callback: Rs 520
     - Blended Planning Average: Rs 290.

4. **Product Replacement Logistics**:
   - **Assumption**: Replacement cost for business planning equals the product unit manufacturing cost (from `Given/products.csv`) plus **Rs 340** for reverse pickup and forward courier transit, with **zero refurbishment recovery** assumed (Policy §5).

5. **SLA Breach Penalties**:
   - **Assumption**: Every ticket missing its channel first-response target (Chat: 15m, Voice: 2h, Social: 4h, Email: 8h) incurs a **Rs 350 automatic store credit** charged to the support P&L (Policy §3).

---

## 2. Data Engineering & Timestamp Assumptions

1. **Legacy UTC to IST Reconciliation**:
   - **Assumption**: In `legacy_fd` records (prior to 14 September 2025), `resolved_at` timestamps were reconstructed from UTC database event logs, whereas `created_at` was stored in IST. Adding **5 hours and 30 minutes** (+5:30) converts `resolved_at` to Indian Standard Time (IST), resolving all negative handle time discrepancies.
   - **Source**: Customer Support Operating Policy v3.2 §9 and `Given/README.txt`.

2. **CSAT Survey Non-Response**:
   - **Assumption**: Missing values in `csat_score` represent customer non-responses (~45% response rate) and must be excluded from average CSAT calculations rather than treated as zero (Policy §8).

3. **Fallback Order Linkage**:
   - **Assumption**: For tickets where `order_id` is blank (4,017 tickets), customer identity and product purchased can be reliably linked via `customer_id + product_sku` against `Given/orders.csv`.

---

## 3. Categorization & Routing Assumptions

1. **Intent Priority Hierarchy**:
   - **Assumption**: When a customer's opening message contains multiple complaints, operational resolution follows this priority order: (1) Pre-dispatch order cancellation / address interception, (2) Post-delivery return / refund follow-up, (3) Payment gateway transaction failure / tax invoice, (4) In-warranty RMA hardware claim, (5) Technical product failure (charging, audio, bluetooth, app).

2. **Human Review Threshold**:
   - **Assumption**: A confidence score threshold of **0.75** (or class probability margin < 0.15) provides an optimal operational trade-off: safely automating ~60% of tickets at 94.5% precision while routing the remaining 40% of complex cases to team lead triage.
