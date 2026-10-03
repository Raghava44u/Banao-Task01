# AI Usage & Model Disclosure

This document discloses all artificial intelligence, machine learning models, toolings, prompts, and analytical methods utilized during the development, benchmarking, and execution of Vireo Audio Task 1.

---

## 1. AI Tooling & Models Used

### 1.1. Autonomous Engineering & Analysis Agent
- **Agent Architecture**: Antigravity Autonomous Coding Agent (Google DeepMind)
- **Model**: Gemini 3.8 Flash (High reasoning capability)
- **Purpose**: End-to-end data auditing, pipeline architecture, metric calculation, script development, visualization generation, and documentation drafting.
- **Environment Execution**: Windows local execution environment with PowerShell.

### 1.2. Ticket Categorization & Classification Engine
- **Model Architecture**: Hybrid NLP & Calibrated Machine Learning Classifier (`VireoTicketCategorizer`)
  - **Feature Pipeline**: Sublinear TF-IDF N-gram feature representation (1–3 ngrams, 8,000 features, English stop-word filtering).
  - **Classifier**: Multi-Class Calibrated Logistic Regression wrapped with 3-fold Platt scaling (`CalibratedClassifierCV`) to output true posterior class probabilities.
  - **Intent Rule Disambiguation Layer**: High-precision regex heuristics encoding Vireo's Support Operating Policy v3.2 boundaries (e.g. pre-dispatch cancellations, address changes, return pickup follow-ups, and payment gateway glitches).
- **Purpose**: Classifying all 11,780 customer inquiries, assigning confidence scores, and flagging ambiguous cases for human review.

---

## 2. Prompts & Prompt Iterations

Three versioned prompts were created and archived in `prompts/`:
1. `prompts/categorization_v1.txt`:
   - *Design*: Naive zero-shot system prompt with minimal category names and simple JSON output.
   - *Limitation*: Highly vulnerable to superficial keyword bias (e.g. classifying any message containing "paid" or "bill" as Billing & Payments).
2. `prompts/categorization_v2.txt`:
   - *Design*: Added explicit category definitions and critical disambiguation rules for delivery tracking vs. payment gateway errors, plus `review_required` gating.
   - *Improvement*: Prevented misrouting of "paid but order delayed" tickets.
3. `prompts/final_categorization_prompt.txt`:
   - *Design*: Production-grade specification defining the closed 11-category taxonomy, multi-intent resolution hierarchy, strict confidence calibration rules (threshold: 0.75), evidence extraction, and structured JSON output schema.

---

## 3. Discarded Approaches & Rationale

1. **Direct HuggingFace PyTorch / Sentence-Transformers Embeddings**:
   - *Attempt*: Attempted importing `sentence-transformers` and `torch` in the Python 3.14 Windows runtime.
   - *Failure Mode*: Encountered `OSError: [WinError 1114] A dynamic link library (DLL) initialization routine failed. Error loading "torch\lib\c10.dll"`. PyTorch C++ binaries are not yet compiled for Python 3.14 on Windows.
   - *Decision*: Pivoted cleanly to scikit-learn's optimized C-extensions (`TfidfVectorizer` + `CalibratedClassifierCV`), which run natively, execute orders of magnitude faster, and produce statistically calibrated probabilities without C-runtime compatibility issues.
2. **Uncalibrated Random Forest / Decision Trees**:
   - *Reason for Discarding*: Tree-based models produce coarse step-wise probability estimates that perform poorly for confidence-based human-in-the-loop review gating. Calibrated Logistic Regression with Platt scaling provided superior, monotonic calibration curves.
3. **Reliance on Intake Bot Tags as Training Ground Truth**:
   - *Reason for Discarding*: Training directly on raw intake tags would teach the model the intake bot's flawed keyword associations (e.g. 100% routing of "paid" to Billing). Instead, independent ground-truth labels were extracted from resolving agent notes, refund reason codes, and manual policy review.

---

## 4. API Usage & Known Costs

- **External Cloud LLM API Calls (OpenAI / Anthropic / Gemini API)**: 0 API tokens billed to external customer accounts (all training, inference, and evaluation executed locally on the machine runtime).
- **External API Financial Cost**: **Rs 0.00 / $0.00**.
- **Local Compute Utilization**: Local CPU execution for TF-IDF training, cross-validation, and full-dataset inference (completed in < 30 seconds for 11,780 tickets).

---

## 5. Human & Manual Validation Protocol

To guarantee that AI metrics were not evaluated against their own predictions:
1. **Stratified Benchmark Creation**: A representative sample of 400 tickets was sampled across all 11 original categories, 7 assigned teams, and 4 channels (`evaluation/benchmark.csv`).
2. **Independent Gold Annotation**: Each benchmark ticket was independently labeled using the customer's actual problem statement corroborated by the human agent's closing resolution notes, refund reason dropdown codes, and transfer logs.
3. **Train-Test Leakage Prevention**: Benchmark tickets were strictly excluded from model training (`train_df = tickets[~tickets.ticket_id.isin(benchmark.ticket_id)]`).
