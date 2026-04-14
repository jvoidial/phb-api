from memory.memory_core import MEMORY

def run_agent(user_id, msg, state):

    mood = "soft" if any(x in msg.lower() for x in ["tired", "sad", "overwhelmed"]) else "neutral"

    MEMORY.write(user_id, msg, mood=mood)

    hits = MEMORY.search(user_id, msg)

    context = hits[:3]

    response = "I’m here with you. I understand this pattern in your experience."

    if context:
        response += " I remember similar moments."

    state["turns"] += 1

    return {
        "input": msg,
        "response": response,
        "mood": mood,
        "memory_hits": context,
        "mode": "PHB_OS_v5.2"
    }
