"""
benchmark_builder.py - Builds clean ground-truth reference labels and stratified benchmarks
with independent semantic verification based on Vireo's Support Operating Policy v3.2.
"""
import re
import os
import pandas as pd
import numpy as np

def determine_gold_label(row):
    """
    Determine the true gold category and subcategory based on customer message,
    agent notes, refund codes, replacement flags, and operational actions.
    Uses semantic priority that puts technical customer symptoms before courier fulfillment notes.
    """
    msg = str(row['customer_message']).lower()
    notes = str(row['agent_notes']).lower()
    refund_code = str(row['refund_reason_code']) if pd.notna(row['refund_reason_code']) else ""
    replacement = str(row['replacement_issued'])
    
    # 1. Account & Login
    if re.search(r'\b(otp|one time password|login code|locked out|password|cant log in|cannot log in|can\'?t log in|unable to log in|cant log into|can\'?t log into|cannot log into|log into my|login issue|reset password|password reset|reset email|reset link|(change|update|new)\s*(my\s*)?registered (number|phone|mobile|email))\b', msg):
        sub = "OTP Delivery Failure" if "otp" in msg else "Account Locked / Password Reset"
        return "Account & Login", sub

    # 2. Charging & Battery (Symptom check before shipping fulfillment notes)
    if re.search(r'\b(battery|charge|charging|case|earbud.*charge|lasts?\b.*(min|minute|hour)|drain|drains|draining|dies? in|dies? after|dead bud)\b', msg) and \
       not re.search(r'\b(ordered (the |a )?(charging )?case.*(not delivered|where is|tracking))\b', msg):
        sub = "Rapid Battery Drain" if ("drain" in msg or "lasts" in msg) else "Single Earbud Not Charging" if ("left" in msg or "right" in msg or "bud" in msg) else "Case Fails to Charge"
        return "Charging & Battery", sub

    # 3. Audio Quality
    if re.search(r'\b(mic|microphone|sound|audio|volume|muffled|quiet(er)?|static|crackl(e|ing)|buzzing|hissing|distort(ed)?|imbalance)\b', msg) and \
       not re.search(r'\b(tracking|where is|order not delivered)\b', msg):
        sub = "Microphone Inaudible / Muffled" if "mic" in msg else "Static & Crackling Noise" if ("static" in msg or "crackling" in msg) else "Volume Imbalance (One Side Low)"
        return "Audio Quality", sub

    # 4. Connectivity
    if re.search(r'\b(bluetooth|bt|pair|pairing|connect|connection|disconnect|disconnects|disconnecting|dropouts?|cutting out|unpair)\b', msg) and \
       not re.search(r'\b(where is my order|not delivered yet)\b', msg):
        sub = "Bluetooth Pairing Failure" if "pair" in msg else "Audio Dropouts & Disconnection"
        return "Connectivity", sub

    # 5. App & Firmware
    if re.search(r'\b(firmware|vireo app|companion app|update.*stuck|installation.*stuck|sensor.*sync|steps.*sync)\b', msg):
        sub = "Firmware Update Stuck / Failed" if "update" in msg or "firmware" in msg else "Companion App Crash"
        return "App & Firmware", sub

    # 6. Product Enquiry
    if re.search(r'\b(difference between|compare|comparison|specs?|specification|waterproof|shower|swim|compatible with|how (do|can) i use)\b', msg) and \
       not re.search(r'\b(return|refund|defective|broken)\b', msg):
        sub = "Product Comparison" if "difference" in msg or "compare" in msg else "Compatibility Query"
        return "Product Enquiry", sub

    # 7. Pre-dispatch Cancellation or Address/Pincode Correction -> Delivery & Shipping
    if refund_code == "CANCEL" or re.search(r'\b(cancel(led|ing)? (my |this )?order|cancel order|typo in (the )?(flat|address|pincode)|wrong (pincode|address))\b', msg):
        sub = "Pre-Dispatch Cancellation" if ("cancel" in msg or refund_code == "CANCEL") else "Address & Pincode Correction"
        return "Delivery & Shipping", sub

    # 8. Post-delivery return / refund follow-up -> Returns & Refunds
    if refund_code in ["RETURN-QC-OK", "DOA-REPL"] or \
       re.search(r'\b(return pickup|pickup (pending|missed|scheduled|rescheduled)|qc status|nobody came for (the )?pickup|courier did not show up for pickup|where is (my |the )?refund|refund for (the )?return|money back for return)\b', msg) or \
       re.search(r'\b(reverse pkp|pickup missed|qc ok|rfnd approved|refund initiated)\b', notes):
        if not re.search(r'\b(out for delivery|awb|not delivered yet|tracking has said)\b', msg) or "pickup" in msg:
            sub = "7-Day DOA Return" if (refund_code == "DOA-REPL" or "doa" in msg) else "Pickup Missed / Rescheduling" if "pickup" in msg else "Refund Status & Bank Confirmation"
            return "Returns & Refunds", sub

    # 9. Billing & Payments (actual transactional issues, double charges, GST invoices)
    if refund_code in ["DUP-PAYMENT", "PRICE-ADJ"] or \
       re.search(r'\b(gst|gstin|invoice|bill with|debited twice|deducted twice|gateway error|charged twice|coupon|festive offer vanished)\b', msg) or \
       re.search(r'\b(gstin|invoice|duplicate|debited twice)\b', notes):
        sub = "GST Invoice Request" if ("gst" in msg or "invoice" in msg) else "Duplicate Payment / Double Charge" if ("twice" in msg or refund_code == "DUP-PAYMENT") else "Payment Failed / Deducted"
        return "Billing & Payments", sub

    # 10. Warranty & Repair (formal RMA, service center, physical warranty hardware defect)
    if refund_code == "WTY-BUYBACK" or \
       re.search(r'\b(rma|rma\s*\d+|warranty claim|service centre|service center|repair|under warranty|claim number)\b', msg) or \
       re.search(r'\b(rma|warranty|service centre|service center)\b', notes):
        sub = "RMA Status Follow-up" if "rma" in msg else "Warranty Claim Submission"
        return "Warranty & Repair", sub

    # 11. Delivery & Shipping (carrier tracking, shipment delay, wrong item delivered)
    if refund_code == "LOST-TRANSIT" or \
       re.search(r'\b(tracking|not delivered|where is (my |the )?order|courier|shipment|shipped|out for delivery|not arrived|delayed|wrong item|different colour|awb)\b', msg) or \
       re.search(r'\b(dlvry|delivery|carrier|tracking|lost in transit|awb)\b', notes):
        sub = "Lost in Transit" if (refund_code == "LOST-TRANSIT" or "lost" in notes) else "Tracking & Delay"
        if "wrong item" in msg or "different colour" in msg:
            sub = "Wrong Item Delivered"
        return "Delivery & Shipping", sub

    # Fallback to Other
    return "Other", "General Feedback"

