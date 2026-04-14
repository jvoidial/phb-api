from fastapi import FastAPI, Request, HTTPException
import traceback
import os

app = FastAPI(title="PHB Companion API")

@app.post("/v1/companion")
async def companion(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        print(f"[PHB] Incoming: {user_message}")
        print(f"[PHB] Env keys: {[k for k in os.environ if 'PHB' in k or 'KEY' in k.upper()]}")

        from phb_intelligence_core import run_intelligence_core
        result = run_intelligence_core(user_message=user_message, recent_context={})

        print(f"[PHB] Core OK: {result}")
        return result

    except Exception as e:
        print("=== PHB CRASH ===")
        print("Type:", type(e).__name__)
        print("Msg:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "msg": "PHB API ready - POST to /v1/companion"}
