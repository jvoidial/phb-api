from fastapi import FastAPI, Request, HTTPException
import traceback

from phb_orchestrator import run_orchestrator

app = FastAPI(title="PHB Unified Orchestrator")

@app.post("/v1/companion")
async def companion(request: Request):
    try:
        data = await request.json()
        msg = data.get("message", "")

        result = run_orchestrator(msg)
        return result

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "system": "PHB ORCHESTRATOR ACTIVE"}
