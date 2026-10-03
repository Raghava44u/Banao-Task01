# Vireo Audio Take-Home Assessment — Submission Form (Draft)

> **NOTICE**: The official `submission-form.md` was **not present** in the supplied files in `Given/` or the project repository. As instructed in Section 39 of the prompt specification, this document serves as a clearly identified **Draft Submission Form** synthesizing all required assessment results, metrics, and deliverables.

---

## 1. Candidate & Project Information
- **Project Name**: Vireo Audio Support Ticket Categorization & Workforce Planning
- **Candidate / Lead**: Kabir Nanda / Antigravity AI Autonomous Coding System
- **Date**: October 2026
- **Repository URL**: https://github.com/Raghava44u/Banao-Task01.git
- **Target Branch**: `main`

---

## 2. Executive CX Summary & Headcount Recommendation
- **Business Question**: Where should Vireo Audio add the next two support hires based on ticket volume?
- **Priya's Initial Assumption**: Billing queue was the largest at ~22% of tickets, so hires should go there.
- **Data Finding**:
  - Billing’s 2,564 assigned tickets (21.77%) were an artifact of intake bot keyword misclassification (e.g. classifying *"paid on 19 Jun, where is my tracking"* as Billing).
  - Billing agents transferred **795 tickets** to Logistics.
  - Billing actually resolved only **1,838 tickets** (15.60%) with a median handle time of **23 minutes**.
  - **Logistics actually resolved 2,673 tickets** (22.69% of all company work) with a median handle time of **24.5 hours** and an SLA breach rate of **17.13%**.
- **Headcount Rule Application**:
  - Under Priya's rule of awarding hires to the highest-volume team:
    - Overall company volume: **Chat Frontline (3,078 resolved)**.
    - Specialized back-office volume: **Logistics (2,673 resolved)**.
    - Billing is **not** the highest-volume queue under actual work performed.
- **Strategic Recommendation**:
  - Do NOT allocate hires to Billing.
  - Allocate approved hires to **Logistics** to alleviate the 24.5-hour backlog.
  - Deploy the AI first-touch router immediately to eliminate 795 hand-offs and recover Rs 242,475 in annual transfer costs.

---

## 3. Categorization Performance & Evaluation Metrics
- **Dataset Size**: 11,780 customer tickets (100% classified in `outputs/categorized_tickets.csv`).
- **Benchmark Size**: 1,767 tickets in untouched, independent 15% holdout test set (`evaluation/benchmark.csv`).
- **AI Model Accuracy**: **84.49%** (+39.22% absolute gain over baseline intake bot's 45.27%).
- **Macro F1-Score**: **0.8874** (vs. 0.4897 baseline bot).
- **Weighted F1-Score**: **0.8514** (vs. 0.4396 baseline bot).
- **Error Rate**: **15.51%** (a 71.68% relative reduction in errors).
- **High-Confidence Straight-Through Accuracy**: **92.70%** (confidence >= 0.75, margin >= 0.15).
- **Human Review Gating Rate**: **28.41%** of complex/ambiguous tickets safely routed for supervisor review.
- **Regression Suite**: 12/12 passing in `tests/test_classifier_regression.py`.

---

## 4. True Intent Category Breakdown (11,780 Tickets)
1. `Other / Non-Actionable`: **3,229 tickets (27.41%)**
2. `Delivery & Shipping`: **2,969 tickets (25.20%)**
3. `Returns & Refunds`: **1,172 tickets (9.95%)**
4. `Billing & Payments`: **1,088 tickets (9.24%)**
5. `Charging & Battery`: **971 tickets (8.24%)**
6. `Connectivity`: **816 tickets (6.93%)**
7. `Audio Quality`: **500 tickets (4.24%)**
8. `Warranty & Repair`: **388 tickets (3.29%)**
9. `Account & Login`: **278 tickets (2.36%)**
10. `Product Enquiry`: **185 tickets (1.57%)**
11. `App & Firmware`: **184 tickets (1.56%)**

---

## 5. Numeric Business Goal
- **Measurable Goal**: **85.0% Automated Straight-Through Routing Coverage with < 5.0% Misclassification Error Rate** within 90 days of deployment.
- **Observed Result**: 59.5% automation at 94.54% precision; overall accuracy 83.25%.
- **Target**: Increase automation to 85.0% via active learning retraining.
- **Financial Benefit**: Rs 242,475 direct savings in internal transfer overhead + Rs 150,000 in SLA penalty avoidance.

---

## 6. Financial & Support Policy Compliance Findings
- **Total Concessions & Support Operational Spend**: Rs 11,413,088 across 11,780 tickets.
- **Customer Cash Refunds**: Rs 5,332,723 across 1,894 refund tickets.
- **Product Replacements**: Rs 2,001,920 across 1,102 replacement dispatches.
- **SLA Breach Penalty Credits**: Rs 469,000 across 1,340 first-response breaches (at Rs 350/breach).
- **Internal Transfer Overhead**: Rs 396,195 across 1,299 recorded transfers.
- **Policy Violations Uncovered**: 2 tickets (`TK-241926` and `TK-248344`) received both a refund and a replacement in violation of Support Policy §5.

---

## 7. Deliverables Checklist
- [x] Streamlit Application (`app.py`)
- [x] Executive Memo (`memo_to_priya.md`)
- [x] Category Taxonomy Guide (`category_taxonomy.md`)
- [x] Support Policy Summary (`support_policy_summary.md`)
- [x] Financial Cost Model (`cost_model.md`)
- [x] Data Audit Report & CSV (`outputs/data_audit.md`, `outputs/data_quality_report.csv`)
- [x] Full Classified Tickets (`outputs/categorized_tickets.csv`)
- [x] Monthly Breakdown CSVs & Charts (`outputs/monthly_category.csv`, `outputs/monthly_team.csv`, `outputs/charts/`)
- [x] Independent Benchmark & Evaluation (`evaluation/benchmark.csv`, `evaluation/predictions.csv`, `evaluation/metrics.json`, `evaluation/confusion_matrix.png`, `evaluation/error_analysis.md`)
- [x] Source Traceability Matrix (`source_traceability.md`)
- [x] Assumptions & Limitations (`assumptions.md`, `limitations.md`)
- [x] AI Usage Disclosure (`ai_usage.md`)
- [x] Decision Log (`decision_log.md`)
- [x] Demo Script (`demo_script.md`)
