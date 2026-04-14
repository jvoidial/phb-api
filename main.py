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

        from phb_intelligence_core_her import run_intelligence_core
        result = run_intelligence_core(user_message=user_message, recent_context={})

        print(f"[PHB] HER‑MODE OK: {result}")
        return result

    except Exception as e:
        print("=== PHB CRASH ===")
        print("Type:", type(e).__name__)
        print("Msg:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "msg": "PHB HER‑MODE active"}
