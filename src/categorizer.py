"""
categorizer.py - Production AI Support Ticket Categorization Engine for Vireo Audio.
Implements a hybrid NLP + machine learning architecture with calibrated confidence scoring,
structured JSON output, intent disambiguation, and human review gating.
"""
import re
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from src.taxonomy import CATEGORIES, CATEGORY_TO_TEAM, SUBCATEGORIES

CONFIDENCE_THRESHOLD = 0.75

class VireoTicketCategorizer:
    def __init__(self, confidence_threshold=CONFIDENCE_THRESHOLD):
        self.confidence_threshold = confidence_threshold
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=8000,
            sublinear_tf=True,
            stop_words='english'
        )
        self.classifier = None
        self.classes_ = None

    def _extract_intent_rules(self, text):
        """
        High-precision domain intent rules for critical disambiguation boundaries.
        Returns (predicted_category, subcategory, reason, evidence, rule_confidence) or None.
        """
        text_lower = text.lower()
        
        # Rule 1: Pre-dispatch Cancellation or Address/Pincode Correction
        if re.search(r'\b(cancel(led|ing)? (my |this )?order|cancel order|please cancel|cancel it)\b', text_lower) and \
           not re.search(r'\b(return pickup|service centre|rma)\b', text_lower):
            return (
                "Delivery & Shipping",
                "Pre-Dispatch Cancellation",
                "Customer requested pre-dispatch order cancellation before fulfillment.",
                "cancel order",
                0.94
            )
            
        if re.search(r'\b(typo in (the )?(flat|address|pincode)|wrong (pincode|address|house number)|update (my )?address)\b', text_lower):
            return (
                "Delivery & Shipping",
                "Address & Pincode Correction",
                "Customer requested destination address or pincode modification prior to delivery.",
                "wrong address / pincode",
                0.95
            )

        # Rule 2: Post-delivery Return / Reverse Pickup / Refund Follow-up
        if re.search(r'\b(return pickup|pickup (pending|missed|scheduled|rescheduled)|nobody came for (the )?pickup|courier did not show up for pickup|where is (my |the )?refund|refund for (the )?return|money back for return)\b', text_lower):
            sub = "Pickup Missed / Rescheduling" if "pickup" in text_lower else "Refund Status & Bank Confirmation"
            return (
                "Returns & Refunds",
                sub,
                "Customer inquiring about return pickup logistics or refund status for returned merchandise.",
                "return pickup / refund follow-up",
                0.95
            )

        # Rule 3: Delivery Delays & Tracking (including "paid ... not delivered")
        if re.search(r'\b(paid.*not delivered|paid.*waiting.*tracking|out for delivery|awb|not delivered yet|shipment delayed|where is (my |the )?order|tracking not updating|dispatch date)\b', text_lower):
            return (
                "Delivery & Shipping",
                "Tracking & Delay",
                "Inquiry regarding shipment transit status, delayed carrier delivery, or dispatch tracking.",
                "delivery / tracking delay",
                0.93
            )

        # Rule 4: Payment Gateway Failures & Tax Invoices
        if re.search(r'\b(gst|gstin|invoice pdf|tax invoice|bill with|debited twice|deducted twice|gateway error|charged twice|coupon code failed)\b', text_lower):
            sub = "GST Invoice Request" if ("gst" in text_lower or "invoice" in text_lower) else "Duplicate Payment / Double Charge"
            return (
                "Billing & Payments",
                sub,
                "Payment transaction anomaly, double debit at gateway, or commercial GST invoice request.",
                "payment gateway / GST invoice",
                0.94
            )

        # Rule 5: Formal Warranty & RMA Tracking
        if re.search(r'\b(rma|rma\s*\d+|service centre|service center|warranty claim|claim number|under 1 year warranty)\b', text_lower):
            return (
                "Warranty & Repair",
                "RMA Status Follow-up" if "rma" in text_lower else "Warranty Claim Submission",
                "Formal warranty claim, authorized service center inquiry, or hardware RMA tracking.",
                "RMA / warranty claim",
                0.95
            )

        # Rule 6: Account Access & Login
        if re.search(r'\b(otp|login code|locked out of (my )?account|password reset|cannot log in|cant log in)\b', text_lower):
            return (
                "Account & Login",
                "OTP Delivery Failure" if "otp" in text_lower else "Account Locked / Password Reset",
                "User authentication difficulty, missing verification OTP, or credential lockout.",
                "login / OTP failure",
                0.95
            )

        return None

    def fit(self, texts, labels):
        """
        Train the machine learning feature extraction and calibrated classifier.
        """
        X = self.vectorizer.fit_transform(texts)
        base_lr = LogisticRegression(max_iter=1000, class_weight='balanced', C=1.5, random_state=42)
        # Wrap in CalibratedClassifierCV to ensure mathematically calibrated posterior probabilities
        self.classifier = CalibratedClassifierCV(estimator=base_lr, cv=3)
        self.classifier.fit(X, labels)
        self.classes_ = self.classifier.classes_
        return self

    def predict_ticket(self, ticket_id, text, metadata=None):
        """
        Classify a single ticket, producing structured output with confidence and review flag.
        """
        # Step 1: Check high-precision intent rule layer
        rule_result = self._extract_intent_rules(text)
        if rule_result is not None:
            cat, sub, reason, evidence, conf = rule_result
            return {
                "ticket_id": ticket_id,
                "category": cat,
                "subcategory": sub,
                "confidence": round(conf, 4),
                "reason": reason,
                "review_required": False if conf >= self.confidence_threshold else True,
                "evidence": evidence
            }

        # Step 2: Use calibrated ML classifier
        X = self.vectorizer.transform([text])
        probs = self.classifier.predict_proba(X)[0]
        max_idx = np.argmax(probs)
        predicted_cat = self.classes_[max_idx]
        confidence = float(probs[max_idx])
        
        # Check margin between top 2 classes
        sorted_probs = np.sort(probs)
        margin = float(sorted_probs[-1] - sorted_probs[-2]) if len(sorted_probs) > 1 else 1.0
        
        review_required = (confidence < self.confidence_threshold) or (margin < 0.15)
        
        # Determine likely subcategory
        subcategories = SUBCATEGORIES.get(predicted_cat, ["General"])
        subcat = subcategories[0] if subcategories else "General"
        
        # Extract evidence (top matching terms)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        evidence_words = [w for w in words if w in self.vectorizer.vocabulary_][:3]
        evidence_str = " ".join(evidence_words) if evidence_words else "text pattern match"
        
        reason = f"ML model posterior probability {confidence:.1%} for {predicted_cat} (margin: {margin:.1%})"
        if review_required:
            reason += " [Flagged for human supervisor review due to lower confidence or close competitor]"

        return {
            "ticket_id": ticket_id,
            "category": predicted_cat,
            "subcategory": subcat,
            "confidence": round(confidence, 4),
            "reason": reason,
            "review_required": review_required,
            "evidence": evidence_str
        }

    def predict_dataset(self, df):
        """
        Classify an entire dataset of tickets and return structured DataFrame.
        """
        records = []
        for idx, row in df.iterrows():
            t_id = row['ticket_id']
            msg = row['cleaned_customer_message'] if 'cleaned_customer_message' in row else row['customer_message']
            pred = self.predict_ticket(t_id, msg)
            records.append(pred)
        return pd.DataFrame(records)
