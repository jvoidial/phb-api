#!/usr/bin/env python3
import json
import sys
from typing import Dict, Any
from phb_science_registry import PHBScienceRegistry

"""
PHB ACADEMIC PAPER INGESTION ENGINE
-----------------------------------
Takes an academic paper ABSTRACT or SUMMARY (provided by the user)
and converts it into a PHB Science Reference JSON object.

Input (stdin JSON):
{
  "title": "...",
  "authors": ["..."],
  "year": 2024,
  "url": "https://...",
  "abstract": "..."
}

Output:
PHB science mapping JSON, registered in PHBScienceRegistry.
"""

def extract_concepts(text: str):
    words = text.lower().replace(",", "").replace(".", "").split()
    keywords = [w for w in words if len(w) > 6]
    return list(dict.fromkeys(keywords))[:10]

def build_reference(data: Dict[str, Any]) -> Dict[str, Any]:
    abstract = data["abstract"]
    concepts = extract_concepts(abstract)

    return {
        "phb_reference_id": f"REF_{data['year']}_{len(concepts)}",
        "source_platform": "user_provided_abstract",
        "source_url": data["url"],
        "title": data["title"],
        "authors": data["authors"],
        "year": data["year"],
        "abstract": abstract,
        "key_concepts": concepts,
        "phb_mapping": {
            "symbolic_layer_only": True,
            "mapped_variables": {
                c: c.replace(" ", "_") for c in concepts
            }
        },
        "safety_flags": {
            "clinical_use": False,
            "regulatory_status": "NON_MEDICAL_NON_CLINICAL",
            "requires_human_expert_for_interpretation": True
        }
    }

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({
            "error": "Provide JSON with: title, authors, year, url, abstract"
        }, indent=2))
        return

    try:
        data = json.loads(raw)
        ref = build_reference(data)

        registry = PHBScienceRegistry()
        mapped = registry.add_reference(ref)

        print(json.dumps(mapped, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": "Ingestion failed",
            "details": str(e)
        }, indent=2))

if __name__ == "__main__":
    main()
