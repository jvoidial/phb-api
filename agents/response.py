def handle(event):
    mem = event.get("memory",[])
    mood = event.get("mood","neutral")

    if mem:
        return {"type":"response","text":"I remember you. You're not alone."}
    return {"type":"response","text":"I'm here with you."}
