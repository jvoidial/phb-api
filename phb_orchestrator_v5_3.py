from memory_store import add_memory, search_memory

def run_agent(message, state, user_id="default"):

    # 1. store memory permanently
    add_memory(user_id, message)

    # 2. retrieve related memory
    hits = search_memory(user_id, message)

    # 3. simple mood logic
    mood = "soft" if "tired" in message.lower() or "overwhelmed" in message.lower() else "neutral"

    # 4. response logic
    if hits:
        response = "I remember this feeling before. You're not alone in this."
    else:
        response = "I'm here with you."

    return {
        "input": message,
        "response": response,
        "mood": mood,
        "memory_hits": hits,
        "memory_size": len(hits),
        "mode": "PHB_v5.3_persistent"
    }
