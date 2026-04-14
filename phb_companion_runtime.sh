#!/data/data/com.termux/files/usr/bin/bash
set -e

# === CONFIG ===
PHB_API_URL="${PHB_API_URL:-https://phb-api-production.up.railway.app}"
PHB_API_PATH="${PHB_API_PATH:-/v1/companion}"
PHB_PY="${PHB_PY:-python3}"

# === CHECK PYTHON ===
if ! command -v "$PHB_PY" >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install with: pkg install python" >&2
  exit 1
fi

# === WRITE PYTHON RUNTIME ===
RUNTIME_PY="phb_companion_runtime.py"

cat << 'PYEOF' > "$RUNTIME_PY"
import sys
import json
import os
import urllib.request

def main():
    # Read JSON from stdin: {"message": "...", "context": {...}}
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            raise ValueError("No input received on stdin.")
        payload = json.loads(raw)
    except Exception as e:
        err = {"error": "invalid_input", "detail": str(e)}
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

    message = payload.get("message", "")
    context = payload.get("context", {}) or {}

    if not isinstance(message, str) or not message:
        err = {"error": "missing_message", "detail": "Field 'message' must be a non-empty string."}
        print(json.dumps(err, ensure_ascii=False))
        sys.exit(1)

    base_url = os.environ.get("PHB_API_URL", "https://phb-api-production.up.railway.app").rstrip("/")
    path = os.environ.get("PHB_API_PATH", "/v1/companion")
    url = f"{base_url}{path}"

    body = json.dumps({"message": message, "context": context}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            try:
                data = json.loads(resp_body)
            except json.JSONDecodeError:
                # Non-JSON response from server
                out = {
                    "error": "invalid_server_response",
                    "status_code": resp.getcode(),
                    "raw": resp_body,
                }
                print(json.dumps(out, ensure_ascii=False))
                sys.exit(1)
    except Exception as e:
        out = {"error": "network_or_server_error", "detail": str(e), "url": url}
        print(json.dumps(out, ensure_ascii=False))
        sys.exit(1)

    # Future-proof: always return full JSON, untouched
    print(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    main()
PYEOF

chmod +x "$RUNTIME_PY"

# === USAGE HINT ===
cat << 'HINT'
PHB Companion Runtime ready.

Example usage (Termux):

  echo '{"message":"hey PHB"}' | ./phb_companion_runtime.py

With custom API URL or path:

  PHB_API_URL="https://phb-api-production.up.railway.app" \
  PHB_API_PATH="/v1/companion" \
  echo '{"message":"hey PHB","context":{"node":"test"}}' | ./phb_companion_runtime.py

This is plug-and-play for:
  - API agents (JSON in → JSON out)
  - PHB nodes (can read her_mode + brain_state from the JSON)
HINT
