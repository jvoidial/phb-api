from fastapi import FastAPI
from fastapi.responses import JSONResponse
from phb_runtime import route_engine

app = FastAPI()

@app.post("/v1/companion")
async def companion(payload: dict):
    try:
        result = route_engine(payload)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
