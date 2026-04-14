#!/data/data/com.termux/files/usr/bin/python3
import sys
import json
import os
import urllib.request

def main():
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            raise ValueError("No input received on stdin.")
        payload = json.loads(raw)
    except Exception as e:
        print(json.dumps({"error":"invalid_input","detail":str(e)}, ensure_ascii=False))
        sys.exit(1)

    message = payload.get("message","")
    context = payload.get("context",{}) or {}

    if not isinstance(message,str) or not message:
        print(json.dumps({"error":"missing_message","detail":"Field 'message' must be a non-empty string."}, ensure_ascii=False))
        sys.exit(1)

    base_url = os.environ.get("PHB_API_URL","https://phb-api-production.up.railway.app").rstrip("/")
    path = os.environ.get("PHB_API_PATH","/v1/companion")
    url = f"{base_url}{path}"

    body = json.dumps({"message":message,"context":context}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            try:
                data = json.loads(resp_body)
            except json.JSONDecodeError:
                print(json.dumps({"error":"invalid_server_response","raw":resp_body}, ensure_ascii=False))
                sys.exit(1)
    except Exception as e:
        print(json.dumps({"error":"network_or_server_error","detail":str(e),"url":url}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    main()
