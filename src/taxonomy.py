"""
taxonomy.py - Programmatic definitions and rules for the Vireo Audio Support Taxonomy.
"""

CATEGORIES = [
    "Delivery & Shipping",
    "Returns & Refunds",
    "Billing & Payments",
    "Warranty & Repair",
    "Charging & Battery",
    "Connectivity",
    "Audio Quality",
    "App & Firmware",
    "Account & Login",
    "Product Enquiry",
    "Other"
]

CATEGORY_TO_TEAM = {
    "Delivery & Shipping": "Logistics",
    "Returns & Refunds": "Returns Desk",
    "Billing & Payments": "Billing",
    "Warranty & Repair": "Escalations & Warranty",
    "Charging & Battery": "Chat Frontline", # Frontline Tier 1
    "Connectivity": "Chat Frontline",      # Frontline Tier 1
    "Audio Quality": "Chat Frontline",     # Frontline Tier 1
    "App & Firmware": "Chat Frontline",    # Frontline Tier 1
    "Account & Login": "Chat Frontline",   # Frontline Tier 1
    "Product Enquiry": "Chat Frontline",   # Frontline Tier 1
    "Other": "Chat Frontline"
}

SUBCATEGORIES = {
    "Delivery & Shipping": [
        "Tracking & Delay",
        "Lost in Transit",
        "Address & Pincode Correction",
        "Pre-Dispatch Cancellation",
        "Wrong Item Delivered"
    ],
    "Returns & Refunds": [
        "Reverse Pickup Scheduling",
        "Pickup Missed / Rescheduling",
        "Refund Status & Bank Confirmation",
        "7-Day DOA Return",
        "Return QC Inspection"
    ],
    "Billing & Payments": [
        "Payment Failed / Deducted",
        "Duplicate Payment / Double Charge",
        "GST Invoice Request",
        "Price Adjustment & Coupon Failure"
    ],
    "Warranty & Repair": [
        "Warranty Claim Submission",
        "RMA Status Follow-up",
        "Hardware Replacement Approval",
        "Service Center Escalation",
        "Warranty Buyback"
    ],
    "Charging & Battery": [
        "Rapid Battery Drain",
        "Single Earbud Not Charging",
        "Case Fails to Charge",
        "Overheating During Charge"
    ],
    "Connectivity": [
        "Bluetooth Pairing Failure",
        "Audio Dropouts & Stutter",
        "Device Not Discoverable",
        "Multi-Point Connection Issue"
    ],
    "Audio Quality": [
        "Microphone Inaudible / Muffled",
        "Static & Crackling Noise",
        "Volume Imbalance (One Side Low)",
        "Audio Distortion"
    ],
    "App & Firmware": [
        "Firmware Update Stuck / Failed",
        "Companion App Crash",
        "Fitness / Sensor Data Sync",
        "Setting & EQ Persistence"
    ],
    "Account & Login": [
        "OTP Delivery Failure",
        "Account Locked / Password Reset",
        "Profile & Phone Update"
    ],
    "Product Enquiry": [
        "Compatibility Query",
        "Water & Sweat Resistance",
        "Specifications & Dimensions",
        "User Manual Guidance"
    ],
    "Other": [
        "General Feedback",
        "Unclear Request",
        "Non-Standard Escalation"
    ]
}
