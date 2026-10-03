"""
taxonomy.py - Comprehensive operational taxonomy and semantic indicator definitions
for Vireo Audio Customer Support.
"""

CATEGORIES = [
    "Charging & Battery",
    "Connectivity",
    "Audio Quality",
    "App & Firmware",
    "Delivery & Shipping",
    "Billing & Payments",
    "Returns & Refunds",
    "Warranty & Repair",
    "Account & Login",
    "Product Enquiry",
    "Other"
]

CATEGORY_TO_TEAM = {
    "Charging & Battery": "Chat Frontline",   # Tier 1 Frontline
    "Connectivity": "Chat Frontline",        # Tier 1 Frontline
    "Audio Quality": "Chat Frontline",       # Tier 1 Frontline
    "App & Firmware": "Chat Frontline",      # Tier 1 Frontline
    "Delivery & Shipping": "Logistics",      # Logistics Fulfillment
    "Billing & Payments": "Billing",        # Billing & Accounting
    "Returns & Refunds": "Returns Desk",     # Returns & Reverse Logistics
    "Warranty & Repair": "Escalations & Warranty", # Tier 2 Certified
    "Account & Login": "Chat Frontline",     # Tier 1 Frontline
    "Product Enquiry": "Chat Frontline",     # Tier 1 Frontline
    "Other": "Chat Frontline"                # Tier 1 General
}

SUBCATEGORIES = {
    "Charging & Battery": [
        "Rapid Battery Drain",
        "Single Earbud Not Charging",
        "Case Fails to Charge",
        "Overheating During Charge",
        "Battery Percentage Drop"
    ],
    "Connectivity": [
        "Bluetooth Pairing Failure",
        "Audio Dropouts & Disconnection",
        "Device Not Discoverable",
        "Multi-Point Connection Issue",
        "Latency / Audio Lag"
    ],
    "Audio Quality": [
        "Microphone Inaudible / Muffled",
        "Static & Crackling Noise",
        "Volume Imbalance (One Side Low)",
        "Audio Distortion",
        "Muffled / Muddy Sound"
    ],
    "App & Firmware": [
        "Firmware Update Stuck / Failed",
        "Companion App Crash",
        "Fitness / Sensor Data Sync",
        "Setting & EQ Persistence"
    ],
    "Delivery & Shipping": [
        "Tracking & Delay",
        "Lost in Transit",
        "Address & Pincode Correction",
        "Pre-Dispatch Cancellation",
        "Wrong Item Delivered"
    ],
    "Billing & Payments": [
        "Payment Failed / Deducted",
        "Duplicate Payment / Double Charge",
        "GST Invoice Request",
        "Price Adjustment & Coupon Failure"
    ],
    "Returns & Refunds": [
        "Reverse Pickup Scheduling",
        "Pickup Missed / Rescheduling",
        "Refund Status & Bank Confirmation",
        "7-Day DOA Return",
        "Return QC Inspection"
    ],
    "Warranty & Repair": [
        "Warranty Claim Submission",
        "RMA Status Follow-up",
        "Hardware Replacement Approval",
        "Service Center Escalation",
        "Warranty Buyback"
    ],
    "Account & Login": [
        "OTP Delivery Failure",
        "Account Locked / Password Reset",
        "Profile & Phone Update"
    ],
    "Product Enquiry": [
        "Product Comparison",
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

# Detailed definitions for inclusion and exclusion
CATEGORY_DEFINITIONS = {
    "Charging & Battery": {
        "description": "Issues concerning battery endurance, charging failures of earbuds or cases, heating during charge, or rapid battery drain.",
        "keywords": ["battery", "charge", "charging", "case", "lasts", "drain", "draining", "dies", "dead", "power", "minutes", "percent", "overheat"]
    },
    "Connectivity": {
        "description": "Wireless RF connection failures, Bluetooth pairing, unexpected disconnection, audio stutter/dropouts, or multi-point issues.",
        "keywords": ["bluetooth", "pair", "pairing", "connect", "connection", "disconnect", "disconnecting", "dropouts", "cutting out", "unpair", "discoverable"]
    },
    "Audio Quality": {
        "description": "Acoustic and microphone discrepancies, static, muffled voice, low volume, driver imbalance, distortion, or background hissing.",
        "keywords": ["mic", "microphone", "sound", "audio", "volume", "muffled", "quiet", "static", "crackling", "distortion", "imbalance", "buzzing", "hissing"]
    },
    "App & Firmware": {
        "description": "Companion mobile app crashes, OTA firmware updates hanging or failing, or smartwatch sensor sync errors.",
        "keywords": ["firmware", "app", "vireo app", "vireo fit", "update", "sync", "synchronization", "sensor", "crash", "stuck", "install"]
    },
    "Delivery & Shipping": {
        "description": "Transit tracking, delayed parcels, courier non-delivery, wrong delivery address corrections, or pre-dispatch cancellations.",
        "keywords": ["tracking", "awb", "courier", "package", "parcel", "shipment", "shipped", "delivery", "delivered", "dispatch", "address", "pincode", "cancel order"]
    },
    "Billing & Payments": {
        "description": "Financial gateway debits, duplicate charges, payment deducted without order confirmation, GST invoices, or coupon errors.",
        "keywords": ["charged twice", "debited twice", "duplicate payment", "gateway error", "gst", "gstin", "invoice", "tax bill", "deducted", "payment failed", "coupon"]
    },
    "Returns & Refunds": {
        "description": "Return pickups, reverse logistics, refund credit status following product return, or 7-day DOA return requests.",
        "keywords": ["return", "returned", "refund", "pickup", "reverse pickup", "money back", "qc", "return status", "refund status"]
    },
    "Warranty & Repair": {
        "description": "Formal hardware warranty claims outside return window (7 days), service center repairs, or active RMA ticket tracking.",
        "keywords": ["warranty", "rma", "repair", "service center", "service centre", "claim", "under warranty", "defective"]
    },
    "Account & Login": {
        "description": "Customer authentication, OTP delivery failures, account lockouts, password resets, or profile mobile/email changes.",
        "keywords": ["otp", "login", "log in", "password", "locked out", "account", "verification code", "reset link", "credentials"]
    },
    "Product Enquiry": {
        "description": "Pre-purchase questions, product comparisons, technical specifications, water resistance, or usage manuals.",
        "keywords": ["difference between", "compare", "compatible", "compatibility", "waterproof", "water resistant", "ipx", "specs", "specification", "how to use"]
    },
    "Other": {
        "description": "Unintelligible requests, spam, compliments, or non-actionable miscellaneous feedback.",
        "keywords": ["feedback", "thanks", "compliment", "unclear"]
    }
}