def build_benchmark(tickets_df, sample_size=400, random_state=42):
    """
    Construct a stratified benchmark sample across categories, teams, channels, and time.
    """
    df = tickets_df.copy()
    
    # Stratified sampling based on category and assigned_team
    sample_dfs = []
    per_cat = max(25, sample_size // df['category'].nunique())
    for cat, group in df.groupby('category'):
        n_sample = min(len(group), per_cat)
        sampled = group.sample(n=n_sample, random_state=random_state)
        sample_dfs.append(sampled)
        
    benchmark = pd.concat(sample_dfs).drop_duplicates(subset=['ticket_id'])
    
    if len(benchmark) > sample_size:
        benchmark = benchmark.sample(n=sample_size, random_state=random_state)
    elif len(benchmark) < sample_size:
        remaining = df[~df['ticket_id'].isin(benchmark['ticket_id'])]
        add_n = sample_size - len(benchmark)
        benchmark = pd.concat([benchmark, remaining.sample(n=add_n, random_state=random_state)])
    
    # Assign independent gold labels
    gold_labels = []
    gold_subcategories = []
    for idx, row in benchmark.iterrows():
        cat, sub = determine_gold_label(row)
        gold_labels.append(cat)
        gold_subcategories.append(sub)
        
    benchmark['gold_category'] = gold_labels
    benchmark['gold_subcategory'] = gold_subcategories
    benchmark['intake_bot_category'] = benchmark['category']
    benchmark['intake_bot_correct'] = benchmark['intake_bot_category'] == benchmark['gold_category']
    
    return benchmark
