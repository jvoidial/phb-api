import sys
import os
import json

# =========================
# PHB BOOTSTRAP FIX LAYER
# =========================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure root is in Python path (fixes "No module named phb")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Safe JSON encoder helper (prevents FastAPI / object crashes)
def safe_json(obj):
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return json.dumps({"error": "serialization_failed"})

# Safe import wrapper for PHB modules
def safe_import(module_path):
    try:
        module = __import__(module_path, fromlist=["*"])
        return module
    except Exception as e:
        return type("DummyModule", (), {
            "__error__": str(e),
            "run": lambda *args, **kwargs: "module_not_available"
        })()

print("🧠 PHB BOOTSTRAP FIX LOADED")
print("📦 PYTHONPATH ROOT FIX ACTIVE")
print("🔧 JSON SAFE MODE ENABLED")
