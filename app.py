"""
SWYNEX Internship - Task 4: Final AI Application
Interactive AI Customer Support Ticket Routing System
"""

import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# 1. Dataset
training_data = [
    # Billing
    ("I was charged twice for my subscription this month.", "Billing"),
    ("Need a refund for an unauthorized charge on my credit card.", "Billing"),
    ("Where can I download my latest invoice and tax receipt?", "Billing"),
    ("My payment failed at checkout, but money was deducted.", "Billing"),
    
    # Technical Bug
    ("The mobile application crashes immediately when opening settings.", "Technical Bug"),
    ("Encountering an internal server error 500 when uploading files.", "Technical Bug"),
    ("The dashboard screen is blank and not displaying any data.", "Technical Bug"),
    ("The submit button is unresponsive and does nothing when clicked.", "Technical Bug"),
    
    # Account Access
    ("I forgot my password and the reset link email is not arriving.", "Account Access"),
    ("Unable to log in, receiving an invalid credentials error.", "Account Access"),
    ("How can I reset my two-factor authentication device on my profile?", "Account Access"),
    ("My account has been locked after several incorrect attempts.", "Account Access"),
    
    # Feature Request
    ("Could you please add dark mode support in the next desktop release?", "Feature Request"),
    ("It would be very helpful to have an option to export reports as PDF and CSV.", "Feature Request"),
    ("Please add support for multi-language localization in the app interface.", "Feature Request"),
    ("We need a bulk user import feature to upload contacts via CSV.", "Feature Request"),
]

X_train = [text for text, label in training_data]
y_train = [label for text, label in training_data]

# 2. Pipeline setup
model = Pipeline([
    ("vectorizer", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(random_state=42))
])
model.fit(X_train, y_train)

CONFIDENCE_THRESHOLD = 35.0

def process_ticket(ticket_text: str) -> dict:
    if not ticket_text or not isinstance(ticket_text, str) or not ticket_text.strip():
        return {
            "status": "ERROR",
            "category": "Invalid",
            "confidence": 0.0,
            "routing": "Rejected (Empty Input)"
        }

    cleaned = ticket_text.strip()
    if len(cleaned.split()) < 2:
        return {
            "status": "ERROR",
            "category": "Invalid",
            "confidence": 0.0,
            "routing": "Rejected (Too Vague - Minimum 2 words required)"
        }

    pred = model.predict([cleaned])[0]
    probs = model.predict_proba([cleaned])[0]
    conf = max(probs) * 100

    if conf < CONFIDENCE_THRESHOLD:
        return {
            "status": "FALLBACK",
            "category": pred,
            "confidence": round(conf, 2),
            "routing": "Human-in-the-Loop (Manual Review Queue)"
        }

    return {
        "status": "SUCCESS",
        "category": pred,
        "confidence": round(conf, 2),
        "routing": f"Automated Queue -> [{pred} Support Team]"
    }

def main():
    print("=" * 60)
    print("      SWYNEX AI APPLICATION: TICKET TRIAGE SYSTEM")
    print("=" * 60)
    print("Type your support ticket message below to see live triage.")
    print("Type 'exit' to quit the application.\n")

    sample_tests = [
        "My account is locked out and 2FA code is expired",
        "The website crashes every time I load the dashboard",
        "I was charged double on my invoice",
        "Please add a button to export data to Excel",
        "hello"
    ]

    print("--- Running Pre-configured Test Suite ---")
    for sample in sample_tests:
        res = process_ticket(sample)
        print(f"\nTicket: \"{sample}\"")
        print(f" -> Status: {res['status']} | Category: {res['category']} | Confidence: {res['confidence']}%")
        print(f" -> Routing: {res['routing']}")

    print("\n" + "=" * 60)
    print("Interactive Mode Ready:")
    while True:
        try:
            user_input = input("\nEnter a support ticket: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("Exiting application. Goodbye!")
                break
            res = process_ticket(user_input)
            print(f"Result -> Status: {res['status']} | Route: {res['routing']} (Confidence: {res['confidence']}%)")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting application.")
            break

if __name__ == "__main__":
    main()
