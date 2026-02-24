import re

# -----------------------------
# LOAN INTEREST DATABASE
# -----------------------------
loan_interest = {
    "personal loan": "Personal loan interest starts from 10.5% per annum.",
    "home loan": "Home loan interest starts from 8.4% per annum.",
    "vehicle loan": "Vehicle loan interest starts from 9.0% per annum.",
    "car loan": "Car loan interest starts from 9.0% per annum.",
    "education loan": "Education loan interest starts from 7.5% per annum."
}


# -----------------------------
# EMI CALCULATION
# -----------------------------
def calculate_emi(principal, rate, months):
    rate = rate / (12 * 100)
    emi = (principal * rate * (1 + rate)**months) / ((1 + rate)**months - 1)
    return round(emi, 2)


# -----------------------------
# EXTRACT NUMBERS (optional use)
# -----------------------------
def extract_numbers(text):
    numbers = re.findall(r'\d+\.?\d*', text)
    return [float(num) for num in numbers]


# -----------------------------
# MAIN FINANCE RESPONSE
# -----------------------------
def handle_finance_query(message):

    message = message.lower()

    # ---------------- PAYMENT FAILED ----------------
    if any(word in message for word in [
        "payment failed",
        "deducted",
        "amount deducted",
        "transaction failed"
    ]):
        return (
            "If money was deducted but payment failed, don't worry. "
            "Usually the amount is automatically refunded within 3 to 5 working days. "
            "If not refunded, please contact your bank customer support."
        )

    # ---------------- FRAUD ----------------
    if any(word in message for word in ["fraud", "scam", "hacked", "stolen"]):
        return (
            "This looks like a fraud situation. Immediately block your card using "
            "mobile banking or contact your bank helpline. Also change your passwords "
            "for safety."
        )

    # ---------------- SHOW LOAN TYPES ----------------
    if "loan types" in message or message.strip() == "loan":
        return (
            "<br>We offer the following loans:</br>"
            "<br>• Personal Loan</br>"
            "<br>• Home Loan</br>"
            "<br>• Vehicle Loan</br>"
            "<br>• Education Loan</br>"
        )

    # ---------------- SINGLE LOAN INTEREST ----------------
    for loan_name, interest_text in loan_interest.items():
        if loan_name in message:
            return interest_text

    # ---------------- GENERAL INTEREST ----------------
    if "interest" in message:
        return "Interest depends on loan type. Ask like: personal loan."

    # ---------------- SAVINGS / INVESTMENT ----------------
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

    # ---------------- NO FINANCE MATCH ----------------
    return None