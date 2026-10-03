# Vireo Audio Support Ticket Taxonomy & Operational Classification Guide

**Author**: Vireo Audio CX Analytics & Antigravity AI Engineering  
**Target Audience**: CX Leadership (Priya Raman), Team Leads, Support Operations (Neha Kulkarni), Engineering  
**Version**: 2.0 (Post-Audit Rationalized Taxonomy)

---

## 1. Taxonomy Design Principles

The Vireo Audio Support Taxonomy is designed to fulfill four critical operational criteria:
1. **Operational Actionability**: Every category corresponds to a specific operational team or skill set, enabling automated, accurate first-touch ticket routing.
2. **Mutual Exclusivity & Clarity**: Unambiguous decision boundaries eliminate cross-category ambiguity and reduce internal ticket hand-offs.
3. **Intent-First Priority**: Classification is driven by the customer's **primary unresolved problem** rather than passive keyword mentions (e.g. distinguishing *"I paid 5 days ago, where is my order?"* as `Delivery & Shipping` rather than `Billing & Payments`).
4. **Workforce Alignment**: Granular subcategories allow management to track root-cause volume shifts (e.g., carrier failure vs. firmware regression) to guide staffing and process engineering.

---

## 2. Core Taxonomy Overview

| Primary Category | Primary Owning Team | Target SLA | Primary Key Drivers | Example Subcategories |
| :--- | :--- | :--- | :--- | :--- |
| **Delivery & Shipping** | Logistics | Chat: 15m / Email: 8h | Courier delay, lost parcels, AWB tracking, pre-dispatch cancellation | Tracking & Delay, Lost in Transit, Address Correction, Pre-Dispatch Cancel |
| **Returns & Refunds** | Returns Desk | Chat: 15m / Email: 8h | Return pickup, reverse logistics, refund credit status, DOA returns | Pickup Rescheduling, QC Status, Refund Credit Follow-up, 7-Day DOA Return |
| **Billing & Payments** | Billing | Chat: 15m / Email: 8h | Payment gateway failures, double deductions, GST tax invoices | Failed Transaction, Duplicate Charge, GST Invoice Request, Coupon Issue |
| **Warranty & Repair** | Escalations & Warranty (Tier 2) | Measured in Days | In-warranty defect, RMA service center claims, hardware replacement | RMA Status Follow-up, Warranty Claim, Hardware Replacement Approval |
| **Charging & Battery** | Frontline (Tier 1) | Chat: 15m / Email: 8h | Battery drain, earbud charging failure, case heating/failure | Single Bud Not Charging, Case Charge Failure, Rapid Drain, Heat Issue |
| **Connectivity** | Frontline (Tier 1) | Chat: 15m / Email: 8h | Bluetooth pairing failure, audio dropouts, multi-point issues | Device Not Discoverable, Bluetooth Dropouts, Pairing Reset, Multi-point Sync |
| **Audio Quality** | Frontline (Tier 1) | Chat: 15m / Email: 8h | Microphone muffled, static/crackling, distorted sound, one-side mute | Mic Volume / Muffled Voice, Static / Hissing Noise, Imbalanced Volume, Distortion |
| **App & Firmware** | Frontline (Tier 1) | Chat: 15m / Email: 8h | Companion app crash, sync failure, firmware update brick/failure | Firmware Update Stuck, App Connection Crash, Feature Sync / Sensor Sync |
| **Account & Login** | Frontline (Tier 1) | Chat: 15m / Email: 8h | OTP not arriving, locked account, profile phone/email update | OTP Delay / Failure, Account Locked, Profile Detail Update, Password Reset |
| **Product Enquiry** | Frontline (Tier 1) | Chat: 15m / Email: 8h | Pre-sales compatibility, feature questions, water resistance | Device Compatibility, Water / Sweat Resistance, Specifications, User Manual |
| **Other / Miscellaneous**| Frontline (Tier 1) | Chat: 15m / Email: 8h | Feedback, unintelligible messages, spam, multi-issue outliers | General Feedback, Incomplete Inquiry, Policy Escalation Non-Standard |

---

