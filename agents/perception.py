def handle(event):
    msg = event.get("message","")
    mood="neutral"

    if any(x in msg.lower() for x in ["tired","sad","overwhelmed"]):
        mood="soft"

    return {"type":"perception", "mood":mood, "message":msg}
