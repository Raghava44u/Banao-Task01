"""
cost_model.py - Financial and operational cost model calculations for Vireo Audio.
"""
import pandas as pd
import numpy as np

def calculate_financial_summary(enriched_df):
    """
    Calculate comprehensive financial metrics based on support-policy.pdf and tickets data.
    """
    df = enriched_df.copy()
    
    total_tickets = len(df)
    
    # 1. Contact Costs
    contact_cost_breakdown = df.groupby('channel')['contact_cost_inr'].agg(['count', 'sum'])
    contact_cost_breakdown.columns = ['ticket_count', 'total_cost_inr']
    total_contact_cost = df['contact_cost_inr'].sum()
    blended_contact_cost = total_contact_cost / total_tickets if total_tickets > 0 else 0.0
    
    # 2. Refund Costs
    refund_df = df[df['refund_amount_inr'] > 0]
    total_refund_tickets = len(refund_df)
    total_refund_amount = df['refund_amount_inr'].sum()
    refund_by_reason = df.groupby('refund_reason_code')['refund_amount_inr'].agg(['count', 'sum']).sort_values('sum', ascending=False)
    refund_by_reason.columns = ['ticket_count', 'total_refund_inr']
    
    # 3. Replacement Costs
    repl_df = df[df['replacement_issued'] == 'Y']
    total_replacements = len(repl_df)
    total_replacement_cost = df['replacement_cost_inr'].sum()
    repl_by_product = df[df['replacement_issued'] == 'Y'].groupby('product_name')['replacement_cost_inr'].agg(['count', 'sum']).sort_values('sum', ascending=False)
    repl_by_product.columns = ['replacement_count', 'total_cost_inr']
    
    # 4. SLA Breach Credits
    sla_breaches = df['sla_breached'].sum()
    total_sla_credit_inr = df['sla_breach_cost_inr'].sum()
    
    # 5. Internal Transfer Costs
    total_transfers = int(df['transfers_count'].sum())
    total_transfer_cost = df['transfer_cost_inr'].sum()
    
    # Misrouted transfers (Billing -> Logistics)
    billing_to_logistics = len(df[(df['assigned_team'] == 'Billing') & (df['resolving_team'] == 'Logistics')])
    billing_to_logistics_cost = billing_to_logistics * 305.0
    
    # 6. Total Operational Impact
    total_cost_impact = (
        total_contact_cost + 
        total_refund_amount + 
        total_replacement_cost + 
        total_sla_credit_inr + 
        total_transfer_cost
    )
    
    return {
        'total_tickets': total_tickets,
        'total_contact_cost': total_contact_cost,
        'blended_contact_cost': blended_contact_cost,
        'contact_cost_breakdown': contact_cost_breakdown,
        'total_refund_tickets': total_refund_tickets,
        'total_refund_amount': total_refund_amount,
        'refund_by_reason': refund_by_reason,
        'total_replacements': total_replacements,
        'total_replacement_cost': total_replacement_cost,
        'repl_by_product': repl_by_product,
        'sla_breaches': int(sla_breaches),
        'total_sla_credit_inr': total_sla_credit_inr,
        'total_transfers': total_transfers,
        'total_transfer_cost': total_transfer_cost,
        'billing_to_logistics_transfers': billing_to_logistics,
        'billing_to_logistics_cost': billing_to_logistics_cost,
        'total_cost_impact': total_cost_impact
    }