## 3. Comprehensive Category Definitions

### 3.1. Delivery & Shipping
- **Definition**: Inquiries regarding the physical fulfillment, dispatch, carrier transit, and delivery of placed orders, as well as requests to intercept or cancel orders prior to warehouse dispatch.
- **Inclusion Criteria**:
  - Customer inquiring about order tracking status, shipping delays, estimated time of arrival (ETA).
  - Carrier delivered to wrong address, courier marked delivered but not received.
  - Request to correct flat/pincode/phone number before delivery.
  - Pre-dispatch order cancellation requests (where the customer wants to halt the order).
- **Exclusion Criteria**:
  - Inquiries where the customer already received the product and wants to return it for a refund -> classify as `Returns & Refunds`.
  - Payment was deducted at gateway but no order ID was generated -> classify as `Billing & Payments`.
- **Examples**:
  - *"Paid on 19 Jun, still waiting for something to show up. VR898250"*
  - *"Tracking has said out for delivery for 4 days now, courier not picking up"*
  - *"Typo in my address, courier will deliver to wrong building, please update pincode"*
- **Edge Cases**: When customer states *"paid, confirmed, then nothing, cancel my order"*, classify as `Delivery & Shipping` (Subcategory: `Pre-Dispatch Cancel`) because the primary operational action is warehouse order interception.
- **Business Relevance**: Direct operational driver for the **Logistics** team. Prevents unnecessary RTO (return-to-origin) costs and courier penalties.

---

### 3.2. Returns & Refunds
- **Definition**: Post-delivery requests to return an eligible product, schedule/reschedule reverse courier pickups, check QC status at the warehouse, or follow up on pending refund credits to original payment methods.
- **Inclusion Criteria**:
  - Dissatisfaction within return window, requesting return pickup.
  - Reverse pickup courier missed scheduled pickup window.
  - Warehouse received return, customer awaiting refund credit to bank account / UPI.
  - 7-day Dead On Arrival (DOA) return requests.
- **Exclusion Criteria**:
  - Pre-dispatch order cancellation where goods never shipped -> classify as `Delivery & Shipping`.
  - Refund requested due to duplicate payment at checkout -> classify as `Billing & Payments`.
  - Hardware defect after the return window requesting warranty repair/replacement -> classify as `Warranty & Repair`.
- **Examples**:
  - *"Return pickup was scheduled for Tuesday but nobody showed up. VR894797"*
  - *"Courier collected the return 6 days ago. Where is my refund?"*
  - *"I received the wrong color, want to return this and get my money back"*
- **Edge Cases**: If customer says *"product sound is terrible, pick it up and give me my refund"*, the intent is a return/refund. Classify as `Returns & Refunds`.
- **Business Relevance**: Governed by the **Returns Desk**. Ensures adherence to 5–7 day banking turnaround SLAs and monitors reverse courier partner reliability.

---

### 3.3. Billing & Payments
- **Definition**: Financial and transactional matters concerning payment processing, gateway errors, double billing, promotional voucher validation, and formal GST tax invoices.
- **Inclusion Criteria**:
  - Payment deducted from bank/UPI but helpdesk shows failed or pending checkout.
  - Double charge on credit card/account for a single order.
  - Requests for tax invoice with company GSTIN number.
  - Coupon code or promotional discount failed during checkout.
- **Exclusion Criteria**:
  - Customer inquiring about refund status for an already returned order -> classify as `Returns & Refunds`.
  - Customer mentioning payment date merely to identify when an undelivered parcel was ordered -> classify as `Delivery & Shipping`.
- **Examples**:
  - *"Money deducted twice from my HDFC account for order VR889123"*
  - *"Need GST invoice with company name and GSTIN for my Strata 3 purchase"*
  - *"Payment went through on UPI but page showed gateway error, no order number"*
- **Edge Cases**: *"Paid via UPI, money deducted, order confirmation email not received."* If no order was created, this is a payment gateway settlement issue (`Billing & Payments`).
- **Business Relevance**: Owned by the **Billing** team. Ensures financial reconciliation with payment aggregators (Razorpay/PayU) and commercial B2B compliance.

