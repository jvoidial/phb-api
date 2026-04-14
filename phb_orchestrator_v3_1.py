from memory_intelligence import GLOBAL_MEMORY

def infer_mood(text):
    if "tired" in text or "overwhelmed" in text:
        return "soft"
    if "good" in text:
        return "warm"
    return "neutral"

def human_tone(mood, memories):
    base = ""

    if mood == "soft":
        base = "I’m here with you… "
    elif mood == "warm":
        base = "Hey, I’m really glad you’re here. "
    else:
        base = "I’m listening. "

    if memories:
        base += "I remember this coming up before. "

    return base

def run_agent(user_message, state):

    mood = infer_mood(user_message)

    # 🧠 STORE MEMORY (NOW PERSISTENT)
    GLOBAL_MEMORY.add(user_message, tags=[mood], weight=0.7)

    # 🧠 RECALL MEMORY
    recalled = GLOBAL_MEMORY.recall(user_message)

    state["turns"] += 1
    state["energy"] = max(1.0, min(10.0, state["energy"] - 0.05))

    return {
        "perception": user_message,
        "summary": human_tone(mood, recalled),
        "state": state,
        "memory_hits": recalled,
        "memory_size": len(GLOBAL_MEMORY.memories)
    }
