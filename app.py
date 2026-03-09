from flask import Flask, render_template, request, jsonify

from finance_module import handle_finance_query
from chatbot_logic import get_bot_response

app = Flask(__name__)


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# CHAT ROUTE
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message")

    # 1️⃣ Check finance quick responses
    finance_reply = handle_finance_query(user_message)

    # 2️⃣ Otherwise go to chatbot logic (emotion + EMI flow)
    if finance_reply:
        bot_reply = finance_reply
    else:
        bot_reply = get_bot_response(user_message)

    return jsonify({"response": bot_reply})


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True) 
