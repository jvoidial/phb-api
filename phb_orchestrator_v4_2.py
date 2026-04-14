from semantic_memory import SemanticMemory

memory = SemanticMemory()

def mood_detect(text):
    t = text.lower()
    if "tired" in t or "exhausted" in t or "overwhelmed" in t:
        return "soft"
    return "neutral"

def run_agent(message, state):

    mood = mood_detect(message)

    memory.store(message, mood)

    recalled = memory.recall(message)

    state["turns"] += 1

    response = "I’m here with you."

    if mood == "soft":
        response = "I’m here with you — take your time."

    if recalled:
        response += " This feeling has appeared before."

    return {
        "input": message,
        "mood": mood,
        "response": response,
        "memory_hits": recalled,
        "memory_size": len(memory.memories),
        "mode": "semantic_v4.2"
    }
