#!/data/data/com.termux/files/usr/bin/bash
set -e

# === CONFIG ===
PHB_API_URL="${PHB_API_URL:-https://phb-api-production.up.railway.app}"
PHB_API_PATH="${PHB_API_PATH:-/v1/companion}"
PYBIN="/data/data/com.termux/files/usr/bin/python3"

# === CHECK PYTHON ===
if [ ! -x "$PYBIN" ]; then
  echo "Python3 not found. Install with: pkg install python" >&2
  exit 1
fi

# === WRITE PYTHON HYPER-ENGINE RUNTIME ===
cat << 'PYEOF' > phb_hyper_engine.py
#!/data/data/com.termux/files/usr/bin/python3
import sys, json, os, urllib.request

def main():
    # Read JSON input
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            raise ValueError("No input received.")
        payload = json.loads(raw)
    except Exception as e:
        print(json.dumps({"error":"invalid_input","detail":str(e)}))
        return

    message = payload.get("message","")
    context = payload.get("context",{}) or {}

    if not isinstance(message,str) or not message:
        print(json.dumps({"error":"missing_message","detail":"Field 'message' must be non-empty."}))
        return

    # API target
    base = os.environ.get("PHB_API_URL","https://phb-api-production.up.railway.app").rstrip("/")
    path = os.environ.get("PHB_API_PATH","/v1/companion")
    url = f"{base}{path}"

    # Build request
    body = json.dumps({"message":message,"context":context}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}, method="POST")

    # Send request
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
            try:
                data = json.loads(text)
            except:
                print(json.dumps({"error":"invalid_server_response","raw":text}))
                return
    except Exception as e:
        print(json.dumps({"error":"network_or_server_error","detail":str(e),"url":url}))
        return

    # Output final JSON
    print(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    main()
PYEOF

chmod +x phb_hyper_engine.py

echo "PHB Hyper-Engine Runtime installed."
echo ""
echo "Test:"
echo "  echo '{\"message\":\"hello\"}' | ./phb_hyper_engine.py"
