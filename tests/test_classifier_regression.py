"""
test_classifier_regression.py - Automated regression test suite for Vireo Audio Ticket Classifier.
Tests all 12 specified critical customer support inquiries against the production pipeline.
"""
import unittest
import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.pipeline import predict_ticket

class TestClassifierRegression(unittest.TestCase):
    
    def test_01_battery_drain_lasts_20_minutes(self):
        """TEST 1: Battery drain / earbud lasts 20 min -> Charging & Battery."""
        text = "My AirBuds were working fine yesterday, but now the left earbud only lasts about 20 minutes even after a full charge."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Charging & Battery", f"Failed: Got {res['category']} instead of Charging & Battery")
        self.assertGreaterEqual(res["confidence"], 0.70, f"Expected high confidence, got {res['confidence']}")

    def test_02_charging_case_not_charging(self):
        """TEST 2: Charging case fully charged but right earbud not charging -> Charging & Battery."""
        text = "The charging case is fully charged, but my right earbud is not charging at all. I cleaned the charging contacts and tried another cable, but nothing changed."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Charging & Battery", f"Failed: Got {res['category']}")

    def test_03_bluetooth_disconnecting(self):
        """TEST 3: AirBuds keep disconnecting from phone -> Connectivity."""
        text = "My AirBuds keep disconnecting from my phone every few minutes. I've tried forgetting the device and pairing it again."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Connectivity", f"Failed: Got {res['category']}")

    def test_04_audio_muffled_and_quieter(self):
        """TEST 4: Sound from right earbud much quieter and sounds muffled -> Audio Quality."""
        text = "The sound from my right earbud is much quieter than the left one and sounds muffled."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Audio Quality", f"Failed: Got {res['category']}")

    def test_05_charged_twice_duplicate_transaction(self):
        """TEST 5: Charged twice for same order -> Billing & Payments."""
        text = "I was charged twice for the same order. Both transactions appear on my bank statement."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Billing & Payments", f"Failed: Got {res['category']}")

    def test_06_returned_product_awaiting_refund(self):
        """TEST 6: Returned headphones ten days ago, still haven't received refund -> Returns & Refunds."""
        text = "I returned my headphones ten days ago but still haven't received my refund."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Returns & Refunds", f"Failed: Got {res['category']}")

    def test_07_tracking_not_updated_package_delayed(self):
        """TEST 7: Tracking hasn't updated for four days, package delayed -> Delivery & Shipping."""
        text = "The tracking hasn't updated for four days and my package was supposed to arrive yesterday."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Delivery & Shipping", f"Failed: Got {res['category']}")

    def test_08_login_password_reset_email(self):
        """TEST 8: Can't log into account, password reset email never arrives -> Account & Login."""
        text = "I can't log into my Vireo account and the password reset email never arrives."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Account & Login", f"Failed: Got {res['category']}")

    def test_09_firmware_update_stuck(self):
        """TEST 9: Vireo app firmware update stuck at 42% -> App & Firmware."""
        text = "The Vireo app says a firmware update is available but installation gets stuck at 42%."
        res = predict_ticket(text)
        self.assertEqual(res["category"], "App & Firmware", f"Failed: Got {res['category']}")

    def test_10_warranty_repair_request(self):
        """TEST 10: Stopped working after 6 months, still under warranty -> Warranty & Repair."""
        text = "My AirBuds stopped working after six months and they're still under warranty. How can I send them for repair?"
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Warranty & Repair", f"Failed: Got {res['category']}")

    def test_11_product_comparison_enquiry(self):
        """TEST 11: Difference between AirBuds Pro 2 and AirBuds Lite -> Product Enquiry."""
        text = "What is the difference between AirBuds Pro 2 and AirBuds Lite?"
        res = predict_ticket(text)
        self.assertEqual(res["category"], "Product Enquiry", f"Failed: Got {res['category']}")

    def test_12_order_cancelled_money_deducted_ambiguity(self):
        """TEST 12: Order cancelled but money deducted -> Ambiguity test (Review Required)."""
        text = "My order was cancelled but the money has already been deducted from my account."
        res = predict_ticket(text)
        # Should be gated for human supervisor review due to multi-intent ambiguity
        self.assertTrue(res["review_required"], "Expected review_required to be True for ambiguous multi-intent query")

if __name__ == "__main__":
    unittest.main()
