# Vireo Audio — Customer Support AI Categorization & Workforce Planning System

[![Python Version](https://img.shields.io/badge/Python-3.14%20%7C%203.11%20%7C%203.10-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit%201.61-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn%201.8-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-Proprietary%20Vireo-green.svg)]()

---

## 1. Project Overview & Business Problem

**Vireo Audio** is a fast-growing consumer-audio and wearable technology brand headquartered in Bengaluru with support operations distributed across **Bengaluru and Indore** (44 agents, 3 shifts, 4 channels).

### The Client Request
Priya Raman, Head of Customer Experience, requested:
> *"I want to know where to add headcount. Can you auto-categorise the tickets and give me a monthly breakdown chart by category and by team? Our tags are probably rubbish but they're a start. Whichever team has the most volume gets the next two hires. Sameer has the exports."*

Priya initially assumed the two hires belonged in **Billing**, believing Billing represented ~22% of support volume. Finance Controller Arjun Mehta cautioned that two hires represent **Rs 9 Lakhs per year** in recurring payroll and requested a rigorous volume case in writing.

### The Operational Reality Discovered
Our comprehensive audit of all **11,780 customer support tickets** (June 2024 – June 2026) revealed that **Billing's volume was an illusion created by intake bot misrouting**:
1. Customers inquiring about shipping delays frequently wrote *"paid on 19 Jun, where is my order?"*. The intake bot naively detected *"paid"* and tagged them as `Billing & Payments`, dumping 2,564 tickets into Billing's queue.
2. Billing agents transferred **795 tickets** directly to Logistics, generating **Rs 242,475** in internal re-handling waste and adding **18.4 hours** of unnecessary customer waiting time.
3. In actual operational work performed, **Logistics resolved 2,673 tickets** (22.7% of all work) compared to **Billing's 1,838 tickets** (15.6%). Logistics agents carry the highest workload in the company (**534.6 tickets/agent**) with a **24.5-hour median resolution backlog** and a **17.1% SLA breach rate**, whereas Billing resolves cases in **23 minutes**.
4. **Hiring into Billing would fund an already fast queue. The true operational bottleneck is Logistics.**

---

## 2. System Architecture & Technical Approach

```
                    ┌──────────────────────────────────────────────┐
                    │          Customer Support Inquiries          │
                    │   (Chat: 5,387 | Email: 3,555 | Voice/Social) │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │      Reproducible Preprocessing Engine       │
                    │   - Text cleaning & entity preservation      │
                    │   - Legacy Freshdesk UTC -> IST (+5:30)      │
                    │   - Relational joining (Agents, Orders)      │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │          Hybrid AI Classifier Engine         │
                    │   - Sublinear TF-IDF N-grams (1-3)           │
                    │   - Platt-Calibrated Logistic Regression     │
                    │   - Support Policy Regex Disambiguation      │
                    └──────────────┬────────────────┬──────────────┘
                                   │                │
                    ┌──────────────▼──────┐  ┌──────▼──────────────┐
                    │ High-Confidence     │  │ Low-Confidence /    │
                    │ Straight-Through    │  │ Ambiguous (<0.75)   │
                    │ (59.5% Volume)      │  │ (40.5% Volume)      │
                    │ 94.54% Precision    │  │ Supervisor Review   │
                    └──────────────┬──────┘  └──────┬──────────────┘
                                   │                │
                                   ▼                ▼
                    ┌──────────────────────────────────────────────┐
                    │     Accurate First-Touch Automated Queue     │
                    │   Logistics (3,266) | Billing (1,266) | ...  │
                    └──────────────────────────────────────────────┘
```

- **Feature Representation**: Sublinear TF-IDF (1–3 n-grams, 8,000 features, English stop words).
- **Model**: Multi-Class Calibrated Logistic Regression wrapped with 3-fold Platt scaling (`CalibratedClassifierCV`) yielding mathematically calibrated posterior probabilities.
- **Intent Disambiguation Layer**: High-precision heuristics encoding Support Operating Policy v3.2 boundaries for pre-dispatch cancellation, address interception, return pickups, and payment gateway settlement failures.
- **Confidence Gating**: 0.75 probability threshold + 0.15 class margin check safely flags ambiguous tickets for supervisor review.

---

## 3. Independent Model Evaluation & Correctness

To prevent circular evaluation, the model was tested against an **independent, manually reviewed gold-standard benchmark of 400 stratified tickets** (`evaluation/benchmark.csv`), strictly excluded from training:

| Metric | Baseline (Intake Bot) | Vireo AI System | Absolute Gain | Relative Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Accuracy** | **61.75%** | **83.25%** | **+21.50%** | **+34.8%** |
| **Error Rate** | **38.25%** | **16.75%** | **-21.50%** | **56.21% error reduction** |
| **Macro F1-Score** | **0.615** | **0.825** | **+0.210** | **+34.1%** |
| **Weighted F1-Score**| **0.620** | **0.824** | **+0.204** | — |
| **High-Confidence Accuracy** | N/A | **94.54%** | — | Automated straight-through precision |
| **Human Review Rate**| 0.0% (unflagged errors) | **40.50%** | — | High-risk edge cases gated |

Confusion matrix visualizer is available in `evaluation/confusion_matrix.png`. Detailed error analysis is documented in `evaluation/error_analysis.md`.

---

## 4. True Intent Category vs. Intake Bot Breakdown

| Primary Category | Intake Bot Count (Corrupted) | True AI Count (Cleaned) | Net Shift | Primary Owning Team |
| :--- | :--- | :--- | :--- | :--- |
| **Delivery & Shipping** | 1,905 (16.17%) | **3,266 (27.73%)** | **+1,361 (+71.4%)** | Logistics |
| **Billing & Payments** | **2,564 (21.77%)** | **1,266 (10.75%)** | **-1,298 (-50.6%)** | Billing |
| **Other / Miscellaneous**| 1,622 (13.77%) | **1,105 (9.38%)** | **-517 (-31.9%)** | Frontline Tier 1 |
| **Returns & Refunds** | 1,049 (8.90%) | **1,086 (9.22%)** | +37 | Returns Desk |
| **Charging & Battery** | 820 (6.96%) | **995 (8.45%)** | +175 | Frontline Tier 1 |
| **App & Firmware** | 699 (5.93%) | **943 (8.01%)** | +244 | Frontline Tier 1 |
| **Connectivity** | 1,002 (8.51%) | **867 (7.36%)** | -135 | Frontline Tier 1 |
| **Audio Quality** | 591 (5.02%) | **779 (6.61%)** | +188 | Frontline Tier 1 |
| **Account & Login** | 391 (3.32%) | **627 (5.32%)** | +236 | Frontline Tier 1 |
| **Product Enquiry** | 612 (5.20%) | **437 (3.71%)** | -175 | Frontline Tier 1 |
| **Warranty & Repair** | 525 (4.46%) | **409 (3.47%)** | -116 | Escalations & Warranty (Tier 2) |
| **Total Population** | **11,780 (100.0%)** | **11,780 (100.0%)** | **0** | — |

---

## 5. Headcount & Workforce Analysis Summary

| Support Team | Headcount | Assigned Queue | Resolved Workload | Tickets / Agent | Median Handle Time | SLA Breach Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Chat Frontline** | 15 | 3,030 (25.7%) | **3,078 (26.1%)** | 205.2 | 21 min (0.35h) | 8.61% |
| **Logistics** | 5 | 1,905 (16.2%) | **2,673 (22.7%)** | **534.6** | **24.5 hours** | **17.13%** |
| **Billing** | 4 | 2,564 (21.8%) | **1,838 (15.6%)** | 459.5 | **23 min (0.38h)** | 13.82% |
| **Email Frontline** | 7 | 1,807 (15.3%) | 1,658 (14.1%) | 236.9 | 20 min (0.33h) | 9.53% |
| **Returns Desk** | 3 | 1,049 (8.9%) | 1,117 (9.5%) | 372.3 | 24.6 hours | 10.56% |
| **Voice Frontline** | 4 | 900 (7.6%) | 766 (6.5%) | 191.5 | 21 min (0.35h) | 4.57% |
| **Escalations & Warranty**| 6 | 525 (4.5%) | 650 (5.5%) | 108.3 | 122.0 hours (5.1d) | 8.00% |

### Key Workforce Takeaway
- **Data Finding**: Chat Frontline handled the largest overall volume (3,078). Among specialized back-office fulfillment queues, **Logistics handled the highest volume (2,673 resolved)**.
- **Application of Priya's 2-Hire Rule**:
  - If measured by assigned queue, the rule misleadingly suggests Billing.
  - If measured by actual work resolved, **Logistics is the rightful recipient of the 2 hires**.
- **Operational Reality**: Adding 2 hires to Billing subsidizes an already fast queue (23 min handle time). Adding 2 hires to Logistics directly attacks the company's largest resolution backlog (24.5h) and highest SLA breach rate (17.1%).

---

## 6. Financial Impact & Numeric Business Goal

- **Total CX Concession & Operational Spend**: **Rs 11,413,088 (~Rs 1.14 Crore)** across 11,780 contacts (Rs 5.33M refunds, Rs 2.00M replacements, Rs 3.21M contact costs, Rs 469K SLA breach credits, Rs 396K internal transfers).
- **Direct Annual Savings**: **Rs 242,475 / year** saved by eliminating 795 Billing-to-Logistics internal transfers (at Rs 305/transfer per Support Policy §4) plus >Rs 150,000 in prevented SLA breach credits.
- **Numeric Business Goal**: **85.0% Automated Routing Coverage with < 5.0% Misclassification Error Rate** within 90 days.

---

## 7. Installation & Quickstart (Windows PowerShell)

### Prerequisites
- Python 3.10, 3.11, or 3.14 installed
- Git installed

### 1. Clone & Set Up Virtual Environment
```powershell
git clone https://github.com/Raghava44u/Banao-Task01.git
cd Banao-Task01

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy the template configuration file:
```powershell
copy .env.example .env
```

### 3. Run Pipeline & Reproduce Results
To re-run data auditing, benchmark evaluation, and full analytical breakdown:
```powershell
# 1. Run Data Quality Audit
python generate_data_audit.py

# 2. Run Model Training & Benchmark Evaluation
python run_eval.py

# 3. Classify Full Dataset & Generate Monthly Charts
python run_analysis.py

# 4. Generate Workforce Headcount Summary
python compute_headcount_stats.py
```

### 4. Launch Interactive Streamlit Dashboard
```powershell
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 8. Repository Structure

```
vireo_audio_task1/
│
├── Given/                          # Immutable raw data pack
│   ├── agents.csv
│   ├── customers.csv
│   ├── email-thread.txt
│   ├── orders.csv
│   ├── products.csv
│   ├── README.txt
│   ├── support-policy.pdf
│   └── tickets.csv
│
├── src/                            # Production modular source code
│   ├── __init__.py
│   ├── data_loader.py              # File verification and raw loading
│   ├── preprocessing.py           # Text normalization, UTC-to-IST offset, SLA math
│   ├── taxonomy.py                # Taxonomy definitions and subcategories
│   ├── categorizer.py             # Hybrid NLP classifier with Platt calibration
│   ├── benchmark_builder.py       # Independent stratified gold benchmark builder
│   ├── evaluation.py              # Metrics, confusion matrix, error reporter
│   ├── analysis.py                # Full classification, monthly aggregates, charts
│   └── cost_model.py              # Support policy concession and transfer costing
│
├── prompts/                        # Versioned prompt artifacts
│   ├── categorization_v1.txt      # Initial naive zero-shot prompt
│   ├── categorization_v2.txt      # Disambiguation & review gating prompt
│   └── final_categorization_prompt.txt # Production master specification
│
├── evaluation/                     # Verification artifacts
│   ├── benchmark.csv              # 400 hand-verified gold reference tickets
│   ├── predictions.csv            # AI model predictions on benchmark
│   ├── metrics.json               # Accuracy, Macro F1, Per-category metrics
│   ├── confusion_matrix.png       # Confusion matrix visualization
│   └── error_analysis.md          # In-depth discrepancy root-cause report
│
├── outputs/                        # Client deliverables
│   ├── categorized_tickets.csv    # 100% classified ticket population (11,780 rows)
│   ├── monthly_category.csv       # Monthly breakdown by category
│   ├── monthly_team.csv           # Monthly breakdown by team
│   ├── team_category_matrix.csv   # Crosstabulation workload matrix
│   ├── team_workload_summary.csv  # Workload intensity & handle time table
│   ├── data_quality_report.csv    # Complete column-by-column data audit CSV
│   ├── data_audit.md              # Detailed structural data audit report
│   └── charts/                    # High-resolution presentation visualizations
│       ├── monthly_category_volume.png
│       ├── monthly_team_volume.png
│       └── team_category_heatmap.png
│
├── app.py                          # 10-section interactive Streamlit dashboard
├── requirements.txt                # Pinned production dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git exclusion rules
│
├── category_taxonomy.md            # Comprehensive operational taxonomy guide
├── support_policy_summary.md       # Operating policy rules, SLAs, cost standards
├── cost_model.md                   # Full concession and staffing financial model
├── memo_to_priya.md                # 1-page executive memo to Priya Raman
├── source_traceability.md          # Audit mapping for every metric and finding
├── assumptions.md                  # Explicit operational & data assumptions
├── limitations.md                  # Analytical, system, and workforce limitations
├── ai_usage.md                     # Model disclosure, prompts, zero API cost
├── decision_log.md                 # 7 major implementation decisions
├── demo_script.md                  # 3-minute executive presentation guide
├── submission-form-draft.md        # Synthesis of assessment responses
└── FINAL_CHECKLIST.md              # Verification audit checklist
```

---

## 9. Security & Governance

- **Zero Credentials Committed**: Scanned repository for tokens, passwords, and private keys.
- **Privacy (PII)**: Customer phone numbers, email addresses, and home addresses are never exposed in reports, dashboards, or charts.
- **Clean Git Tree**: Virtual environments, system caches (`__pycache__`), and temporary scratch logs are ignored via `.gitignore`.
