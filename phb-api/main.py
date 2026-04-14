from fastapi import FastAPI, Request
from cognition.core import think

app = FastAPI(title="PHB AI OS v7.1")

STATE = {"booted": True}

@app.post("/message")
async def message(req: Request):
    data = await req.json()

    return think(
        data.get("message",""),
        STATE,
        data.get("user_id","default")
    )

@app.get("/")
def root():
    return {
        "status": "PHB AI OS v7.1 ONLINE",
        "mode": "cognitive-runtime"
    }
