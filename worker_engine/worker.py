import time, uuid
from event_engine.engine import get_next, load, save
from result_store import write

def process(event):
    msg = event.get("message","")

    mood = "neutral"
    if any(x in msg.lower() for x in ["tired","overwhelmed","sad"]):
        mood = "soft"

    return {
        "response":"I understand you. I'm here with you.",
        "mood":mood
    }

while True:
    event = get_next()

    if event:
        try:
            result = process(event)

            event_id = str(uuid.uuid4())
            write(event_id, result)

            event["result_id"] = event_id
            event["status"] = "done"

        except Exception as e:
            event["status"] = "failed"
            event["error"] = str(e)

        save(load())

    time.sleep(1)
