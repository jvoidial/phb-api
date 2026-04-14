from event_bus import get_event
from cognition import run_cognition
import time

# -----------------------
# EVENT KERNEL WORKER
# -----------------------

def process_event(event):
    if not event:
        return None

    if event["type"] == "message":
        data = event["payload"]

        result = run_cognition(
            data["user_id"],
            data["message"]
        )

        # apply persona layer (AI woman style)
        result["response"] = apply_persona(result["response"])

        return result

    return {"status": "unknown_event"}

def apply_persona(text):
    # soft empathetic response style layer
    return f"{text} 🤍"

def kernel_loop():
    while True:
        event = get_event()

        if event:
            process_event(event)

        time.sleep(0.1)
