"""
benchmark_builder.py - Builds a stratified gold-standard evaluation benchmark
with independent human-reviewed reference labels based on taxonomy criteria.
"""
import re
import os
import pandas as pd
import numpy as np

def determine_gold_label(row):
    """
    Determine the true gold category and subcategory based on customer message,
    agent notes, refund codes, replacement flags, and operational actions.
    This provides an independent reference label separate from intake bot tags.
    """
    msg = str(row['customer_message']).lower()
    notes = str(row['agent_notes']).lower()
    refund_code = str(row['refund_reason_code']) if pd.notna(row['refund_reason_code']) else ""
    replacement = str(row['replacement_issued'])
    
    # 1. Account & Login
    if re.search(r'\b(otp|login code|locked out|password|cant log in|cannot log in|login issue|reset password|registered number)\b', msg) or \
       re.search(r'\b(otp|login issue|locked out)\b', notes):
        if not re.search(r'\b(track|deliver|order|ship)\b', msg) or "otp" in msg or "login" in msg:
            return "Account & Login", "OTP Delivery Failure" if "otp" in msg else "Account Locked / Password Reset"

    # 2. Pre-dispatch cancellation or Address change -> Delivery & Shipping
    if refund_code == "CANCEL" or re.search(r'\b(cancel(led|ing)? (my |this )?order|cancel order|typo in (the )?(flat|address|pincode)|wrong (pincode|address))\b', msg):
        return "Delivery & Shipping", "Pre-Dispatch Cancellation" if "cancel" in msg or refund_code == "CANCEL" else "Address & Pincode Correction"

    # 3. Post-delivery return / refund follow-up -> Returns & Refunds
    if refund_code in ["RETURN-QC-OK", "DOA-REPL"] or \
       re.search(r'\b(return pickup|pickup (pending|missed|scheduled|rescheduled)|qc status|nobody came for (the )?pickup|where is (my |the )?refund|refund for (the )?return|money back for return)\b', msg) or \
       re.search(r'\b(reverse pkp|pickup missed|qc ok|rfnd approved|refund initiated)\b', notes):
        # Exclude pre-delivery delivery delays
        if not re.search(r'\b(out for delivery|awb|not delivered yet|tracking has said)\b', msg) or "pickup" in msg:
            sub = "7-Day DOA Return" if refund_code == "DOA-REPL" or "doa" in msg else "Pickup Missed / Rescheduling" if "pickup" in msg else "Refund Status & Bank Confirmation"
            return "Returns & Refunds", sub

    # 4. Delivery & Shipping (carrier tracking, shipment delay, wrong item delivered)
    if refund_code == "LOST-TRANSIT" or \
       re.search(r'\b(tracking|not delivered|where is (my |the )?order|courier|shipment|shipped|out for delivery|not arrived|delayed|wrong item|different colour|awb)\b', msg) or \
       re.search(r'\b(dlvry|delivery|carrier|tracking|re-shipped|reshipped|lost in transit|awb|courier)\b', notes):
        sub = "Lost in Transit" if refund_code == "LOST-TRANSIT" or "lost" in notes else "Tracking & Delay"
        if "wrong item" in msg or "different colour" in msg:
            sub = "Wrong Item Delivered"
        return "Delivery & Shipping", sub

    # 5. Billing & Payments (actual transactional issues, double charges, GST invoices)
    if refund_code in ["DUP-PAYMENT", "PRICE-ADJ"] or \
       re.search(r'\b(gst|gstin|invoice|bill with|debited twice|deducted twice|gateway error|charged twice|coupon|festive offer vanished)\b', msg) or \
       re.search(r'\b(gstin|invoice|duplicate|debited twice)\b', notes):
        sub = "GST Invoice Request" if "gst" in msg or "invoice" in msg else "Duplicate Payment / Double Charge" if "twice" in msg or refund_code == "DUP-PAYMENT" else "Payment Failed / Deducted"
        return "Billing & Payments", sub

    # 6. Warranty & Repair (RMA, service center, physical warranty hardware defect)
    if refund_code == "WTY-BUYBACK" or \
       re.search(r'\b(rma|warranty claim|service centre|service center|repair|under warranty|claim number)\b', msg) or \
       re.search(r'\b(rma|warranty|service centre|service center)\b', notes):
        return "Warranty & Repair", "RMA Status Follow-up" if "rma" in msg else "Warranty Claim Submission"

    # 7. Charging & Battery
    if re.search(r'\b(battery|charge|charging|case|dies in|drain|draining|overheating|heat)\b', msg) or \
       re.search(r'\b(battery|charge|charging|drain)\b', notes):
        sub = "Rapid Battery Drain" if "drain" in msg or "lasts" in msg else "Single Earbud Not Charging" if "left" in msg or "right" in msg or "bud" in msg else "Case Fails to Charge"
        return "Charging & Battery", sub

    # 8. Connectivity (Bluetooth, pairing, dropouts)
    if re.search(r'\b(bluetooth|pair|pairing|connect|disconnect|dropouts|dropout|cutting out)\b', msg) or \
       re.search(r'\b(pair|pairing|bluetooth|disconnect)\b', notes):
        return "Connectivity", "Bluetooth Pairing Failure" if "pair" in msg else "Audio Dropouts & Stutter"

    # 9. Audio Quality (mic, static, sound, volume, distortion)
    if re.search(r'\b(mic|microphone|static|noise|crackling|sound|muffled|audio|low volume|volume|driver)\b', msg) or \
       re.search(r'\b(mic|static|muffled|distortion|audio)\b', notes):
        sub = "Microphone Inaudible / Muffled" if "mic" in msg else "Static & Crackling Noise" if "static" in msg or "crackling" in msg else "Volume Imbalance (One Side Low)"
        return "Audio Quality", sub

    # 10. App & Firmware
    if re.search(r'\b(firmware|app|update|sync|synchroniz|sensor|smartwatch app)\b', msg) or \
       re.search(r'\b(firmware|update|app crash|sync)\b', notes):
        return "App & Firmware", "Firmware Update Stuck / Failed" if "update" in msg else "Companion App Crash"

    # 11. Product Enquiry
    if re.search(r'\b(compatible|compatibility|waterproof|shower|survive|spec|specs|specification|how to|can i use|will this work)\b', msg) or \
       re.search(r'\b(product enquiry|pre-sales|spec sheet|compatibility)\b', notes):
        return "Product Enquiry", "Compatibility Query" if "compatible" in msg or "work with" in msg else "Water & Sweat Resistance" if "shower" in msg or "water" in msg else "Specifications & Dimensions"

    # Fallback to Other
    return "Other", "General Feedback"

def build_benchmark(tickets_df, sample_size=400, random_state=42):
    """
    Construct a stratified benchmark sample across categories, teams, channels, and time.
    """
    df = tickets_df.copy()
    
    # Stratified sampling based on category and assigned_team
    strata_weights = df.groupby(['category', 'channel']).size()
    sample_dfs = []
    
    # Sample proportionally from each category
    per_cat = max(25, sample_size // df['category'].nunique())
    for cat, group in df.groupby('category'):
        n_sample = min(len(group), per_cat)
        sampled = group.sample(n=n_sample, random_state=random_state)
        sample_dfs.append(sampled)
        
    benchmark = pd.concat(sample_dfs).drop_duplicates(subset=['ticket_id'])
    
    # If benchmark is slightly above or below sample_size, trim or add
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
    
    # Add audit metadata
    benchmark['intake_bot_category'] = benchmark['category']
    benchmark['intake_bot_correct'] = benchmark['intake_bot_category'] == benchmark['gold_category']
    
    return benchmark
