import json

def safe_response(data):
    try:
        return json.loads(json.dumps(data, default=str))
    except Exception:
        return {"error": "serialization_failed"}
