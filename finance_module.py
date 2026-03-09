import re

loan_interest = {
    "personal loan": "Personal loan interest starts from 10.5% per annum.",
    "home loan": "Home loan interest starts from 8.4% per annum.",
    "vehicle loan": "Vehicle loan interest starts from 9.0% per annum.",
    "car loan": "Car loan interest starts from 9.0% per annum.",
    "education loan": "Education loan interest starts from 7.5% per annum."
}


def handle_finance_query(message):

    message = message.lower()
    # ---------------- EMOTION / POLITE RESPONSES ----------------
    if "i am very happy" in message or "i'm very happy" in message:
     return "That's wonderful to hear! I'm glad you're feeling happy."

    if "thank you" in message or "thanks" in message:
      return "You're welcome! I'm happy to help."

    if "please" in message:
      return "Sure! I'm here to help. Let me know what information you need."

    # ---------------- PAYMENT FAILED / UNEXPECTED DEDUCTION ----------------
    if any(word in message for word in [
        "payment failed",
        "deducted",
        "amount deducted",
        "transaction failed",
        "unexpectedly money deducted",
        "unexpected deduction",
        "unauthorized transaction"
    ]):
        return (
            "If money was unexpectedly deducted from your account, immediately check your "
            "transaction history for unauthorized activity or pending failed payments. "
            "Contact your bank to freeze your card, initiate a chargeback for fraudulent "
            "charges, and report it to the RBI Digital Payment Helpline (14440)."
        )

    # ---------------- FRAUD ----------------
    if any(word in message for word in ["fraud", "scam", "hacked", "stolen"]):
        return (
            "This looks like a fraud situation. Immediately block your card using "
            "mobile banking or contact your bank helpline. Also change your passwords."
        )

    # ---------------- LOAN TYPES ----------------
    if " types of loan" in message or message.strip() == "loan":
        return (
            "Loan types available:\n"
            "• Personal Loan\n"
            "• Home Loan\n"
            "• Vehicle Loan\n"
            "• Education Loan"
        )

    # ---------------- SINGLE LOAN INTEREST ----------------
    for loan_name, interest_text in loan_interest.items():
        if loan_name in message:
            return interest_text

    # ---------------- SAVINGS ----------------
    if "save" in message or "investment" in message:
        return (
            "You can grow your money through SIP, Mutual Funds, Fixed Deposits, "
            "Recurring Deposits, or PPF depending on your risk level."
        )

    # ---------------- BALANCE ----------------
    if "balance" in message:
        return (
            "You can check your account balance using mobile banking, ATM, "
            "or by contacting your bank."
        )

    return None 
