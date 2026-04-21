#!/usr/bin/env python3
import json
import sys
from typing import Dict, Any

"""
PHB REAL SCIENCE REFERENCE PLUGIN (FICTIONAL + SAFE)

This module allows PHB to ingest *real scientific papers* (e.g. from Academia.edu)
as structured JSON references WITHOUT treating them as medical instructions.

It maps:
- real scientific concepts → symbolic PHB variables
- abstracts → summaries
- models → symbolic engines
- limitations → safety flags

This keeps PHB grounded, safe, and compliant.
"""


# -----------------------------
# 1. VALIDATION
# -----------------------------

def validate_reference(ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures the JSON reference contains required fields.
    """
    required = [
        "phb_reference_id",
        "source_platform",
        "source_url",
        "title",
        "authors",
        "year",
        "abstract",
        "key_concepts",
        "phb_mapping",
        "safety_flags"
    ]

    missing = [k for k in required if k not in ref]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    return ref


# -----------------------------
# 2. MAPPING TO PHB SYMBOLIC LAYER
# -----------------------------

def map_to_phb(ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a real science reference into a PHB-ready symbolic mapping.
    """
    mapping = ref["phb_mapping"]["mapped_variables"]

    return {
        "reference_id": ref["phb_reference_id"],
        "title": ref["title"],
        "authors": ref["authors"],
        "year": ref["year"],
        "key_concepts": ref["key_concepts"],
        "symbolic_variables": mapping,
        "symbolic_only": ref["phb_mapping"]["symbolic_layer_only"],
        "safety_flags": ref["safety_flags"],
        "notes": "Mapped from real science → symbolic PHB layer. Not clinical."
    }


# -----------------------------
# 3. MAIN ENTRYPOINT
# -----------------------------

def main():
    """
    Usage:
      echo '{...}' | python3 phb_science_plugin.py

    Input: JSON describing a real science reference.
    Output: PHB symbolic mapping JSON.
    """
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            raise ValueError("No JSON input provided.")

        ref = json.loads(raw)
        validated = validate_reference(ref)
        mapped = map_to_phb(validated)

        print(json.dumps(mapped, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": "Invalid reference JSON",
            "details": str(e)
        }, indent=2))


if __name__ == "__main__":
    main()
