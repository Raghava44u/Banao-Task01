# Analytical, Data & System Limitations

This document outlines the known limitations of the available datasets, analytical models, and operational workforce planning methods.

---

## 1. Data Availability & Structural Limitations

1. **Absence of Legacy Transfers Data**:
   - The `transfers` field was introduced only after the migration to the current helpdesk on 14 September 2025. All 4,052 tickets from the legacy Freshdesk era (`legacy_fd`) have blank transfer counts. Consequently, transfer volume (1,299) and transfer cost waste (Rs 396,195) reflect only the 9.5-month modern helpdesk period and represent an **underestimate of total historical transfer waste**.

2. **Absence of Step-by-Step Touch Times**:
   - The dataset provides `created_at`, `first_response_at`, and `resolved_at`, but does not record individual agent touch times (active seconds spent reading or typing). Handle time represents total ticket lifecycle (first response to resolution) and includes customer waiting time.

3. **Multi-Touch Complexity in Tier 2 (Escalations & Warranty)**:
   - As mandated by Support Operating Policy §6, Tier 2 cases are multi-touch, certified hardware investigations measured on resolution in days (median 122 hours), not tickets closed per week. Evaluating Tier 2 on raw ticket volume alone severely distorts their actual workload intensity.

---

## 2. Model & Algorithmic Limitations

1. **Short & Ambiguous Customer Messages**:
   - Inquiries with minimal text (e.g., *"not working"*, *"help please"*, or one-word IVR transcripts) lack sufficient linguistic context for definitive automated categorization. These must be caught by the human review gate.

2. **Multi-Intent Compromise**:
   - Single-label categorization forces a ticket with both a product complaint (*"sound is muffled"*) and a commercial demand (*"cancel order and refund"*) into a single primary category. While subcategories capture nuance, helpdesk intake systems inherently require single-queue routing.

3. **Static Model Adaptation**:
   - The current model is trained on historical data up to June 2026. Sudden shifts in product hardware (e.g. new product launches like a hypothetical *Pulse 3* or *Orbit 2*) will require retraining to incorporate new product names and vocabulary.

---

## 3. Workforce Planning Limitations of Volume-Only Staffing

1. **Flaw of Naive Queue Sizing**:
   - As demonstrated by this case study, basing headcount allocations strictly on unverified queue volume rewards poor routing rather than actual operational need. If Priya had executed the two-hire rule based on initial assigned queue, Rs 9.0 Lakhs in payroll would have been added to an already fast queue (Billing) while the true operational bottleneck (Logistics) remained unresolved.

2. **Complexity vs. Volume Blindspot**:
   - 100 simple billing questions resolved in 20 minutes require far fewer staffing resources than 20 complex lost-in-transit courier claims taking 48 hours of carrier coordination. Headcount planning must incorporate **Resolution Complexity** and **Handling Effort**, not ticket counts alone.
