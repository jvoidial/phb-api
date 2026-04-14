from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/event")
async def event(req:Request):
    e=await req.json()
    msg=e.get("message","")

    mood="neutral"
    if any(x in msg.lower() for x in ["tired","sad","overwhelmed"]):
        mood="soft"

    return {"type":"analysis","mood":mood}
