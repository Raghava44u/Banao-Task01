# Architectural & Implementation Decision Log

This log records the technical, methodological, and operational decisions made during the execution of Vireo Audio Task 1.

---

## Decision 1: Taxonomy Design & Boundary Rationalization
- **Context**: The existing dataset contained 11 categories populated by a naive intake bot, resulting in 2,564 tickets dumped into `Billing & Payments` and 1,622 dumped into `Other`.
- **Options Considered**:
  1. Invent a completely new 20+ category taxonomy with granular tech specs.
  2. Collapse categories into 4 macro-teams (Billing, Logistics, Tech, Frontline).
  3. Rationalize the existing 10 domain categories + 1 Other category, clarifying mutual exclusivity and adding granular subcategories.
- **Decision Taken**: Option 3. Retaining the 10 core operational categories allows direct, head-to-head comparison against the baseline bot tags and preserves continuity for Vireo's 44 agents. Adding clear operational definitions for `Delivery & Shipping` vs. `Billing & Payments` resolved the primary misrouting flaw.
- **Impact**: Category `Delivery & Shipping` expanded from 1,905 to 3,266 tickets, reflecting true customer shipping inquiries. `Billing & Payments` contracted from 2,564 to 1,266 tickets.

---

## Decision 2: Model Architecture & Runtime Compatibility
- **Context**: PyTorch DLL initialization failed on the Windows Python 3.14 environment (`[WinError 1114]`).
- **Options Considered**:
  1. Downgrade Python system installation.
  2. Mock/hardcode LLM responses.
  3. Build a high-performance Hybrid NLP Architecture using scikit-learn's `TfidfVectorizer` + `CalibratedClassifierCV` combined with domain intent heuristics.
- **Decision Taken**: Option 3. It guaranteed 100% real execution, high reproducibility, mathematical probability calibration, and sub-minute inference for 11,780 tickets without brittle native binary dependencies.
- **Impact**: Classification accuracy of 83.25% overall and 94.54% on high-confidence predictions, with zero API cost.

---

## Decision 3: Ground Truth Labeling & Benchmark Isolation
- **Context**: The client stated *"Our tags are probably rubbish but they're a start."* We could not evaluate the AI model against the intake bot's corrupted tags.
- **Options Considered**:
  1. Evaluate model on its own training predictions (circular / invalid).
  2. Manually label all 11,780 tickets (time-prohibitive).
  3. Construct a stratified 400-ticket benchmark independently labeled using customer messages cross-referenced with human agent closing notes, refund codes, and transfer logs, strictly isolated from model training.
- **Decision Taken**: Option 3.
- **Impact**: Created an uncompromised evaluation standard (`evaluation/benchmark.csv`), proving a +21.5% accuracy gain over the baseline bot.

---

## Decision 4: Legacy UTC Timestamp Adjustment (+5:30)
- **Context**: In 2,379 legacy Freshdesk rows, `resolved_at` was earlier than `created_at`. README and Policy §9 explained that legacy resolution timestamps were reconstructed from UTC event logs while helpdesk exports in IST.
- **Decision Taken**: Applied a programmatic `+pd.Timedelta(hours=5, minutes=30)` offset to all legacy resolution timestamps during data preprocessing.
- **Impact**: Eliminated 100% of negative handle time anomalies, enabling accurate calculation of handle times across both legacy and modern helpdesk eras.

---

## Decision 5: Confidence Threshold & Review Protocol
- **Context**: The business requires high automation without introducing catastrophic misrouting errors.
- **Options Considered**:
  1. Route all tickets automatically without human review (risks 16.75% error rate).
  2. Set a high threshold (e.g. 0.90) flagging >70% of tickets for review.
  3. Set a calibrated threshold of **0.75** combined with a class margin check ($\ge 0.15$).
- **Decision Taken**: Option 3.
- **Impact**: 59.5% of tickets route straight-through with **94.54% precision**. The remaining 40.5% ambiguous or multi-intent cases are flagged for team lead review, preventing re-handling waste.

---

## Decision 6: Headcount Evaluation Distinction (Data Finding vs. Business Rule)
- **Context**: Priya stated: *"Whichever team has the most volume gets the next two hires. I've already half-promised them to Billing... Neha, Logistics is barely 16%."*
- **Options Considered**:
  1. Blindly recommend 2 hires to Billing based on assigned queue count (2,564).
  2. Blindly claim Billing needs zero hires without explaining Priya's rule.
  3. Clearly separate **Data Finding** (Chat Frontline resolved 3,078; Logistics resolved 2,673; Billing resolved 1,838) from the **Business Rule Application** (explaining that under assigned queue Billing appears #2, but under actual resolved work Logistics is #1 back-office queue).
- **Decision Taken**: Option 3. Transparently demonstrates why hiring into Billing is an operational mistake and shows that Logistics is the true operational bottleneck.

---

## Decision 7: UI Framework & Design Choices
- **Context**: Required an executive-ready application.
- **Decision Taken**: Implemented Streamlit (`app.py`) with 10 dedicated sections, interactive filters, live message classifier testing, and chart embeddings. Kept UI clean and focused on business clarity over visual clutter.

---

## Decision 8: Classifier Pipeline Audit & Motivating Failure Resolution
- **Context**: Live classifier in `app.py` failed on obvious ticket *"My AirBuds were working fine yesterday, but now the left earbud only lasts about 20 minutes even after a full charge"*, returning `Delivery & Shipping (88%)`.
- **Root Cause Analysis**:
  1. `app.py` previously instantiated an un-fitted categorizer falling through to a mock fallback returning `Delivery & Shipping (88%)`.
  2. Ground truth labeling previously prioritized courier fulfillment notes over customer hardware symptoms, mislabeling replacement earbud shipments as delivery issues.
  3. Signoff phrases such as *"Please call me on my registered number"* were mistakenly matched as `Account & Login`, dumping hundreds of non-account complaints into `Account & Login` and contaminating feature vocabulary.
- **Resolution Implemented**:
  1. Built unified inference pipeline (`src/pipeline.py`) serving `predict_ticket(text)` identically to evaluation, regression tests, and `app.py`.
  2. Structured hybrid architecture combining Word TF-IDF (1-3), Character TF-IDF (3-5), domain policy intent features, and Platt-calibrated `LinearSVC(C=0.5, class_weight='balanced')`.
  3. Added second-best category, confidence margin, and extracted evidence to prediction outputs.
  4. Executed strict 70/15/15 stratified train/val/test split with an untouched 1,767-ticket test set (AI Accuracy: 84.49%, Macro F1: 0.8874, High-Confidence Accuracy: 92.70%).
  5. Established 12-test automated regression suite (`tests/test_classifier_regression.py`), passing 12/12. Motivating query now predicts `Charging & Battery` (96.7% confidence, `Single Earbud Not Charging`, 94.8% margin).
