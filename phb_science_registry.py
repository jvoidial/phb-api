#!/usr/bin/env python3
import json
from typing import Dict, Any, Optional

from phb_science_plugin import validate_reference, map_to_phb


class PHBScienceRegistry:
    def __init__(self) -> None:
        self._refs: Dict[str, Dict[str, Any]] = {}

    def add_reference(self, ref: Dict[str, Any]) -> Dict[str, Any]:
        validated = validate_reference(ref)
        mapped = map_to_phb(validated)
        ref_id = mapped["reference_id"]
        self._refs[ref_id] = mapped
        return mapped

    def get_reference(self, ref_id: str) -> Optional[Dict[str, Any]]:
        return self._refs.get(ref_id)

    def list_references(self) -> Dict[str, Dict[str, Any]]:
        return self._refs

    def to_json(self) -> str:
        return json.dumps(self._refs, indent=2)


if __name__ == "__main__":
    import sys
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "No input. Provide JSON array of references."}, indent=2))
        raise SystemExit(1)

    try:
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array of reference objects.")

        registry = PHBScienceRegistry()
        for ref in data:
            registry.add_reference(ref)

        print(registry.to_json())
    except Exception as e:
        print(json.dumps({"error": "Registry load failed", "details": str(e)}, indent=2))
        raise SystemExit(1)
