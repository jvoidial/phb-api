from embedding_memory import GLOBAL_EMBED_MEMORY

def infer_mood(text):
    t = text.lower()
    if "tired" in t or "overwhelmed" in t or "exhausted" in t:
        return "soft"
    if "good" in t or "great" in t:
        return "warm"
    return "neutral"

def tone(mood, memories):
    if mood == "soft":
        base = "I’m here with you… "
    elif mood == "warm":
        base = "Hey, I’m really glad you’re here. "
    else:
        base = "I’m listening. "

    if memories:
        base += "This feels familiar in a deeper way. "

    return base

def run_agent(message, state):

    mood = infer_mood(message)

    # store semantic memory
    GLOBAL_EMBED_MEMORY.add(message, tags=[mood], weight=0.7)

    # semantic recall (KEY UPGRADE)
    recalled = GLOBAL_EMBED_MEMORY.recall(message)

    state["turns"] += 1
    state["energy"] = max(1.0, min(10.0, state["energy"] - 0.03))

    return {
        "perception": message,
        "summary": tone(mood, recalled),
        "state": state,
        "memory_hits": recalled,
        "memory_mode": "embedding_semantic_v3.2",
        "memory_size": len(GLOBAL_EMBED_MEMORY.memories)
    }
