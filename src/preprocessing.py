"""
preprocessing.py - Data cleaning, feature enrichment, and quality auditing for Vireo Audio.
"""
import re
import pandas as pd
import numpy as np

# SLA response targets in minutes per support-policy.pdf §3
SLA_TARGETS_MIN = {
    'chat': 15,
    'voice': 120,
    'social': 240,
    'email': 480
}

# Contact costs in INR per support-policy.pdf §4
CONTACT_COSTS_INR = {
    'chat': 210,
    'email': 260,
    'voice': 520,
    'social': 240
}

def clean_text(text):
    """
    Clean and normalize ticket messages and agent notes while strictly preserving:
    - Order IDs (e.g., VR888724)
    - RMA codes (e.g., RMA82419)
    - Product references (Pulse 2, Strata, AirLite, Orbit, Nexa)
    - Tracking / AWB mentions
    - Numerical currency/warranty terms
    - Normalizes curly quotes and unicode dashes
    """
    if pd.isna(text):
        return ""
    text = str(text)
    # Normalize unicode apostrophes, quotes, and dashes
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("—", "-").replace("–", "-")
    # Normalize unicode spaces & newlines
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Strip unnecessary repeated punctuation but preserve hyphens/alphanumerics
    text = re.sub(r' +', ' ', text).strip()
    return text

def parse_and_adjust_dates(tickets_df):
    """
    Parse dates and adjust legacy UTC resolved_at timestamps to IST.
    Per support-policy §9 and README:
    'Resolution timestamps for migrated tickets were reconstructed from the legacy event log, which stores UTC.
     The helpdesk displays and exports timestamps in IST in its standard reports.'
    Adding 5 hours and 30 minutes aligns legacy UTC resolved_at to IST.
    """
    df = tickets_df.copy()
    df['created_dt'] = pd.to_datetime(df['created_at'])
    df['first_resp_dt'] = pd.to_datetime(df['first_response_at'])
    df['resolved_dt_raw'] = pd.to_datetime(df['resolved_at'])
    
    # Apply UTC -> IST (+5h 30m) offset to legacy_fd resolved timestamps
    df['resolved_dt'] = df['resolved_dt_raw']
    legacy_mask = (df['source_system'] == 'legacy_fd') & df['resolved_dt_raw'].notna()
    df.loc[legacy_mask, 'resolved_dt'] = df.loc[legacy_mask, 'resolved_dt_raw'] + pd.Timedelta(hours=5, minutes=30)
    
    # Calculate response times
    df['first_response_time_min'] = (df['first_resp_dt'] - df['created_dt']).dt.total_seconds() / 60.0
    
    # Calculate handle time (first response to resolution) in hours
    df['handle_time_hours'] = (df['resolved_dt'] - df['first_resp_dt']).dt.total_seconds() / 3600.0
    
    # Calculate total resolution time (creation to resolution) in hours
    df['total_resolution_time_hours'] = (df['resolved_dt'] - df['created_dt']).dt.total_seconds() / 3600.0
    
    # Month period for reporting
    df['year_month'] = df['created_dt'].dt.to_period('M').astype(str)
    
    return df

def calculate_slas_and_costs(df):
    """
    Calculate SLA breach metrics, breach penalty credits, contact costs, and transfer costs.
    """
    df = df.copy()
    df['sla_target_min'] = df['channel'].map(SLA_TARGETS_MIN)
    df['sla_breached'] = df['first_response_time_min'] > df['sla_target_min']
    
    # SLA breach penalty: Rs 350 store credit per breach (policy §3)
    df['sla_breach_cost_inr'] = np.where(df['sla_breached'], 350.0, 0.0)
    
    # Fully loaded contact cost (policy §4)
    df['contact_cost_inr'] = df['channel'].map(CONTACT_COSTS_INR)
    
    # Internal transfer cost: Rs 305 per transfer (policy §4)
    # Available only for helpdesk; legacy_fd transfers are blank
    df['transfers_count'] = df['transfers'].fillna(0)
    df['transfer_cost_inr'] = df['transfers_count'] * 305.0
    
    return df

def enrich_tickets(tickets_df, agents_df, products_df, customers_df, orders_df):
    """
    Merge relational context from agents, products, customers, and orders.
    """
    df = parse_and_adjust_dates(tickets_df)
    df = calculate_slas_and_costs(df)
    
    # Clean text fields
    df['cleaned_customer_message'] = df['customer_message'].apply(clean_text)
    df['cleaned_agent_notes'] = df['agent_notes'].apply(clean_text)
    
    # Join resolving agent info (Use agent_id, not name, per README and email-thread)
    agent_cols = agents_df[['agent_id', 'name', 'site', 'team', 'shift', 'tier']].rename(
        columns={
            'name': 'resolving_agent_name',
            'site': 'agent_site',
            'team': 'resolving_team',
            'shift': 'agent_shift',
            'tier': 'agent_tier'
        }
    )
    df = df.merge(agent_cols, on='agent_id', how='left')
    
    # Join product details
    prod_cols = products_df[['sku', 'product_name', 'family', 'unit_cost_inr', 'retail_price_inr', 'warranty_months']].rename(
        columns={'sku': 'product_sku'}
    )
    df = df.merge(prod_cols, on='product_sku', how='left')
    
    # Replacement cost planning: unit cost + Rs 340 logistics (policy §5)
    df['replacement_cost_inr'] = np.where(df['replacement_issued'] == 'Y', df['unit_cost_inr'] + 340.0, 0.0)
    
    # Policy violation flag: support-policy §5 forbids both refund and replacement
    df['policy_violation_flag'] = (df['refund_amount_inr'] > 0) & (df['replacement_issued'] == 'Y')
    
    # Join customer care_plus status
    cust_cols = customers_df[['customer_id', 'care_plus', 'city', 'state']]
    df = df.merge(cust_cols, on='customer_id', how='left')
    
    return df
