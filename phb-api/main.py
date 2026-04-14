from fastapi import FastAPI, Request
from cognition.core import think

app = FastAPI(title="PHB AI OS v7.1")

STATE = {"booted": True}

@app.post("/message")
async def message(req: Request):
    data = await req.json()

    return think(
        data.get("message",""),
        STATE,
        data.get("user_id","default")
    )

@app.get("/")
def root():
    return {
        "status": "PHB AI OS v7.1 ONLINE",
        "mode": "cognitive-runtime"
    }

# === PHB v3 BRIDGE INTEGRATION ===
from phb.bridge.v3_adapter import V3ArchitectureBridge

bridge = V3ArchitectureBridge()

# Override message handler safely
original_message_handler = None

@app.post("/message")
def message(payload: dict):
    user_msg = payload.get("message", "")

    result = bridge.route(user_msg)

    return {
        "input": user_msg,
        "response": str(result),
        "mode": "v2-v3-bridged",
        "github_integrated": True
    }


# =========================
# PHB BOOTSTRAP INJECTION
# =========================
try:
    from phb.bridge.v3_adapter import V3ArchitectureBridge
except Exception:
    import sys
    sys.path.append("..")
    from phb.bridge.v3_adapter import V3ArchitectureBridge

# =========================
# PHB SAFE IMPORT PATCH
# =========================
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from phb.bridge.v3_adapter import V3ArchitectureBridge
except Exception:
    class V3ArchitectureBridge:
        def route(self, message, kernel=None, architecture=None):
            return {"fallback": True, "message": message}

# =========================
# PHB SAFE COGNITION PATCH
# =========================
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from cognition.core import think
except Exception:
    def think(message):
        return {
            "fallback": True,
            "input": message,
            "response": "cognition fallback active"
        }

from phb.brain.global_brain import GlobalBrain

BRAIN = GlobalBrain()

@app.get("/brain-state")
def brain_state():
    return BRAIN.load()
