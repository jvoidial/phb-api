import time
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from phb_intelligence_core import run_v2
from phb_intelligence_core_v2_1_engine import run_v2_1


ENGINE_REGISTRY = {
    "v2": run_v2,
    "v2.1": run_v2_1,
}


def route_engine(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expected payload:
      {
        "message": "text...",
        "engine": "v2" | "v2.1"  (optional, defaults to v2)
      }
    """
    message = payload.get("message", "").strip()
    if not message:
        return {
            "error": "missing_message",
            "detail": "Payload must include a non-empty 'message' field.",
        }

    engine_key = payload.get("engine", "v2")
    engine_fn = ENGINE_REGISTRY.get(engine_key, run_v2)

    return engine_fn(message)


app = FastAPI(title="PHB Runtime", version="1.0.0")


@app.post("/v1/companion")
def companion(payload: Dict[str, Any]):
    out = route_engine(payload)
    return JSONResponse(content=out)
