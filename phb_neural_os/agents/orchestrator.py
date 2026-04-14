from agents.emotion_engine import detect_emotion

def run_orchestrator(message, memory):
    mood = detect_emotion(message)

    return {
        "input": message,
        "mood": mood,
        "response": generate(message, mood),
        "memory": memory
    }

def generate(message, mood):
    if "tired" in message:
        return "I’m here with you. Take it slowly."
    return "I understand."
