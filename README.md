# SWYNEX - Final AI Application (Task 4)

An intelligent, end-to-end Natural Language Processing system for automated customer support ticket triage, routing, and error recovery.

---

## 1. Problem Statement
Manual triage of inbound customer support tickets is repetitive, expensive, and introduces significant response latency. Customer inquiries often sit in generic queues for hours before reaching the appropriate technical or billing specialist. This application provides automated instant classification into four core departments: **Billing**, **Technical Bug**, **Account Access**, and **Feature Request**.

---

## 2. Technical Method
* **Feature Extraction:** Character/Word n-gram Term Frequency-Inverse Document Frequency (`TfidfVectorizer`, ngram_range=(1, 2)).
* **Classification Algorithm:** Multi-class Logistic Regression with calibrated probability outputs.
* **Intelligent Routing Logic:**
  * **Input Validation:** Catches empty strings and single-word inputs that lack actionable context.
  * **Confidence Thresholding:** Any prediction falling below a 35% probability benchmark triggers a Human-in-the-Loop fallback instead of misrouting the customer.

---

## 3. Interactive Demo & Example Cases

| Scenario | Input Ticket | Status | Action Taken |
|---|---|---|---|
| **Billing** | *"I was charged double on my invoice"* | `SUCCESS` | Automated Queue -> [Billing Support Team] |
| **Technical Bug** | *"The website crashes every time I load the dashboard"* | `SUCCESS` | Automated Queue -> [Technical Bug Support Team] |
| **Account Access** | *"My account is locked out and 2FA code is expired"* | `SUCCESS` | Automated Queue -> [Account Access Support Team] |
| **Feature Request** | *"Please add a button to export data to Excel"* | `SUCCESS` | Automated Queue -> [Feature Request Support Team] |
| **Edge Case (Vague)** | *"hello"* | `ERROR` | Rejected (Too Vague - Minimum 2 words required) |

---

## 4. Limitations
* **Language Constraint:** The current baseline model is trained exclusively on English queries and does not handle multi-lingual input.
* **Multi-Intent Tickets:** Tickets containing multiple distinct issues (e.g., both a billing complaint and a software bug) are mapped to a single primary category.
* **Lexical Coverage:** Specialized technical error codes not represented in the initial training vocabulary may require retraining or fallback routing.

---

## 5. Ethics & Responsible AI Notes
* **Privacy & Data Minimization:** The system runs locally without persistent logging of Personally Identifiable Information (PII) such as credit card numbers or credentials.
* **Fairness & Human Oversight:** Low-confidence outputs are systematically routed to human review rather than being silently misclassified, ensuring users experiencing rare issues are not ignored.
* **Transparency:** Confidence metrics and routing rationale are provided for every decision, preventing black-box failure modes.

---

## 6. How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/akshatsinghh03/SWYNEX-Final-AI-Application.git](https://github.com/akshatsinghh03/SWYNEX-Final-AI-Application.git)
   cd SWYNEX-Final-AI-Application
