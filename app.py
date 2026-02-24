from flask import Flask, render_template, request, jsonify

from emotion_model import detect_emotion, get_emotion_prefix
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

    # 1️⃣ Detect emotion
    emotion = detect_emotion(user_message)
    emotion_prefix = get_emotion_prefix(emotion)

    # 2️⃣ Check finance query
    finance_reply = handle_finance_query(user_message)

    # 3️⃣ Otherwise chatbot logic (EMI steps etc.)
    if finance_reply:
        bot_reply = finance_reply
    else:
        bot_reply = get_bot_response(user_message)

    # 4️⃣ Final response
    final_reply = emotion_prefix + bot_reply

    return jsonify({"response": final_reply})


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)