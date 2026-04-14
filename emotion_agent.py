class EmotionAgent:
    def detect(self, text):
        t = text.lower()

        if any(x in t for x in ["tired", "sad", "overwhelmed", "exhausted"]):
            return "soft"
        if any(x in t for x in ["happy", "good", "great"]):
            return "positive"
        return "neutral"
