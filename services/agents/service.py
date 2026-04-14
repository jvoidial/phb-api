from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/process")
async def process(req:Request):
    d=await req.json()
    msg=d["message"]

    mood="neutral"
    if any(x in msg.lower() for x in ["tired","sad","overwhelmed"]):
        mood="soft"

    return {
        "mood":mood,
        "analysis":"processed"
    }
