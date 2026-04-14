from typing import Any, Dict

from phb_intelligence_core_v2_1_engine import run_v2_1
from phb_intelligence_core import run_v2  # your existing v2 engine


ENGINE_REGISTRY = {
    "v2": run_v2,
    "v2.1": run_v2_1,
}


def route_engine(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route a companion-style payload to the correct engine.

    Expected payload shape:
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
