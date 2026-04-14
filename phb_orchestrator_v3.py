from memory_graph_ai import MemoryGraphAI
from tone_engine import humanize

memory = MemoryGraphAI()

def infer_mood(text):
    if "tired" in text or "overwhelmed" in text:
        return "soft"
    if "good" in text:
        return "warm"
    return "neutral"

def run_agent(user_message, state):

    mood = infer_mood(user_message)

    memory.add(user_message, tags=[mood], weight=0.7)
    hits = memory.recall("tired")

    state["turns"] += 1
    state["energy"] = max(1.0, state["energy"] - 0.05)

    response_text = humanize(mood, hits, user_message)

    return {
        "perception": user_message,
        "summary": response_text,
        "state": state,
        "memory_hits": hits
    }
