"""
app.py - Vireo Audio CX Analytics & AI Ticket Categorization Dashboard
Author: Antigravity AI Engineering
Target: Executive CX Leadership (Priya Raman) & Operations
"""
import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Vireo Audio CX & Workforce Analytics",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
    .sub-header { font-size: 15px; color: #64748B; margin-bottom: 20px; }
    .metric-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; text-align: center; }
    .metric-value { font-size: 24px; font-weight: 700; color: #0F172A; }
    .metric-label { font-size: 12px; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
    .finding-box { background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 12px 16px; border-radius: 4px; margin-bottom: 15px; }
    .warning-box { background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 12px 16px; border-radius: 4px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# Data Caching
@st.cache_data
def load_all_artifacts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    cat_tickets_path = os.path.join(base_dir, "outputs", "categorized_tickets.csv")
    monthly_cat_path = os.path.join(base_dir, "outputs", "monthly_category.csv")
    monthly_team_path = os.path.join(base_dir, "outputs", "monthly_team.csv")
    team_cat_path = os.path.join(base_dir, "outputs", "team_category_matrix.csv")
    workload_path = os.path.join(base_dir, "outputs", "team_workload_summary.csv")
    quality_path = os.path.join(base_dir, "outputs", "data_quality_report.csv")
    metrics_path = os.path.join(base_dir, "evaluation", "metrics.json")
    predictions_path = os.path.join(base_dir, "evaluation", "predictions.csv")
    
    data = {}
    if os.path.exists(cat_tickets_path):
        data['tickets'] = pd.read_csv(cat_tickets_path)
    if os.path.exists(monthly_cat_path):
        data['monthly_cat'] = pd.read_csv(monthly_cat_path)
    if os.path.exists(monthly_team_path):
        data['monthly_team'] = pd.read_csv(monthly_team_path)
    if os.path.exists(team_cat_path):
        data['team_cat'] = pd.read_csv(team_cat_path, index_col=0)
    if os.path.exists(workload_path):
        data['workload'] = pd.read_csv(workload_path, index_col=0)
    if os.path.exists(quality_path):
        data['quality'] = pd.read_csv(quality_path)
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r', encoding='utf-8') as f:
            data['metrics'] = json.load(f)
    if os.path.exists(predictions_path):
        data['predictions'] = pd.read_csv(predictions_path)
        
    return data

artifacts = load_all_artifacts()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/headphones.png", width=64)
st.sidebar.title("Vireo Audio CX")
st.sidebar.caption("Support AI & Workforce Planning System")

section = st.sidebar.radio(
    "Navigation Menu",
    [
        "1. AI Ticket Categorization Engine",
        "2. Executive Summary & CX Brief",
        "3. Data Overview & Integrity",
        "4. Category Trends",
        "5. Team Trends",
        "6. Team × Category",
        "7. Model Evaluation",
        "8. Error Analysis",
        "9. Headcount Analysis",
        "10. Assumptions & Limitations"
    ],
    index=0
)

tickets_df = artifacts.get('tickets', pd.DataFrame())

# ==========================================
# 1. TICKET CATEGORIZATION (DEFAULT FIRST VIEW)
# ==========================================
if section == "1. AI Ticket Categorization Engine":
    st.markdown('<div class="main-header">AI Ticket Categorization Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated classification, intent disambiguation, and human review gating</div>', unsafe_allow_html=True)
    
    st.subheader("Live Ticket Classifier Test")
    test_input = st.text_area(
        "Enter incoming customer support message or IVR transcript:",
        value="paid on 19 jun via upi, payment confirmed but still waiting for something to show up. order vr898250. where is my tracking"
    )
    
    if st.button("Run AI Classification", type="primary"):
        from src.pipeline import predict_ticket
        res = predict_ticket(test_input)
        cat = res['category']
        sub = res['subcategory']
        conf = res['confidence']
        second_cat = res['second_best_category']
        second_conf = res['second_best_confidence']
        margin = res['margin']
        rev = res['review_required']
        ev = res['evidence']
        reason = res['reason']
            
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        with res_col1:
            st.metric("Primary Category", str(cat))
            st.caption(f"Subcategory: **{sub}**")
        with res_col2:
            st.metric("Confidence Score", f"{conf:.1%}")
            st.caption("Calibrated posterior")
        with res_col3:
            st.metric("Runner-Up Category", str(second_cat))
            st.caption(f"Prob: **{second_conf:.1%}** | Margin: **{margin:.1%}**")
        with res_col4:
            st.metric("Review Required?", "Yes (Flagged)" if rev else "No (Straight-through)")
            st.caption("Gating: 75% conf / 15% margin")
            
        st.info(f"**Classification Rationale**: {reason}")
        if ev:
            st.markdown(f"**Triggering Feature Evidence**: `{ev}`")
        
    st.divider()
    st.subheader("Full Classified Dataset Explorer")
    if not tickets_df.empty:
        filter_cat = st.multiselect("Filter by AI Category", options=sorted(tickets_df['category'].dropna().unique()))
        filter_team = st.multiselect("Filter by Resolving Team", options=sorted(tickets_df['resolving_team'].dropna().unique()))
        
        filtered = tickets_df.copy()
        if filter_cat:
            filtered = filtered[filtered['category'].isin(filter_cat)]
        if filter_team:
            filtered = filtered[filtered['resolving_team'].isin(filter_team)]
            
        st.write(f"Displaying **{len(filtered):,}** matching tickets:")
        st.dataframe(
            filtered[['ticket_id', 'date', 'category', 'ai_subcategory', 'confidence', 'second_best_category', 'margin', 'review_required', 'resolving_team', 'classification_reason']].head(100),
            use_container_width=True
        )

# ==========================================
# 2. EXECUTIVE SUMMARY
# ==========================================
elif section == "2. Executive Summary & CX Brief":
    st.markdown('<div class="main-header">Executive Summary & CX Decision Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Strategic analysis for Priya Raman (Head of CX) & Arjun Mehta (Finance Controller)</div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Tickets Analyzed", f"{len(tickets_df):,}", "Jun 2024 – Jun 2026")
    with m2:
        st.metric("AI Categorization Accuracy", "84.49%", "+39.2% vs Intake Bot")
    with m3:
        st.metric("Highest-Volume Team (Resolved)", "Chat Frontline (3,078)", "Logistics #2 (2,673)")
    with m4:
        st.metric("Transfer Waste Recoverable", "Rs 242,475", "795 Misrouted Tickets")
        
    st.markdown("""
    <div class="finding-box">
    <b>DATA FINDING vs. BUSINESS RULE</b><br>
    <ul>
        <li><b>Priya's Initial Assumption:</b> <i>"Billing is our biggest queue by a mile, 22% of tickets... Whichever team has the most volume gets the next two hires."</i></li>
        <li><b>Data Discovery:</b> Billing's 2,564 assigned tickets were an <b>artifact of intake bot misclassification</b>. Customers writing <i>"paid, where is my tracking"</i> triggered the keyword <i>"paid"</i> and were routed to Billing. Billing transferred <b>795 tickets</b> to Logistics.</li>
        <li><b>Operational Workload Reality:</b> Logistics actually resolved <b>2,673 tickets</b> (22.7% of all work) with a median handle time of <b>24.5 hours</b> (vs Billing's 23 minutes) and the highest SLA breach rate (17.1%).</li>
        <li><b>Business Decision Rule:</b> Under Priya's rule of assigning 2 hires to the highest-volume team:
            <ul>
                <li>If measured by <b>Assigned Queue</b>: Chat Frontline (3,030) > Billing (2,564) > Logistics (1,905).</li>
                <li>If measured by <b>Actual Resolved Work</b>: Chat Frontline (3,078) > Logistics (2,673) > Billing (1,838).</li>
                <li>If measured by <b>Specialized Back-Office Work</b>: <b>Logistics is #1 by far</b> (2,673 tickets vs Billing's 1,838).</li>
            </ul>
        </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Workforce Staffing Recommendation")
        st.write("""
        1. **Do NOT allocate the 2 hires to Billing**: Billing is not drowning; its volume was artificially inflated by misrouted delivery queries.
        2. **Allocate to Logistics if hiring**: Logistics agents handle 534.6 tickets/agent with a 24.5-hour resolution backlog and 17.1% SLA breaches.
        3. **Deploy AI First-Touch Routing**: Fixes root-cause routing at intake, saving Rs 242,475 in internal transfer costs and eliminating 18.4 hours of customer lag.
        """)
    with col_b:
        st.subheader("Financial Impact Summary")
        st.write("""
        - **Total Quantified CX Spend**: Rs 11,413,088 across 11,780 customer contacts.
        - **Refunds & Replacements**: Rs 5.33M in refunds + Rs 2.00M in replacements.
        - **SLA Breach Penalty Credits**: Rs 469,000 incurred across 1,340 breached contacts (at Rs 350/breach).
        - **Two Hires Budget**: Rs 9,00,000 / year (Rs 4.5L / FTE).
        """)

# ==========================================
# 3. DATA OVERVIEW
# ==========================================
elif section == "3. Data Overview & Integrity":
    st.markdown('<div class="main-header">Support Data Audit & System Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Relational validation and data quality metrics across all tables</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Tickets", "11,780", "100% Relational Match")
    with c2:
        st.metric("Active Agents", "44", "25 Bengaluru / 19 Indore")
    with c3:
        st.metric("Customers & Orders", "9,500 / 15,000", "0 Orphan Records")
    with c4:
        st.metric("SLA Breach Rate", "11.38%", "1,340 Breaches Total")

    st.subheader("Data Quality Audit Summary")
    quality_df = artifacts.get('quality', pd.DataFrame())
    if not quality_df.empty:
        st.dataframe(quality_df, use_container_width=True)

    st.subheader("Channel SLAs and CSAT Performance")
    ch_col1, ch_col2 = st.columns(2)
    with ch_col1:
        st.write("**First-Response SLA Performance by Channel (§3)**")
        sla_table = pd.DataFrame([
            {"Channel": "Chat", "Target": "15 min", "Median Response": "5.0 min", "Breach Rate": "13.37%", "Breaches": 720},
            {"Channel": "Email", "Target": "8 hours (480m)", "Median Response": "162.0 min", "Breach Rate": "12.10%", "Breaches": 430},
            {"Channel": "Voice", "Target": "2 hours (120m)", "Median Response": "33.0 min", "Breach Rate": "5.82%", "Breaches": 99},
            {"Channel": "Social", "Target": "4 hours (240m)", "Median Response": "67.0 min", "Breach Rate": "8.01%", "Breaches": 91},
        ])
        st.dataframe(sla_table, hide_index=True, use_container_width=True)
    with ch_col2:
        st.write("**CSAT Score Distribution (§8)**")
        st.write("- Total CSAT responses: 5,345 (45.4% response rate, matching policy expectation)")
        st.write("- Average CSAT: **3.37 / 5.0**")
        st.write("- Voice Frontline achieved highest CSAT (**3.53**), Chat Frontline was lowest (**3.33**)")

# ==========================================
# 4. CATEGORY TRENDS
# ==========================================
elif section == "4. Category Trends":
    st.markdown('<div class="main-header">Monthly Category Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Volume trends across the 11-category taxonomy (Client Deliverable)</div>', unsafe_allow_html=True)
    
    chart_path = os.path.join(os.path.dirname(__file__), "outputs", "charts", "monthly_category_volume.png")
    if os.path.exists(chart_path):
        st.image(chart_path, caption="Monthly Ticket Volume by Primary Category", use_container_width=True)
        
    st.subheader("Category Distribution Summary")
    if not tickets_df.empty:
        cat_summary = tickets_df['category'].value_counts().reset_index()
        cat_summary.columns = ['Category', 'Ticket Count']
        cat_summary['Percentage'] = (cat_summary['Ticket Count'] / len(tickets_df) * 100).round(2)
        
        c_left, c_right = st.columns([1, 1])
        with c_left:
            st.dataframe(cat_summary, use_container_width=True)
        with c_right:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(cat_summary['Ticket Count'].head(6), labels=cat_summary['Category'].head(6), autopct='%1.1f%%', startangle=140)
            ax.set_title("Top 6 Category Volume Share")
            st.pyplot(fig)

# ==========================================
# 5. TEAM TRENDS
# ==========================================
elif section == "5. Team Trends":
    st.markdown('<div class="main-header">Monthly Team Breakdown</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Volume resolved by each team over time (Client Deliverable)</div>', unsafe_allow_html=True)
    
    chart_team_path = os.path.join(os.path.dirname(__file__), "outputs", "charts", "monthly_team_volume.png")
    if os.path.exists(chart_team_path):
        st.image(chart_team_path, caption="Monthly Ticket Volume Resolved by Team", use_container_width=True)
        
    monthly_team_df = artifacts.get('monthly_team', pd.DataFrame())
    if not monthly_team_df.empty:
        st.subheader("Monthly Team Volume Table")
        st.dataframe(monthly_team_df.head(50), use_container_width=True)

# ==========================================
# 6. TEAM × CATEGORY
# ==========================================
elif section == "6. Team × Category":
    st.markdown('<div class="main-header">Team × Category Workload Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Cross-tabulation showing workload composition and routing patterns</div>', unsafe_allow_html=True)
    
    heatmap_path = os.path.join(os.path.dirname(__file__), "outputs", "charts", "team_category_heatmap.png")
    if os.path.exists(heatmap_path):
        st.image(heatmap_path, caption="Team × Category Workload Heatmap", use_container_width=True)
        
    team_cat_df = artifacts.get('team_cat', pd.DataFrame())
    if not team_cat_df.empty:
        st.subheader("Team × Category Workload Table")
        st.dataframe(team_cat_df, use_container_width=True)

# ==========================================
# 7. MODEL EVALUATION
# ==========================================
elif section == "7. Model Evaluation":
    st.markdown('<div class="main-header">Independent Model Evaluation & Benchmarking</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Rigorous validation against 400 manually reviewed gold-standard tickets</div>', unsafe_allow_html=True)
    
    metrics = artifacts.get('metrics', {})
    if metrics:
        ai_m = metrics.get('ai_model', {})
        base_m = metrics.get('baseline_intake_bot', {})
        imp = metrics.get('improvement', {})
        
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("AI Accuracy", f"{ai_m.get('accuracy', 0):.1%}", f"+{imp.get('accuracy_gain_pct', 0)}% vs Bot")
        with k2:
            st.metric("Baseline Bot Accuracy", f"{base_m.get('accuracy', 0):.1%}", "Intake Bot Tags")
        with k3:
            st.metric("Macro F1 Score", f"{ai_m.get('macro_f1', 0):.3f}", f"+{imp.get('f1_macro_gain_pct', 0)}% gain")
        with k4:
            st.metric("High-Conf Accuracy", f"{ai_m.get('high_confidence_accuracy', 0):.1%}", "Straight-Through Cases")
            
    cm_path = os.path.join(os.path.dirname(__file__), "evaluation", "confusion_matrix.png")
    if os.path.exists(cm_path):
        st.subheader("Confusion Matrix")
        st.image(cm_path, caption="Confusion Matrix on 400 Gold Benchmark Samples", use_container_width=True)

# ==========================================
# 8. ERROR ANALYSIS
# ==========================================
elif section == "8. Error Analysis":
    st.markdown('<div class="main-header">Model Error Analysis & Edge Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Detailed examination of misclassifications, ambiguous tickets, and multi-intent queries</div>', unsafe_allow_html=True)
    
    preds_df = artifacts.get('predictions', pd.DataFrame())
    if not preds_df.empty:
        errors = preds_df[preds_df['ai_predicted_category'] != preds_df['gold_category']]
        st.write(f"Total misclassifications in benchmark: **{len(errors)} / {len(preds_df)}** ({len(errors)/len(preds_df):.1%})")
        
        st.dataframe(
            errors[['ticket_id', 'customer_message', 'gold_category', 'ai_predicted_category', 'confidence', 'review_required', 'reason']],
            use_container_width=True
        )
        
    st.markdown("""
    ### Key Discrepancy Drivers
    1. **Acoustic Driver Defect vs Warranty RMA**: Customer describes muffled driver; model predicts `Audio Quality`, but device age > 90 days makes it a `Warranty & Repair` RMA claim.
    2. **Multi-Intent Queries**: Customer states *"Paid 5 days ago, order not here, refund my money"*. Contains both delivery tracking and refund intent.
    3. **Human Review Guardrail**: 40.5% of cases trigger human review, ensuring straight-through automated tickets operate at **94.5% precision**.
    """)

# ==========================================
# 9. HEADCOUNT ANALYSIS
# ==========================================
elif section == "9. Headcount Analysis":
    st.markdown('<div class="main-header">Workforce & Headcount Allocation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating Priya\'s two-hire rule against actual operational data</div>', unsafe_allow_html=True)
    
    workload_df = artifacts.get('workload', pd.DataFrame())
    if not workload_df.empty:
        st.dataframe(workload_df, use_container_width=True)
        
    st.markdown("""
    ### Headcount Analysis Findings
    
    **1. Data Finding (Ticket Volumes)**
    - Highest Volume Team by **Assigned Queue**: Chat Frontline (3,030) followed by Billing (2,564).
    - Highest Volume Team by **Actual Resolved Work**: Chat Frontline (3,078) followed by Logistics (2,673).
    - Among dedicated back-office fulfillment queues: **Logistics resolved 2,673 tickets (22.7%)** vs **Billing's 1,838 tickets (15.6%)**.
    
    **2. Business Rule Application**
    - Under Priya's literal rule (*"Whichever team has the most volume gets the next two hires"*):
      - If volume means *frontline queue*, Chat Frontline qualifies.
      - If volume means *back-office resolving queues*, **Logistics qualifies**, NOT Billing.
      
    **3. Productivity & Backlog Constraints**
    - Logistics agents handle **534.6 tickets/agent**, the highest in the company.
    - Logistics resolution time is **24.5 hours median** (41.1 hours mean), compared to Billing's **23 minutes**.
    - Adding 2 hires to Billing would fund an already fast queue. Adding 2 hires to Logistics directly relieves an acute operational bottleneck.
    """)

# ==========================================
# 10. ASSUMPTIONS & LIMITATIONS
# ==========================================
elif section == "10. Assumptions & Limitations":
    st.markdown('<div class="main-header">Assumptions, Limitations & Source Traceability</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Methodological constraints, system boundaries, and data traceability</div>', unsafe_allow_html=True)
    
    st.subheader("Key Methodological Assumptions")
    st.write("""
    1. **Legacy Timestamps**: Reconstructed legacy resolution timestamps in Freshdesk were stored in UTC; applying a +5:30 offset aligns them to IST.
    2. **Headcount Costing**: Annual cost of 2 FTE hires is assumed at Rs 9,00,000 (Rs 4.5L/year/hire) as confirmed by Finance Controller Arjun Mehta.
    3. **Transfer Cost**: Re-handling cost per internal ticket transfer is fixed at Rs 305 per Support Policy §4.
    4. **CSAT Survey**: Blank CSAT scores represent non-responses (45.4% response rate) and are excluded from averages.
    """)
    
    st.subheader("System Limitations")
    st.write("""
    1. **Lack of Agent Handling Time for Legacy Period**: Pre-migration Freshdesk tickets lack step-by-step touch timestamps.
    2. **Multi-Touch Complexity**: Tier 2 Escalations & Warranty resolution is measured in days, not closed tickets per week. Raw ticket volume underrepresents Tier 2 workload.
    3. **Confidence Calibration**: While probabilities are mathematically calibrated, extreme out-of-domain vocabulary requires human supervisor gating.
    """)
