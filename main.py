from fastapi import FastAPI, Request, HTTPException
import traceback

from user_manager import UserManager
from phb_orchestrator_v3 import run_agent

app = FastAPI(title="PHB Neural v3 ACTIVE")

users = UserManager()

@app.post("/v2/message")
async def message(request: Request):
    try:
        data = await request.json()

        user_id = data.get("user_id", "default")
        msg = data.get("message", "")

        state = users.get(user_id)

        result = run_agent(msg, state)

        users.update(user_id, state)

        return result

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {
        "status": "ok",
        "system": "PHB NEURAL v3 ACTIVE"
    }
