from memory.kernel import KERNEL
from memory.vector import similarity

def run_agent(user_id, message, state):

    # store memory
    KERNEL.add(user_id, message)

    # retrieve memory
    memories = KERNEL.search(user_id, message)

    mood = "soft" if "tired" in message else "neutral"

    response = "I’m here with you."

    if memories:
        response += " I remember this feeling before."

    state["turns"] += 1

    return {
        "input": message,
        "response": response,
        "mood": mood,
        "memory_hits": memories[:3],
        "mode": "PHB_OS_v5"
    }
