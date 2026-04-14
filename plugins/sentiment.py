def run(event):
    msg = event.get("message","")
    if "tired" in msg:
        return {"sentiment":"low_energy"}
    return {"sentiment":"neutral"}
