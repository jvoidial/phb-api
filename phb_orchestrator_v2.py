from memory_graph import MemoryGraph

graph = MemoryGraph()

def infer_mood(text, state):
    if "tired" in text or "overwhelmed" in text:
        return "soft", "stabilise"
    if "good" in text or "great" in text:
        return "warm", "amplify"
    return "neutral", "observe"

def run_agent(user_message, user_state):
    mood, arc = infer_mood(user_message, user_state)

    user_state["turns"] += 1
    user_state["energy"] = max(1.0, min(10.0, user_state["energy"] + 0.1))

    node = graph.add(
        text=user_message,
        tags=["input", mood],
        weight=0.7
    )

    response = {
        "perception": user_message,
        "summary": f"PHB v2 responding in {mood} mode.",
        "state": user_state,
        "memory_node": node,
        "arc": arc
    }

    return response
