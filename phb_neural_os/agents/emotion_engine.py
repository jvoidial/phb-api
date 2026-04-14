def detect_emotion(text):
    text = text.lower()

    if "tired" in text or "exhausted" in text:
        return "soft"
    if "happy" in text:
        return "positive"
    return "neutral"
