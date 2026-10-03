"""
categorizer.py - Production Hybrid NLP & Calibrated Classifier for Vireo Audio.
Combines Word TF-IDF, Character N-Grams, and Domain Intent Features with
Platt-calibrated linear classification, top-2 probability margins, and human review gating.
"""
import os
import re
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from src.taxonomy import CATEGORIES, CATEGORY_TO_TEAM, SUBCATEGORIES

CONFIDENCE_THRESHOLD = 0.75
MARGIN_THRESHOLD = 0.15

class DomainIntentFeatures(BaseEstimator, TransformerMixin):
    """
    Extracts dense categorical intent signals based on domain keywords and regex patterns
    derived from Vireo Audio's Support Operating Policy v3.2.
    """
    def __init__(self):
        self.intent_patterns = {
            "Charging & Battery": [
                r"\b(battery|charge|charging|case|lasts?|drain|drains|draining|dies?|dead|overheat(ing)?|power)\b",
                r"\b(lasts?\b.*(min|minute|hour)|drain|drains|draining)\b",
                r"\b(won'?t charge|not charging|doesn'?t charge|fail(s|ed|ing)? to charge|charge overnight|full charge)\b",
                r"\b(left|right|single)\s*(ear)?bud\b.*\b(charge|battery|dies?|drain|power)\b",
                r"\b(charging\s*case|battery life)\b"
            ],
            "Connectivity": [
                r"\b(bluetooth|pair|pairing|connect|connection|disconnect|disconnecting|dropouts?|cutting out|unpair)\b",
                r"\b(unable to pair|pairing fail(s|ed|ure)?|won'?t pair|can'?t pair|won'?t connect|can'?t connect)\b",
                r"\b(forget.*device|pair.*again|re-pair|multi-?point|discoverable)\b",
                r"\b(disconnect|disconnects|disconnecting)\b.*\b(phone|laptop|minutes?)\b"
            ],
            "Audio Quality": [
                r"\b(mic|microphone|sound|audio|volume|muffled|quiet(er)?|static|crackl(e|ing)|distort(ed|ion)?|buzz(ing)?|hiss(ing)?|imbalance)\b",
                r"\b(muffled|crackling|static noise|buzzing noise|hissing|imbalance)\b",
                r"\b(right|left)\s*(ear)?bud\b.*\b(quieter|muffled|no sound|silent|low volume)\b",
                r"\b(callers? (cannot|can'?t) hear|mic(rophone)? (is )?(low|bad|muffled|broken))\b"
            ],
            "App & Firmware": [
                r"\b(firmware|ota|update)\b.*\b(stuck|fail(ed|s)?|hangs?|error|bricked?|install(ing|ation)?|\d+%)\b",
                r"\b(app|vireo app|companion app|vireo fit)\b.*\b(crash(es|ed)?|freeze|sync(ing)?|synchroniz(e|ation)?|won'?t open|not connecting)\b",
                r"\b(smartwatch|fit band|watch)\b.*\b(sensor|steps?|heart rate|sync)\b"
            ],
            "Delivery & Shipping": [
                r"\b(tracking|awb|courier|shipment|shipped|out for delivery|transit|dispatch(ed)?)\b",
                r"\b(package|order|parcel)\b.*\b(not (arrived|delivered)|supposed to arrive|delayed|late|where is)\b",
                r"\b(cancel(led|ing)? (my |this )?order|cancel order before (dispatch|shipping))\b",
                r"\b(wrong (pincode|address|flat)|typo in (the )?(address|pincode|flat number)|update address)\b",
                r"\b(paid.*not delivered|paid.*waiting.*tracking)\b"
            ],
            "Billing & Payments": [
                r"\b(charged twice|debited twice|deducted twice|double charge|charged two times|two transactions?)\b",
                r"\b(gateway error|payment fail(ed|ure)?|money (debited|deducted).*no order|amount deducted.*no confirmation)\b",
                r"\b(gst|gstin|tax invoice|invoice pdf|commercial bill|need invoice)\b",
                r"\b(coupon( code)?|discount|promo code)\b.*\b(invalid|fail(ed)?|not applied|vanished)\b"
            ],
            "Returns & Refunds": [
                r"\b(returned|sent back)\b.*\b(refund|money back)\b",
                r"\b(still haven'?t received (my |a )?refund|where is (my |the )?refund|refund pending|refund status)\b",
                r"\b(return pickup|pickup (missed|pending|scheduled|rescheduled)|courier (did not|didn'?t) show up for pickup|nobody came for (the )?pickup)\b",
                r"\b(return (this|the|my) (earbuds?|headphones?|watch|band|item|product)|want to return)\b"
            ],
            "Warranty & Repair": [
                r"\b(still under warranty|in warranty|warranty claim|claim warranty|warranty status)\b",
                r"\b(send (them|it) for repair|how (can|do) i get (it|them) repaired|service cent(er|re))\b",
                r"\b(rma|rma\s*\d+|rma number|claim number)\b",
                r"\b(stopped working after (six|6|several|three|four|five|\d+) months)\b"
            ],
            "Account & Login": [
                r"\b(otp|one time password|login code|verification code)\b.*\b(not (received|arriving|coming)|never arrives?|resend)\b",
                r"\b(locked out|cannot log ?in|can'?t log ?in|unable to log ?in|cannot log into|can'?t log into|cant log into|log into|log in to|password reset|reset email|reset link|forgot password)\b",
                r"\b(update|change)\s*(my )?(registered )?(phone|mobile|email|number)\b",
                r"\b(log ?in|account)\b.*\b(password|reset|locked|code|never arrives?)\b",
                r"\b(vireo account|user account)\b.*\b(log ?in|log into|password|access)\b"
            ],
            "Product Enquiry": [
                r"\b(difference between|compare|comparison)\b.*\b(and|vs|versus)\b",
                r"\b(is (it|this|pulse|airlite|strata|nexa)|will (it|this))\b.*\b(compatible with|work with|support)\b",
                r"\b(waterproof|water resistant|ipx|swim(ming)?|shower|specs?|specification|battery capacity|dimensions?)\b",
                r"\b(how (do|can) i (use|turn on|enable|connect|set up))\b"
            ],
            "Other": [
                r"\b(compliment|great work|kudos|feedback only|no issue)\b"
            ]
        }
        self.categories = list(self.intent_patterns.keys())

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = np.zeros((len(X), len(self.categories)), dtype=np.float32)
        for i, text in enumerate(X):
            text_lower = str(text).lower()
            for j, cat in enumerate(self.categories):
                patterns = self.intent_patterns[cat]
                score = 0.0
                for pat in patterns:
                    if re.search(pat, text_lower):
                        score += 1.0
                features[i, j] = score * 3.0
        return features

