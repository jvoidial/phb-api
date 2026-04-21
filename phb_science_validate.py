#!/usr/bin/env python3
import json
import sys
from phb_science_plugin import validate_reference

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "No JSON input provided."}, indent=2))
        sys.exit(1)

    try:
        ref = json.loads(raw)
        validate_reference(ref)
        print(json.dumps({"valid": True}, indent=2))
    except Exception as e:
        print(json.dumps({"valid": False, "details": str(e)}, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
