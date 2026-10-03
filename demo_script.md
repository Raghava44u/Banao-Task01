# Vireo Audio CX Analytics — 3-Minute Demonstration Script

**Target Duration**: 3 minutes (180 seconds)  
**Presenter**: Lead Analytics & AI Specialist  
**Audience**: Priya Raman (Head of CX), Arjun Mehta (Finance Controller)  
**Application**: Streamlit Dashboard (`streamlit run app.py`)

---

## Timeline & Presentation Script

### ⏱️ 0:00 – 0:20 | The Business Problem
- **Screen to Show**: Streamlit App -> **Tab 1: Executive Summary**
- **Spoken Script**:
  > *"Priya asked where to allocate the next two support hires, operating under the assumption that Billing is the largest queue at 22% of ticket volume. However, our investigation revealed that Billing's high volume was a mirage created by intake bot misclassification. Today, we demonstrate the real data findings, a high-precision AI categorization engine, and the true operational destination for the next two hires."*

### ⏱️ 0:20 – 0:40 | The Support Data & System Audit
- **Screen to Show**: Streamlit App -> **Tab 2: Data Overview**
- **Spoken Script**:
  > *"We audited all 11,780 customer tickets spanning June 2024 to June 2026 across 44 agents, 9,500 customers, and 15,000 orders. Relational integrity across all foreign keys is 100% intact. We uncovered two policy compliance violations where both refund and replacement were issued, reconciled Freshdesk legacy UTC timestamps, and identified 1,299 internal transfers costing Rs 3.96 Lakhs in re-handling waste."*

### ⏱️ 0:40 – 1:10 | AI Categorization Engine & Disambiguation
- **Screen to Show**: Streamlit App -> **Tab 3: Ticket Categorization**
- **Action**: Type into the live tester: `paid on 19 jun via upi, payment confirmed but still waiting for something to show up. order vr898250. where is my tracking` and click **Run AI Classification**.
- **Spoken Script**:
  > *"Here is why the intake bot failed: when a customer said 'paid 5 days ago, where is my order?', the bot saw the word 'paid' and routed it to Billing. Our production AI engine analyzes the true underlying intent, correctly categorizing this as Delivery & Shipping with a Tracking subcategory at 93% confidence. It features calibrated confidence scoring and a 0.75 review threshold to protect against misrouting."*

### ⏱️ 1:10 – 1:35 | Model Evaluation & Correctness Evidence
- **Screen to Show**: Streamlit App -> **Tab 7: Model Evaluation** (Scroll to Confusion Matrix)
- **Spoken Script**:
  > *"We benchmarked the model against an independent, human-reviewed gold standard of 400 stratified tickets. The AI system achieved 83.25% overall accuracy and a 0.825 Macro F1, representing a +21.5% absolute gain over the legacy bot's 61.75% accuracy—cutting errors by 56.2%. Crucially, on high-confidence straight-through tickets, the system achieves 94.54% accuracy."*

### ⏱️ 1:35 – 2:10 | Monthly Category & Team Breakdown Charts
- **Screen to Show**: Streamlit App -> **Tab 4: Category Trends** followed by **Tab 5: Team Trends**
- **Spoken Script**:
  > *"Here is the monthly category breakdown Priya requested. Under true AI classification, Delivery & Shipping is the number-one customer complaint driver at 27.7% of all volume (3,266 tickets), while true Billing issues represent only 10.8% (1,266 tickets). Looking at team trends, Logistics actually resolved 2,673 tickets—far exceeding Billing's 1,838 resolved tickets—due to receiving 795 handoffs from Billing."*

### ⏱️ 2:10 – 2:35 | Headcount Analysis: Data Finding vs. Business Rule
- **Screen to Show**: Streamlit App -> **Tab 9: Headcount Analysis**
- **Spoken Script**:
  > *"Now to the headcount decision. If Priya's two-hire rule is applied to initial assigned queue, Billing appears second. But if applied to actual resolved workload, Logistics is the number-one specialized queue. Furthermore, Logistics agents handle 534.6 tickets per agent with a median resolution backlog of 24.5 hours and a 17.1% SLA breach rate, compared to Billing's 23-minute resolution time. Logistics is the team drowning; adding hires to Billing would fund an empty queue."*

### ⏱️ 2:35 – 2:50 | Executive Memo & Business Value
- **Screen to Show**: Display `memo_to_priya.md` (or Streamlit Tab 1 / Tab 10)
- **Spoken Script**:
  > *"Our executive memo to Priya outlines a concrete numeric goal: 85% automated routing coverage with under 5% error within 90 days. For Finance Controller Arjun Mehta, implementing our AI intake router eliminates 795 unnecessary transfers, saving Rs 242,475 in annual transfer waste and preventing Rs 150,000 in SLA penalties."*

### ⏱️ 2:50 – 3:00 | AI Usage, Limitations & Conclusion
- **Screen to Show**: Streamlit App -> **Tab 10: Assumptions & Limitations**
- **Spoken Script**:
  > *"All classification executed locally with zero API cost. In conclusion: do not hire into Billing. Deploy the AI first-touch router, allocate any new headcount to Logistics, and review performance in 30 days. Thank you."*