class VireoHybridClassifier:
    """
    Production Hybrid AI Classifier combining Word TF-IDF, Character N-Grams,
    Domain Intent Features, and Platt-calibrated Linear Support Vector Machine.
    """
    def __init__(self, confidence_threshold=CONFIDENCE_THRESHOLD, margin_threshold=MARGIN_THRESHOLD):
        self.confidence_threshold = confidence_threshold
        self.margin_threshold = margin_threshold
        
        # Word N-Grams (1-3)
        self.word_vec = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=12000,
            sublinear_tf=True
        )
        
        # Character N-Grams (3-5)
        self.char_vec = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(3, 5),
            max_features=12000,
            sublinear_tf=True
        )
        
        # Domain Intent Vectorizer
        self.intent_vec = DomainIntentFeatures()
        
        # Feature Union
        self.feature_union = FeatureUnion([
            ('word', self.word_vec),
            ('char', self.char_vec),
            ('intent', self.intent_vec)
        ])
        
        # Base Linear Support Vector Classifier with balanced weights
        base_svc = LinearSVC(C=0.5, class_weight='balanced', max_iter=2000, random_state=42)
        # Wrap in CalibratedClassifierCV to obtain calibrated posterior probabilities
        self.calibrated_clf = CalibratedClassifierCV(estimator=base_svc, cv=3)
        self.classes_ = None

    def fit(self, texts, labels):
        """Train feature extractors and calibrated classifier."""
        X_trans = self.feature_union.fit_transform(texts)
        self.calibrated_clf.fit(X_trans, labels)
        self.classes_ = self.calibrated_clf.classes_
        return self

    def _extract_evidence(self, text, predicted_cat):
        """Extract triggering keywords or key phrases from message for explanation."""
        text_lower = text.lower()
        patterns = self.intent_vec.intent_patterns.get(predicted_cat, [])
        matches = []
        for pat in patterns:
            m = re.search(pat, text_lower)
            if m:
                matches.append(m.group(0))
        if matches:
            return ", ".join(list(dict.fromkeys(matches))[:3])
        
        # Fallback to key words in message
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
        return " ".join(words[:4]) if words else "text feature match"

    def _determine_subcategory(self, text, category):
        """Map text to best matching subcategory using semantic rules."""
        text_lower = text.lower()
        subs = SUBCATEGORIES.get(category, ["General Inquiry"])
        
        if category == "Charging & Battery":
            if re.search(r'\b(drain|drains|draining|lasts?\b.*(min|hour))\b', text_lower):
                return "Rapid Battery Drain"
            elif re.search(r'\b(left|right|one)\s*(bud|earbud)\b', text_lower):
                return "Single Earbud Not Charging"
            elif re.search(r'\b(case|charging case)\b', text_lower):
                return "Case Fails to Charge"
            elif re.search(r'\b(heat|hot|overheat)\b', text_lower):
                return "Overheating During Charge"
            return "Battery Percentage Drop"
            
        elif category == "Connectivity":
            if re.search(r'\b(pair|pairing|unpair|re-pair)\b', text_lower):
                return "Bluetooth Pairing Failure"
            elif re.search(r'\b(disconnect|dropouts?|cutting out)\b', text_lower):
                return "Audio Dropouts & Disconnection"
            elif re.search(r'\b(discoverable|find|see)\b', text_lower):
                return "Device Not Discoverable"
            return "Multi-Point Connection Issue"
            
        elif category == "Audio Quality":
            if re.search(r'\b(mic|microphone|caller|hear me)\b', text_lower):
                return "Microphone Inaudible / Muffled"
            elif re.search(r'\b(static|crackl|buzz|hiss)\b', text_lower):
                return "Static & Crackling Noise"
            elif re.search(r'\b(quieter|low|imbalance|one side)\b', text_lower):
                return "Volume Imbalance (One Side Low)"
            return "Audio Distortion"
            
        elif category == "Delivery & Shipping":
            if re.search(r'\b(cancel(led|ing)? (my |this )?order)\b', text_lower):
                return "Pre-Dispatch Cancellation"
            elif re.search(r'\b(wrong (address|pincode)|typo in (address|pincode|flat))\b', text_lower):
                return "Address & Pincode Correction"
            elif re.search(r'\b(tracking|awb|stuck|days)\b', text_lower):
                return "Tracking & Delay"
            return "Tracking & Delay"
            
        elif category == "Billing & Payments":
            if re.search(r'\b(twice|two times|double charge)\b', text_lower):
                return "Duplicate Payment / Double Charge"
            elif re.search(r'\b(gst|gstin|invoice)\b', text_lower):
                return "GST Invoice Request"
            return "Payment Failed / Deducted"
            
        elif category == "Returns & Refunds":
            if re.search(r'\b(pickup|courier)\b', text_lower):
                return "Pickup Missed / Rescheduling"
            elif re.search(r'\b(where is (my )?refund|still haven\'?t received)\b', text_lower):
                return "Refund Status & Bank Confirmation"
            return "7-Day DOA Return"
            
        elif category == "Warranty & Repair":
            if re.search(r'\b(rma|claim number)\b', text_lower):
                return "RMA Status Follow-up"
            return "Warranty Claim Submission"
            
        elif category == "Account & Login":
            if re.search(r'\b(otp|login code|verification code)\b', text_lower):
                return "OTP Delivery Failure"
            return "Account Locked / Password Reset"
            
        elif category == "Product Enquiry":
            if re.search(r'\b(difference between|compare)\b', text_lower):
                return "Product Comparison"
            elif re.search(r'\b(compatible|work with)\b', text_lower):
                return "Compatibility Query"
            return "Specifications & Dimensions"
            
        return subs[0] if subs else "General"

    def predict_single(self, text, ticket_id="LIVE"):
        """
        Classify a single ticket inquiry, returning structured predictions with
        primary category, confidence, alternative category, margin, review flag, evidence, and reason.
        """
        text_str = str(text) if text else ""
        X_trans = self.feature_union.transform([text_str])
        probs = self.calibrated_clf.predict_proba(X_trans)[0]
        
        top_indices = np.argsort(probs)[::-1]
        top1_idx = top_indices[0]
        top2_idx = top_indices[1]
        
        primary_cat = self.classes_[top1_idx]
        primary_conf = float(probs[top1_idx])
        
        second_cat = self.classes_[top2_idx]
        second_conf = float(probs[top2_idx])
        
        margin = primary_conf - second_conf
        
        # Review Gating Policy:
        # Flag if confidence < threshold OR margin < margin_threshold OR multi-intent ambiguity detected
        multi_intent_ambiguity = False
        text_lower = text_str.lower()
        if ("cancel" in text_lower and "deducted" in text_lower) or \
           ("delivered" in text_lower and "refund" in text_lower and primary_conf < 0.85):
            multi_intent_ambiguity = True
            
        review_required = (primary_conf < self.confidence_threshold) or (margin < self.margin_threshold) or multi_intent_ambiguity
        
        # Subcategory
        subcategory = self._determine_subcategory(text_str, primary_cat)
        
        # Evidence
        evidence = self._extract_evidence(text_str, primary_cat)
        
        # Clear, informative rationale
        if review_required:
            if multi_intent_ambiguity:
                reason = f"Multi-intent customer complaint detected. Primary category '{primary_cat}' ({primary_conf:.1%}) competes with '{second_cat}' ({second_conf:.1%}). Flagged for human review."
            elif margin < self.margin_threshold:
                reason = f"Narrow margin between top predictions: '{primary_cat}' ({primary_conf:.1%}) vs '{second_cat}' ({second_conf:.1%}, margin {margin:.1%}). Flagged for supervisor review."
            else:
                reason = f"Confidence {primary_conf:.1%} below production threshold {self.confidence_threshold:.0%}. Alternative: '{second_cat}' ({second_conf:.1%}). Flagged for review."
        else:
            reason = f"High-confidence match ({primary_conf:.1%}) supported by strong domain signals for '{primary_cat}'. Alternative: '{second_cat}' ({second_conf:.1%}, margin {margin:.1%}). Straight-through routing approved."

        return {
            "ticket_id": ticket_id,
            "category": primary_cat,
            "subcategory": subcategory,
            "confidence": round(primary_conf, 4),
            "second_best_category": second_cat,
            "second_best_confidence": round(second_conf, 4),
            "margin": round(margin, 4),
            "review_required": review_required,
            "evidence": evidence,
            "reason": reason
        }

    def predict_dataset(self, df):
        """Classify an entire DataFrame of tickets."""
        results = []
        for idx, row in df.iterrows():
            t_id = row.get('ticket_id', f'TK-{idx}')
            msg = row.get('cleaned_customer_message', row.get('customer_message', ''))
            res = self.predict_single(msg, ticket_id=t_id)
            results.append(res)
        return pd.DataFrame(results)

    def save(self, filepath):
        """Serialize trained model to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        print(f"Model successfully saved to {filepath}")

    @classmethod
    def load(cls, filepath):
        """Load serialized model from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at {filepath}")
        return joblib.load(filepath)
