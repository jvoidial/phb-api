from fastapi import FastAPI, Request
from phb.cognition.core import think
from phb.bridge.v3_adapter import V3ArchitectureBridge

app = FastAPI(title="PHB AI OS v7.1")

STATE = {"booted": True}
bridge = V3ArchitectureBridge()

@app.post("/message")
async def message(req: Request):
    data = await req.json()
    user_msg = data.get("message", "")
    user_id = data.get("user_id", "default")

    # STEP 1: bridge routing layer
    routed = bridge.route(user_msg)

    # STEP 2: cognition layer (single source of truth)
    result = think(user_msg, STATE, user_id)

    # STEP 3: merge outputs safely
    return {
        "input": user_msg,
        "bridge": routed,
        "cognition": result,
        "state": STATE
    }

@app.get("/")
def root():
    return {
        "status": "PHB AI OS v7.1 ONLINE",
        "mode": "cognitive-runtime"
    }