---

### 3.4. Warranty & Repair
- **Definition**: Claims for hardware failures, repairs, RMA tracking, and component replacement occurring outside the initial return window under Vireo's 12-month limited warranty.
- **Inclusion Criteria**:
  - Customer submitting formal warranty claim for hardware breakdown.
  - Inquiry regarding status of an active RMA at an authorized service center.
  - Out-of-the-box hardware defect beyond 7-day return window.
  - Requests for warranty buyback where replacement units are out of stock.
- **Exclusion Criteria**:
  - First-line troubleshooting for connection dropouts or app pairing -> classify as `Connectivity` or `App & Firmware`.
  - DOA failure within first 7 days of delivery requesting immediate return/refund -> classify as `Returns & Refunds`.
- **Examples**:
  - *"Service center took my Strata headphones 2 weeks ago, RMA-88192, no update"*
  - *"Headband hinge snapped after 4 months of normal use, claiming warranty"*
  - *"Right driver completely dead, need replacement under 1-year warranty"*
- **Edge Cases**: Complex, repeated hardware failures requiring certified Tier 2 evaluation.
- **Business Relevance**: Certified domain of **Escalations & Warranty (Tier 2)**. Multi-touch handling measured in days; critical for tracking manufacturing lot defects (`lot_code`).

---

### 3.5. Charging & Battery
- **Definition**: Hardware and power performance issues related to battery capacity, charging docks/cases, USB-C ports, and power endurance.
- **Inclusion Criteria**:
  - Battery draining prematurely (e.g. lasting 1–2 hours instead of rated specs).
  - Left or right earbud not making contact with charging case pins.
  - Charging case LED not turning on or case failing to accept charge.
  - Device overheating while charging.
- **Exclusion Criteria**:
  - Customer wanting to claim warranty replacement after troubleshooting has already failed -> classify as `Warranty & Repair`.
  - Third-party charger pre-purchase compatibility -> classify as `Product Enquiry`.
- **Examples**:
  - *"Left earbud never shows green charging light in the case"*
  - *"Battery goes from 100% to 10% during a 45-minute commute"*
  - *"Case becomes extremely hot when plugged into 65W GaN charger"*
- **Business Relevance**: Handled by **Frontline Teams (Tier 1)** via SOP triage steps before escalating to hardware warranty.

---

### 3.6. Connectivity
- **Definition**: Issues establishing, maintaining, or resetting wireless RF connections (Bluetooth 5.x) between Vireo devices and host endpoints (smartphones, laptops, TVs).
- **Inclusion Criteria**:
  - Earbuds or headphones not discoverable in Bluetooth scan.
  - Frequent audio dropouts, stuttering, or desynchronization between left/right buds.
  - Multi-point connection switching failure between laptop and phone.
  - High latency / audio-video sync lag during video playback or gaming.
- **Exclusion Criteria**:
  - Hardware completely unpowered / battery dead -> classify as `Charging & Battery`.
  - Companion mobile application failing to recognize device -> classify as `App & Firmware`.
- **Examples**:
  - *"Bluetooth keeps disconnecting every 3 minutes when phone is in my pocket"*
  - *"Pulse 2 earbuds not showing up in iPhone Bluetooth search list"*
  - *"Right bud connects but left bud remains unpaired"*
- **Business Relevance**: Resolvable via Tier 1 SOP reset sequences (hold button 10s, clear cache), avoiding unnecessary logistics returns.

---

### 3.7. Audio Quality
- **Definition**: Acoustic and transducer performance discrepancies, including microphone clarity, frequency response, distortion, background noise, or balance issues.
- **Inclusion Criteria**:
  - Microphone low, muffled, or inaudible during calls.
  - Audible static, hissing, buzzing, or crackling noise in audio drivers.
  - Severe channel imbalance (one side substantially quieter than the other).
  - Audio distortion at moderate listening levels.
- **Exclusion Criteria**:
  - One side silent due to dead battery / charging failure -> classify as `Charging & Battery`.
  - Audio cutting out due to Bluetooth packet drops -> classify as `Connectivity`.
