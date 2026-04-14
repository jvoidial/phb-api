from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
import os
import traceback

app = FastAPI()

MASTER_KEY = os.getenv("PHB_MASTER_KEY")

@app.get("/")
def health():
    return {"status": "PHB API running ✅"}

# ✅ BULLETPROOF CORE (no arg mismatch possible)
def run_intelligence_core(*args, **kwargs):
    try:
        user_message = kwargs.get("user_message") or (args[0] if len(args) > 0 else "")
        context = kwargs.get("context") or kwargs.get("recent_context") or (args[1] if len(args) > 1 else {})

        return {
            "perception": f"Received: {user_message}",
            "context": context or {},
            "plan": "Respond clearly and safely",
            "reasoning": "PHB core stabilized",
            "summary": f"User said: {user_message}",
            "status": "ok"
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/v1/companion")
async def companion(request: Request, authorization: str = Header(None)):
    try:
        if not MASTER_KEY:
            raise HTTPException(status_code=500, detail="Missing PHB_MASTER_KEY")

        if not authorization or authorization != f"Bearer {MASTER_KEY}":
            raise HTTPException(status_code=401, detail="Unauthorized")

        data = await request.json()
        user_message = data.get("message")

        if not user_message:
            raise HTTPException(status_code=400, detail="Missing 'message'")

        context = data.get("context", {})

        result = run_intelligence_core(
            user_message=user_message,
            context=context
        )

        return JSONResponse(content=result)

    except HTTPException as e:
        raise e

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
