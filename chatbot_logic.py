# -----------------------------
# IMPORT EMOTION MODEL
# -----------------------------
from emotion_model import detect_emotion, get_emotion_prefix


# -----------------------------
# STORE CONVERSATION STATE
# -----------------------------
user_data = {
    "stage": None,
    "loan_amount": None,
    "tenure": None,
    "interest": None
}


# -----------------------------
# EMI CALCULATION FUNCTION
# -----------------------------
def calculate_emi(P, annual_rate, months):
    r = annual_rate / 12 / 100
    emi = (P * r * (1 + r)**months) / ((1 + r)**months - 1)
    return round(emi, 2)


# -----------------------------
# RESET USER STATE
# -----------------------------
def reset_user_data():
    user_data["stage"] = None
    user_data["loan_amount"] = None
    user_data["tenure"] = None
    user_data["interest"] = None


# -----------------------------
# MAIN CHATBOT RESPONSE FUNCTION
# -----------------------------
def get_bot_response(user_input):

    text = user_input.lower().strip()

    # detect emotion
    emotion = detect_emotion(text)
    prefix = get_emotion_prefix(emotion)

    # -----------------------------
    # GREETINGS
    # -----------------------------
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if text in greetings:
        reset_user_data()
        return prefix + "Hello 😊 How can I help you with your finances today?"


    # -----------------------------
    # CANCEL PROCESS
    # -----------------------------
    if text == "cancel":
        reset_user_data()
        return prefix + "Okay 👍 I've cancelled the current process."


    # -----------------------------
    # ACCOUNT TYPES
    # -----------------------------
    if "current account" in text:
        return prefix + (
            "📌 Current Account:\n"
            "Used for businesses with frequent transactions.\n"
            "• Unlimited transactions\n"
            "• Overdraft facility\n"
            "• No interest"
        )

    if "savings account" in text or "saving account" in text:
        return prefix + (
            "📌 Savings Account:\n"
            "• Earn interest\n"
            "• Safe storage\n"
            "• Limited withdrawals"
        )

    if "fixed deposit" in text:
        return prefix + (
            "📌 Fixed Deposit:\n"
            "• Lump sum deposit\n"
            "• Higher interest\n"
            "• Fixed maturity period"
        )

    if "recurring deposit" in text:
        return prefix + (
            "📌 Recurring Deposit:\n"
            "• Monthly saving plan\n"
            "• Fixed interest\n"
            "• Good for regular savings"
        )

    if "salary account" in text:
        return prefix + (
            "📌 Salary Account:\n"
            "• Zero balance account\n"
            "• Monthly salary credit\n"
            "• Special loan benefits"
        )

    if "account types" in text or "types of account" in text:
        return prefix + (
            "Banks offer:\n"
            "• Savings Account\n"
            "• Current Account\n"
            "• Salary Account\n"
            "• Fixed Deposit\n"
            "• Recurring Deposit"
        )


    # -----------------------------
    # EMOTIONAL FINANCE SUPPORT
    # -----------------------------
    if any(word in text for word in ["stress", "worried", "tension", "debt"]):
        return prefix + (
            "Financial stress is tough 💛\n"
            "Try this:\n"
            "• Track expenses\n"
            "• Reduce unnecessary spending\n"
            "• Create monthly budget\n"
            "• Build emergency fund"
        )


    # -----------------------------
    # LOAN INFORMATION
    # -----------------------------
    if "personal loan" in text:
        return prefix + "Personal loan interest starts from 10.5% per annum."

    if "home loan" in text:
        return prefix + "Home loan interest starts from 8.4% per annum."

    if "education loan" in text:
        return prefix + "Education loan interest starts from 7.5% per annum."

    if "vehicle loan" in text or "car loan" in text:
        return prefix + "Vehicle loan interest starts from 9.0% per annum."

    if "loan" and "types" in text or text == "loan":
        return prefix + (
            "Loan types available:\n"
            "• Personal Loan\n"
            "• Home Loan\n"
            "• Education Loan\n"
            "• Vehicle Loan"
        )


    # -----------------------------
    # START EMI PROCESS
    # -----------------------------
    if "emi" in text:
        reset_user_data()
        user_data["stage"] = "ask_amount"
        return prefix + "Sure 👍 Tell me the loan amount."


    # -----------------------------
    # EMI ASK AMOUNT
    # -----------------------------
    if user_data["stage"] == "ask_amount":
        try:
            user_data["loan_amount"] = float(text)
            user_data["stage"] = "ask_tenure"
            return prefix + "Enter loan tenure in months or years."
        except:
            return prefix + "Please enter valid numeric loan amount."


    # -----------------------------
    # EMI ASK TENURE
    # -----------------------------
    if user_data["stage"] == "ask_tenure":
        try:
            if "year" in text:
                years = float(text.split()[0])
                months = int(years * 12)
            elif "month" in text:
                months = int(float(text.split()[0]))
            else:
                months = int(float(text))

            user_data["tenure"] = months
            user_data["stage"] = "ask_interest"
            return prefix + "Enter annual interest rate (example 9.5)."
        except:
            return prefix + "Please enter valid tenure."


    # -----------------------------
    # EMI ASK INTEREST
    # -----------------------------
    if user_data["stage"] == "ask_interest":
        try:
            user_data["interest"] = float(text)

            emi = calculate_emi(
                user_data["loan_amount"],
                user_data["interest"],
                user_data["tenure"]
            )

            reset_user_data()
            return prefix + f"Your monthly EMI is ₹{emi}"

        except:
            return prefix + "Please enter valid interest rate."


    # -----------------------------
    # DEFAULT MESSAGE
    # -----------------------------
    return prefix + (
        "I can help with:\n"
        "• Account types\n"
        "• Loan information\n"
        "• EMI calculation\n"
        "• Financial guidance"
    )