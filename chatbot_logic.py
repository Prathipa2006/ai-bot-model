import re
from emotion_model import detect_emotion, get_emotion_prefix


user_data = {
    "stage": None,
    "loan_amount": None,
    "tenure": None,
    "interest": None
}


def calculate_emi(P, annual_rate, months):
    r = annual_rate / 12 / 100
    emi = (P * r * (1 + r)**months) / ((1 + r)**months - 1)
    return round(emi, 2)


def reset_user_data():
    user_data["stage"] = None
    user_data["loan_amount"] = None
    user_data["tenure"] = None
    user_data["interest"] = None


def is_number(text):
    return re.match(r"^\d+(\.\d+)?$", text)


def get_bot_response(user_input):

    text = re.sub(r"[^\w\s.]", "", user_input.lower().strip())

    emotion = detect_emotion(text)
    prefix = get_emotion_prefix(emotion)

    # ---------------- GREETING ----------------
    if text in ["hi", "hello", "hey", "hii"]:
        return prefix + "Hello 😊 How can I help you with your finances today?"

    # ---------------- CANCEL EMI ----------------
    if text in ["cancel", "stop", "reset"]:
        reset_user_data()
        return prefix + "EMI calculation cancelled."

    # ---------------- START EMI ----------------
    if "emi" in text:
        reset_user_data()
        user_data["stage"] = "ask_amount"
        return prefix + "Sure 👍 Tell me the loan amount."

    # ================= EMI FLOW =================

    if user_data["stage"] == "ask_amount":

        if is_number(text):
            user_data["loan_amount"] = float(text)
            user_data["stage"] = "ask_tenure"
            return prefix + "Enter loan tenure in months."

        return prefix + (
            "I can help with:\n"
            "• Loan information\n"
            "• EMI calculation\n"
            "• Financial guidance"
        )

    if user_data["stage"] == "ask_tenure":

        if is_number(text):
            user_data["tenure"] = int(float(text))
            user_data["stage"] = "ask_interest"
            return prefix + "Enter annual interest rate (example 9.5)."

        return prefix + (
            "I can help with:\n"
            "• Loan information\n"
            "• EMI calculation\n"
            "• Financial guidance"
        )

    if user_data["stage"] == "ask_interest":

        if is_number(text):

            user_data["interest"] = float(text)

            emi = calculate_emi(
                user_data["loan_amount"],
                user_data["interest"],
                user_data["tenure"]
            )

            reset_user_data()

            return prefix + f"Your monthly EMI is ₹{emi}"

        return prefix + (
            "I can help with:\n"
            "• Loan information\n"
            "• EMI calculation\n"
            "• Financial guidance"
        )

    # ---------------- DEFAULT ----------------
    return prefix + (
        "I can help with:\n"
        "• Loan information\n"
        "• EMI calculation\n"
        "• Financial guidance"
    )
