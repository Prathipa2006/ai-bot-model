from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def detect_emotion(text):
    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.5:
        return "happy"
    elif score <= -0.5:
        return "angry"
    elif score < 0:
        return "sad"
    else:
        return "neutral"


def get_emotion_prefix(emotion):
    if emotion == "angry":
        return "I'm really sorry you're facing this issue. "
    elif emotion == "sad":
        return "I understand how you feel. "
    elif emotion == "happy":
        return "That's great to hear! "
    else:
        return "" 