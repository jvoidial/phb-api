#!/usr/bin/env python3
import json
from typing import Dict, Any

from phb_science_registry import PHBScienceRegistry

registry = PHBScienceRegistry()

def phb_api_register_science_reference(ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Called by PHB-API when a new science reference is submitted.
    """
    mapped = registry.add_reference(ref)
    return {
        "status": "ok",
        "reference_id": mapped["reference_id"],
        "symbolic_only": mapped["symbolic_only"],
        "safety_flags": mapped["safety_flags"]
    }

def phb_api_get_science_reference(ref_id: str) -> Dict[str, Any]:
    ref = registry.get_reference(ref_id)
    if not ref:
        return {"status": "not_found", "reference_id": ref_id}
    return {"status": "ok", "reference": ref}

def phb_api_list_science_references() -> Dict[str, Any]:
    return {"status": "ok", "references": registry.list_references()}

if __name__ == "__main__":
    # Simple CLI demo
    import sys
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "Provide a single reference JSON on stdin."}, indent=2))
        raise SystemExit(1)

    ref = json.loads(raw)
    result = phb_api_register_science_reference(ref)
    print(json.dumps(result, indent=2))