- **Examples**:
  - *"Static noise when playing classical music or podcasts"*
  - *"Microphone works for Zoom on PC but callers say I sound underwater on phone"*
  - *"Right speaker driver sounds muffled compared to the left"*
- **Business Relevance**: Frontline Tier 1 triage; identifies firmware EQ settings or triggers replacement under DOA/warranty if physical driver is defective.

---

### 3.8. App & Firmware
- **Definition**: Operational issues involving the companion Vireo smartphone app (iOS/Android) or embedded firmware update processes.
- **Inclusion Criteria**:
  - Companion app crashes, freezes, or fails to launch.
  - Over-the-air (OTA) firmware update hangs at X%, fails, or bricks device.
  - Health/fitness sensor data not syncing from Nexa Smartwatch to app.
  - Equalizer / ANC settings in app not saving to hardware.
- **Exclusion Criteria**:
  - Customer unable to log into their user account due to OTP -> classify as `Account & Login`.
  - Basic Bluetooth pairing between hardware and OS -> classify as `Connectivity`.
- **Examples**:
  - *"Firmware update to v1.2.4 stuck at 68% for two hours"*
  - *"Vireo Fit app crashes immediately upon opening on Android 15"*
  - *"Step counter on Nexa Fit band not synchronizing with phone dashboard"*
- **Business Relevance**: Handled by Frontline Tier 1; vital early-warning telemetry for mobile app release regressions.

---

### 3.9. Account & Login
- **Definition**: Customer profile management, authentication, credential recovery, and digital security on Vireo's e-commerce store and app.
- **Inclusion Criteria**:
  - One-time password (OTP) not delivered to mobile number or email.
  - User locked out of account following multiple login attempts.
  - Request to update registered email address, phone number, or shipping address profile.
  - Password reset links expired or broken.
- **Exclusion Criteria**:
  - Updating shipping address for an already placed, in-transit order -> classify as `Delivery & Shipping`.
- **Examples**:
  - *"Login OTP never arrives on my Airtel number, tried 6 times"*
  - *"Locked out of my Vireo account, password reset link gives invalid token"*
  - *"Need to change registered phone number on my Vireo Care+ profile"*
- **Business Relevance**: Resolvable rapidly by Tier 1 frontline agents with account administration tools; high customer friction if unresolved.

---

### 3.10. Product Enquiry
- **Definition**: Pre-purchase or post-purchase informational inquiries regarding device specifications, compatibility, feature availability, and usage instructions.
- **Inclusion Criteria**:
  - Compatibility questions (e.g., *"Will Pulse 2 work with Samsung smart TV?"*).
  - Feature specifications (battery capacity, IPX rating, driver size, codecs).
  - User manual queries (button controls, LED light status meanings).
  - Launch dates or accessory availability questions.
- **Exclusion Criteria**:
  - Customer reporting an actual defect or failure of an owned unit -> classify under appropriate technical category.
  - B2B commercial bulk pricing -> classify under `Billing & Payments`.
- **Examples**:
  - *"Can I wear the Arc Neckband while swimming or in heavy rain?"*
  - *"Does the Nexa Smartwatch support continuous heart rate monitoring?"*
  - *"Can I connect two Pulse earbuds to a single phone simultaneously?"*
- **Business Relevance**: Handled by Tier 1 Frontline; drives sales conversion and prevents product return due to misplaced customer expectations.

---

### 3.11. Other / Miscellaneous
- **Definition**: Edge cases, unstructured customer feedback, incomprehensible transcripts, or non-support solicitations that cannot reasonably be classified into the primary 10 categories.
- **Inclusion Criteria**:
  - Brand compliments, general praise without actionable issue.
  - Incomprehensible one-word inquiries (e.g. *"test"*, *"asdf"*).
  - High-ambiguity tickets requiring manual Tier 1 supervisor assessment.
- **Exclusion Criteria**:
  - Any ticket where a core customer intent (delivery, refund, defect, billing, audio) can be established.
- **Business Rule**: Strict constraint: **Target < 3% of total ticket volume**. Any high concentration in `Other` signifies an incomplete taxonomy or uncaptured operational shift.
