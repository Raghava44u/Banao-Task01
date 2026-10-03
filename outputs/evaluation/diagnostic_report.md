# Diagnostic Audit Report: Classifier Architecture & Root-Cause Failure Analysis

**Date**: October 2026  
**Investigator**: Lead CX AI Systems Engineer (Antigravity Autonomous Agent)  
**System Investigated**: Vireo Audio Support Ticket Categorization & Workforce Routing Engine  

---

## 1. Executive Summary: The Immediate Root Cause

During manual testing of the query:
> *"My AirBuds were working fine yesterday, but now the left earbud only lasts about 20 minutes even after a full charge."*

The live Streamlit application incorrectly reported:
- **Category**: `Delivery & Shipping`
- **Subcategory**: `Tracking & Delay`
- **Confidence**: `88%`
- **Review Required**: `No`

### The Critical Root Cause
Inspection of `app.py` lines 198–208 revealed a catastrophic flaw in the live inference path:
```python
if st.button("Run AI Classification", type="primary"):
    from src.categorizer import VireoTicketCategorizer
    cat_engine = VireoTicketCategorizer()
    # Mock prediction using engine rule or ML logic
    rule = cat_engine._extract_intent_rules(test_input)
    if rule:
        cat, sub, reason, ev, conf = rule
        rev = False if conf >= 0.75 else True
    else:
        cat, sub, conf, reason, rev, ev = "Delivery & Shipping", "Tracking & Delay", 0.88, "ML classifier match", False, "tracking order"
```

1. **The Live UI Never Loaded a Trained Model**: `cat_engine = VireoTicketCategorizer()` was instantiated in memory **without calling `.fit()` and without loading any serialized model artifact** from disk.
2. **Hardcoded Fallback in UI**: Because the battery query did not match the 6 narrow regex rules in `_extract_intent_rules()`, execution entered the `else:` block, which **literally hardcoded a fallback prediction of `"Delivery & Shipping"`, `"Tracking & Delay"`, `0.88`, and `review_required=False`**!
3. **Model Decoupling**: The evaluation code in `src/evaluation.py` trained a model in memory, evaluated it, and discarded it. It never persisted the model to disk. Consequently, the live application was completely decoupled from the ML pipeline.

---

## 2. In-Depth Audit of the 18 Implementation Dimensions

### 1. Where Training Labels Come From
- In `src/evaluation.py` and `src/analysis.py`, training labels were derived from `determine_gold_label()` in `src/benchmark_builder.py`.
- **Flaw**: `determine_gold_label()` checked `agent_notes` for keywords like `"dlvry"`, `"delivery"`, and `"courier"` *before* checking for battery, audio, or connectivity symptoms. When an agent resolved a battery issue by re-shipping a replacement via courier, the ticket was incorrectly labeled as `Delivery & Shipping`.

### 2. Treatment of Existing Tags
- The original bot tags from `Given/tickets.csv` were correctly recognized as unreliable, but the heuristic labeler used to generate ground truth suffered from regex precedence bias.

### 3. Category Normalization
- Mapped to the 11 categories in `src/taxonomy.py`.

### 4. Subcategory Assignment
- Subcategories were assigned using a crude default (`subcategories[0] if subcategories else "General"`) rather than semantic intent analysis.

### 5. Text Cleaning
- `clean_text()` in `src/preprocessing.py` removed carriage returns and excess whitespace. While it did not erase key terms, it did not extract domain entity features.

### 6. Feature Extraction
- The model used only word n-grams (1–3) with TF-IDF. It lacked **character n-grams** (crucial for typos, inflections like *"drains"*, *"draining"*, *"uncharged"*) and domain semantic keyword features.

### 7. Classifier Training
- Trained using `CalibratedClassifierCV(estimator=LogisticRegression(), cv=3)`.
- **Flaw**: Model hyperparameters were not tuned with a formal train/validation split.

### 8. Confidence Calculation
- Calculated via `np.max(probabilities)`.
- However, because the live app bypassed the ML model entirely, it reported a bogus `88%`.

### 9. Confidence Calibration
- While Platt scaling was used in `evaluation.py`, the margin between top-1 and top-2 classes was not systematically enforced, and the live app had no calibration.

### 10. Live App Model Loading
- **CRITICAL FAILURE**: `app.py` did not load any trained model file (`.joblib` or `.pkl`).

### 11. Live App vs. Evaluation Parity
- **ZERO PARITY**: The live app and the evaluation script executed two entirely different code paths.

### 12. Category Mapping Consistency
- Inconsistent due to lack of model serialization.

### 13. Stale Model Artifacts
- No model artifact was saved; code was executed on ad-hoc volatile objects.

### 14. Benchmark Label Quality
- Benchmark labels derived from `determine_gold_label()` contained false positives for `Delivery & Shipping` where replacement dispatch notes contaminated symptom labels.

### 15. Class Imbalance
- `Delivery & Shipping` (3,266) heavily dominated minority classes like `Product Enquiry` (437) and `Warranty & Repair` (409), causing the ML model to bias toward majority classes on ambiguous queries.

### 16. Heuristic Override Flaws
- Heuristics were incomplete (covered only 6 of 11 classes) and lacked semantic context for battery life, audio balance, and product comparison.

### 17. Subcategory Logic Overwrite
- Subcategory assignment was disconnected from primary category prediction.

### 18. Preprocessing Term Loss
- English stop-word filtering removed functional words like *"lasts"*, *"after"*, *"over"*, which carry critical meaning in *"lasts 20 minutes"* or *"overnight charge"*.

---

## 3. Systematic Architecture Redesign Plan

To permanently resolve these issues and satisfy all 23 acceptance criteria:

1. **Unified Inference Pipeline (`src/pipeline.py`)**:
   - Create a single, shared, serialized production pipeline (`models/vireo_classifier.joblib`).
   - `app.py`, `run_eval.py`, and `run_analysis.py` will import and call the exact same `predict_ticket(text)` function.
2. **Hybrid Classifier with Intent-Semantic Features & Word+Char N-grams**:
   - Feature Union combining:
     - Word TF-IDF n-grams (1–3) with custom domain stop words (retaining functional duration/power words).
     - Character n-grams (3–5) for morphological robustness.
     - Domain Intent Features (explicit indicator signals for Battery/Power, Bluetooth/Wireless, Acoustic/Mic, Invoicing/Tax, Delivery/AWB, Return/QC, Warranty/RMA, App/OTA, Credentials/OTP, Specs/Comparison).
   - Calibrated Linear Support Vector / Logistic Regression with `class_weight='balanced'`.
3. **Rigorous Train / Validation / Holdout Test Split**:
   - 70% Train, 15% Validation (for hyperparameter tuning), 15% Holdout Test (strictly untouched during tuning).
   - Evaluate against the baseline intake bot using the exact same split.
4. **Enhanced Top-2 Confidence & Human Review Gating**:
   - Return: `category`, `confidence`, `second_best_category`, `second_best_confidence`, `margin`, `review_required`, `evidence`, and detailed `reason`.
   - Flag for review when confidence < 0.75 OR margin < 0.15 OR conflicting domain signals exist.
5. **Automated Regression Suite (`tests/test_classifier_regression.py`)**:
   - Implement the 12 specified test cases. The test suite must pass 100%.
