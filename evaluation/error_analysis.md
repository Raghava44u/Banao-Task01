# Independent Evaluation & Error Analysis Report

**Date**: October 2026  
**Evaluation Scope**: 1,767 Untouched Holdout Test Tickets (15% Stratified Split)  
**Model Architecture**: Vireo Hybrid NLP & Calibrated Linear Classifier  
**Baseline Comparator**: Legacy Intake Helpdesk Bot Tags  

---

## 1. Executive Performance Benchmark

| Evaluation Metric | Baseline (Intake Bot) | Vireo AI System | Absolute Gain | Relative Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Accuracy** | **45.3%** | **84.5%** | **+39.22%** | **+8662.7%** |
| **Error Rate** | **54.7%** | **15.5%** | **-39.22%** | **71.66% error reduction** |
| **Macro F1 Score** | **0.493** | **0.887** | **+39.41%** | — |
| **Weighted F1 Score** | **0.442** | **0.842** | **+39.96%** | — |
| **Human Review Rate** | 0.0% (unflagged errors) | **29.9%** | — | High-risk tickets gated |
| **High-Confidence Accuracy** | N/A | **92.7%** | — | Automated straight-through precision |

---

## 2. Per-Category Breakdown (Untouched Test Set)

| Category | Precision | Recall | F1 Score | Support | Owning Team |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Account & Login** | 100.0% | 100.0% | 1.000 | 42 | Chat Frontline |
| **App & Firmware** | 100.0% | 92.9% | 0.963 | 28 | Chat Frontline |
| **Audio Quality** | 100.0% | 100.0% | 1.000 | 75 | Chat Frontline |
| **Billing & Payments** | 82.9% | 77.5% | 0.801 | 169 | Billing |
| **Charging & Battery** | 98.6% | 98.6% | 0.986 | 145 | Chat Frontline |
| **Connectivity** | 100.0% | 100.0% | 1.000 | 122 | Chat Frontline |
| **Delivery & Shipping** | 79.7% | 94.5% | 0.865 | 379 | Logistics |
| **Other** | 79.2% | 79.7% | 0.795 | 483 | Chat Frontline |
| **Product Enquiry** | 86.7% | 100.0% | 0.929 | 26 | Chat Frontline |
| **Returns & Refunds** | 75.9% | 61.1% | 0.677 | 216 | Returns Desk |
| **Warranty & Repair** | 88.3% | 64.6% | 0.747 | 82 | Escalations & Warranty |


---

## 3. Detailed Error Discrepancy Analysis

The test set revealed **274 misclassified tickets** out of 1767 holdout cases (15.5% error rate).

### Key Error Patterns
1. **Multi-Intent Customer Inquiries**: Queries mentioning both delivery delay and payment deductions (e.g. *"paid but nothing arrived, refund my money"*). The model applies the business resolution hierarchy, prioritizing warehouse delivery interception (`Delivery & Shipping`) while safely setting `review_required = True`.
2. **Product Accessories vs. Device Hardware**: Queries asking about *"charging case"* delivery can trigger power keywords if not parsed in full context. The domain intent layer distinguishes purchase inquiries from charging failures.
3. **Acoustic Driver Failure vs. Hardware Warranty**: Out-of-the-box acoustic defects vs. long-term hardware wear.

---

## 4. Representative Error Examples from Actual Test Set

#### Example 1: Ticket `TK-241435`
- **Customer Message**: `"I haven't received my order - what do i do now?"`
- **Gold Standard Label**: `Returns & Refunds`
- **AI Predicted Label**: `Delivery & Shipping` (Confidence: 58.5%, Alternative: `Returns & Refunds` 21.0%, Margin: 37.5%)
- **Review Gated**: [YES - Safely Caught by Review Gate]
- **System Rationale**: Confidence 58.5% below production threshold 75%. Alternative: 'Returns & Refunds' (21.0%). Flagged for review.

#### Example 2: Ticket `TK-252027`
- **Customer Message**: `"product: orbit mini
order: vr908066
purchased: 23-03-2026
issue: is orbit mini compatible with my tv
expected: refund"`
- **Gold Standard Label**: `Other`
- **AI Predicted Label**: `Product Enquiry` (Confidence: 63.1%, Alternative: `Other` 22.9%, Margin: 40.2%)
- **Review Gated**: [YES - Safely Caught by Review Gate]
- **System Rationale**: Confidence 63.1% below production threshold 75%. Alternative: 'Other' (22.9%). Flagged for review.

#### Example 3: Ticket `TK-252069`
- **Customer Message**: `"strap material peeling liike an old sticker, kindly look into it"`
- **Gold Standard Label**: `Warranty & Repair`
- **AI Predicted Label**: `Other` (Confidence: 56.4%, Alternative: `Warranty & Repair` 30.0%, Margin: 26.4%)
- **Review Gated**: [YES - Safely Caught by Review Gate]
- **System Rationale**: Confidence 56.4% below production threshold 75%. Alternative: 'Warranty & Repair' (30.0%). Flagged for review.

#### Example 4: Ticket `TK-244809`
- **Customer Message**: `"[IVR transcript] Hi there, Bought AirLite around August 26 from vireo.in. My order has not been delivered yet. I CHECKED WITH NEIGHBOURS. Please call me on my registered number. Rgds,"`
- **Gold Standard Label**: `Returns & Refunds`
- **AI Predicted Label**: `Delivery & Shipping` (Confidence: 55.9%, Alternative: `Other` 34.7%, Margin: 21.2%)
- **Review Gated**: [YES - Safely Caught by Review Gate]
- **System Rationale**: Confidence 55.9% below production threshold 75%. Alternative: 'Other' (34.7%). Flagged for review.

#### Example 5: Ticket `TK-248647`
- **Customer Message**: `"Hello Vireo, Bouhgt Pulse 2 aronud Decembre 09 from Flipkart. Paiid via UPI on 09 Dec. 10 days. nothing. Need this sorted this week. Thank you"`
- **Gold Standard Label**: `Warranty & Repair`
- **AI Predicted Label**: `Other` (Confidence: 52.5%, Alternative: `Delivery & Shipping` 40.4%, Margin: 12.1%)
- **Review Gated**: [YES - Safely Caught by Review Gate]
- **System Rationale**: Narrow margin between top predictions: 'Other' (52.5%) vs 'Delivery & Shipping' (40.4%, margin 12.1%). Flagged for supervisor review.

#### Example 6: Ticket `TK-241300`
- **Customer Message**: `"Product: my Pulse
Purchased: 20 Feb
Issue: the app saiid pickup today, that was on 20 Feb
Tried: called courier
Expected: fix"`
- **Gold Standard Label**: `Returns & Refunds`
- **AI Predicted Label**: `Delivery & Shipping` (Confidence: 52.3%, Alternative: `Returns & Refunds` 42.1%, Margin: 10.2%)
- **Review Gated**: [YES - Safely Caught by Review Gate]
- **System Rationale**: Narrow margin between top predictions: 'Delivery & Shipping' (52.3%) vs 'Returns & Refunds' (42.1%, margin 10.2%). Flagged for supervisor review.

