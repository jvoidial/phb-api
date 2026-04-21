#!/usr/bin/env python3
import json
from typing import Dict, Any

from phb_science_registry import PHBScienceRegistry

registry = PHBScienceRegistry()

def load_science_into_vortex(ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes a real science reference JSON and returns a
    'vortex-ready' symbolic descriptor.
    """
    mapped = registry.add_reference(ref)

    return {
        "vortex_node_id": f"SCIENCE::{mapped['reference_id']}",
        "label": mapped["title"],
        "concepts": mapped["key_concepts"],
        "symbolic_variables": mapped["symbolic_variables"],
        "safety_flags": mapped["safety_flags"],
        "mode": "SYMBOLIC_SCIENCE_ANCHOR"
    }

if __name__ == "__main__":
    import sys
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "Provide a single reference JSON on stdin."}, indent=2))
        raise SystemExit(1)

    ref = json.loads(raw)
    node = load_science_into_vortex(ref)
    print(json.dumps(node, indent=2))
