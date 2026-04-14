from memory.store import add, get

def think(msg, state, user_id):

    state["turns"] = state.get("turns",0) + 1

    text = msg.lower()

    # emotion model
    if any(x in text for x in ["tired","overwhelmed","sad","anxious"]):
        mood = "soft"
    else:
        mood = "neutral"

    memory = get(user_id)

    # REAL MEMORY RECOGNITION LOGIC
    similar = []
    for m in memory:
        if any(word in m["text"].lower() for word in text.split()):
            similar.append(m)

    if similar:
        response = "I remember something like this before."
    elif memory:
        response = "You’ve shared this energy before — I’m here with you."
    else:
        response = "I’m here with you."

    add(user_id, msg, mood)

    return {
        "input": msg,
        "response": response,
        "mood": mood,
        "memory_hits": memory[-5:],
        "state_turns": state["turns"],
        "mode": "PHB_AI_OS_v7.1"
    }
