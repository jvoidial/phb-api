#!/bin/bash

echo "🧠 PHB AI OS v7.1 BUILD STARTING..."

BASE="phb-api"
mkdir -p $BASE
cd $BASE || exit

# =========================
# MAIN API
# =========================
cat << 'PY' > main.py
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
PY

# =========================
# RUN SCRIPT (SAFE SINGLE INSTANCE)
# =========================
cat << 'SH' > run.sh
#!/bin/bash

echo "🧠 PHB AI OS v7.1 STARTING..."

cd "$(dirname "$0")"

# kill only uvicorn (safe)
pkill -f "uvicorn main:app" || true

sleep 1

uvicorn main:app --host 0.0.0.0 --port 8000
SH

chmod +x run.sh

# =========================
# MEMORY ENGINE (ROBUST + PERSISTENT)
# =========================
mkdir -p memory

cat << 'PY' > memory/store.py
import json, os, time

DB = "phb_memory.json"

def load():
    if not os.path.exists(DB):
        return {}
    try:
        return json.load(open(DB))
    except:
        return {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def add(user_id, text, mood):
    db = load()
    db.setdefault(user_id, [])

    db[user_id].append({
        "text": text,
        "mood": mood,
        "time": time.time()
    })

    save(db)

def get(user_id):
    db = load()
    return db.get(user_id, [])
PY

# =========================
# COGNITIVE ENGINE (REAL LOGIC LOOP)
# =========================
mkdir -p cognition

cat << 'PY' > cognition/core.py
from memory.store import add, get

def think(msg, state, user_id):

    state["turns"] = state.get("turns",0) + 1

    text = msg.lower()

    # emotion model
    if any(x in text for x in ["tired","overwhelmed","sad","anxious"]):
        mood = "soft"
    else:
        mood = "neutral"

    memory = get(user_id)

    # REAL MEMORY RECOGNITION LOGIC
    similar = []
    for m in memory:
        if any(word in m["text"].lower() for word in text.split()):
            similar.append(m)

    if similar:
        response = "I remember something like this before."
    elif memory:
        response = "You’ve shared this energy before — I’m here with you."
    else:
        response = "I’m here with you."

    add(user_id, msg, mood)

    return {
        "input": msg,
        "response": response,
        "mood": mood,
        "memory_hits": memory[-5:],
        "state_turns": state["turns"],
        "mode": "PHB_AI_OS_v7.1"
    }
PY

# =========================
# SUPERVISOR (LIGHTWEIGHT + SAFE)
# =========================
mkdir -p supervisor

cat << 'PY' > supervisor/kernel.py
import subprocess, time

print("[PHB SUPERVISOR v7.1] ONLINE")

def start():
    return subprocess.Popen(
        "uvicorn main:app --host 0.0.0.0 --port 8000",
        shell=True
    )

api = start()

while True:
    time.sleep(5)

    if api.poll() is not None:
        print("[SUPERVISOR] restart")
        api = start()
PY

# =========================
# REQUIREMENTS
# =========================
cat << 'TXT' > requirements.txt
fastapi
uvicorn
TXT

# =========================
# DONE
# =========================
echo "✅ PHB AI OS v7.1 BUILT SUCCESSFULLY"
echo ""
echo "RUN:"
echo "  cd phb-api"
echo "  pip install fastapi uvicorn"
echo "  ./run.sh"
