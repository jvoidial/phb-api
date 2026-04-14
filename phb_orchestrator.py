import json
import random
from datetime import datetime

STATE_FILE = "phb_state.json"

DEFAULT_STATE = {
    "energy": 4.5,
    "mood": "stable",
    "veil": "clear",
    "turns": 0,
    "arc": "neutral",
    "memory": []
}

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_STATE.copy()

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def update_state(state, user_message):
    state["turns"] += 1
    state["energy"] = max(1.0, min(10.0, state["energy"] + random.uniform(-0.2, 0.2)))

    if "tired" in user_message.lower():
        state["mood"] = "soft"
        state["arc"] = "stabilise"
    elif "good" in user_message.lower():
        state["mood"] = "warm"
        state["arc"] = "amplify"

    state["memory"].append({
        "t": datetime.utcnow().isoformat(),
        "msg": user_message
    })

    state["memory"] = state["memory"][-20:]

    return state

def generate_response(state, user_message):
    if state["mood"] == "soft":
        text = "I’m here with you — let’s steady things gently."
    elif state["mood"] == "warm":
        text = "I feel your energy rising — staying with you."
    else:
        text = "PHB is stable and listening."

    return {
        "perception": user_message,
        "summary": text,
        "state": state
    }

def run_orchestrator(user_message: str):
    state = load_state()
    state = update_state(state, user_message)
    save_state(state)
    return generate_response(state, user_message)
