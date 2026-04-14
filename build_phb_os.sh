#!/bin/bash

echo "🧠 PHB NEURAL OS BUILD STARTING..."

# ----------------------------
# ROOT STRUCTURE
# ----------------------------
mkdir -p phb_neural_os/{api/routes,agents,memory,runtime,distribution,utils}

cd phb_neural_os || exit

# ----------------------------
# MAIN ENTRY
# ----------------------------
cat << 'EOF2' > main.py
from fastapi import FastAPI
from api.routes.message import router
from runtime.supervisor import start_supervisor

app = FastAPI(title="PHB Neural OS")

app.include_router(router)

@app.on_event("startup")
def boot():
    start_supervisor()

@app.get("/")
def root():
    return {"status": "PHB NEURAL OS ACTIVE"}
EOF2

# ----------------------------
# API LAYER
# ----------------------------
cat << 'EOF2' > api/routes/message.py
from fastapi import APIRouter, Request
from agents.orchestrator import run_orchestrator
from memory.memory_core import MemoryCore

router = APIRouter()
MEMORY = MemoryCore()

@router.post("/v2/message")
async def message(req: Request):
    data = await req.json()
    user_id = data.get("user_id", "default")
    msg = data.get("message", "")

    context = MEMORY.get(user_id)
    result = run_orchestrator(msg, context)

    MEMORY.store(user_id, msg, result)

    return result
EOF2

# ----------------------------
# AGENT LAYER
# ----------------------------
cat << 'EOF2' > agents/orchestrator.py
from agents.emotion_engine import detect_emotion

def run_orchestrator(message, memory):
    mood = detect_emotion(message)

    return {
        "input": message,
        "mood": mood,
        "response": generate(message, mood),
        "memory": memory
    }

def generate(message, mood):
    if "tired" in message:
        return "I’m here with you. Take it slowly."
    return "I understand."
EOF2

cat << 'EOF2' > agents/emotion_engine.py
def detect_emotion(text):
    text = text.lower()

    if "tired" in text or "exhausted" in text:
        return "soft"
    if "happy" in text:
        return "positive"
    return "neutral"
EOF2

# ----------------------------
# MEMORY LAYER
# ----------------------------
cat << 'EOF2' > memory/memory_core.py
class MemoryCore:
    def __init__(self):
        self.db = {}

    def store(self, user_id, msg, result):
        if user_id not in self.db:
            self.db[user_id] = []

        self.db[user_id].append({
            "message": msg,
            "response": result
        })

    def get(self, user_id):
        return self.db.get(user_id, [])
EOF2

# ----------------------------
# RUNTIME LAYER
# ----------------------------
cat << 'EOF2' > runtime/supervisor.py
import threading
import time

running = False

def loop():
    while True:
        print("[PHB OS] autonomous cycle running...")
        time.sleep(60)

def start_supervisor():
    global running
    if running:
        return

    running = True
    t = threading.Thread(target=loop, daemon=True)
    t.start()
EOF2

# ----------------------------
# DISTRIBUTION LAYER
# ----------------------------
cat << 'EOF2' > distribution/node.py
class PHBNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.peers = []

    def connect(self, peer):
        self.peers.append(peer)
EOF2

# ----------------------------
# REQUIREMENTS
# ----------------------------
cat << 'EOF2' > requirements.txt
fastapi
uvicorn
EOF2

# ----------------------------
# RUN SCRIPT
# ----------------------------
cat << 'EOF2' > run.sh
#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000
EOF2

chmod +x run.sh

echo "✅ PHB NEURAL OS BUILD COMPLETE"
echo "👉 Next: cd phb_neural_os && ./run.sh"
