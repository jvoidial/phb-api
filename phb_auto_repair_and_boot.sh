#!/bin/bash

echo "🧠 PHB FULL AUTO-REPAIR + BOOT SYSTEM STARTING..."

BASE="/data/data/com.termux/files/home/phb-api"
cd $BASE || exit

# ----------------------------
# 1. CLEAN OLD PROCESSES
# ----------------------------
pkill -f uvicorn || true
pkill -f python || true
sleep 1

# ----------------------------
# 2. FIX PYTHON PACKAGE STRUCTURE
# ----------------------------
echo "🔧 Fixing Python package structure..."

mkdir -p event_engine worker_engine memory_store kernel observability cluster

touch event_engine/__init__.py
touch worker_engine/__init__.py
touch memory_store/__init__.py
touch kernel/__init__.py
touch cluster/__init__.py
touch observability/__init__.py

# ----------------------------
# 3. FORCE PYTHON PATH FIX
# ----------------------------
export PYTHONPATH=.

# ----------------------------
# 4. SAFE EVENT ENGINE (if missing)
# ----------------------------
cat > event_engine/engine.py << 'PY'
import json, os, time

DB="event_log.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else []

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def emit(event):
    db = load()
    event["time"]=time.time()
    event["status"]="queued"
    db.append(event)
    save(db)

def get_next():
    db = load()
    for e in db:
        if e.get("status")=="queued":
            e["status"]="processing"
            save(db)
            return e
    return None
PY

# ----------------------------
# 5. SAFE WORKER ENGINE
# ----------------------------
cat > worker_engine/worker.py << 'PY'
import time
from event_engine.engine import get_next, load, save

def process(event):
    msg = event.get("message","")

    mood = "neutral"
    if any(x in msg.lower() for x in ["tired","overwhelmed","sad"]):
        mood = "soft"

    return {
        "response":"PHB processed",
        "mood":mood
    }

while True:
    event = get_next()

    if event:
        try:
            event["result"] = process(event)
            event["status"] = "done"
        except Exception as e:
            event["status"] = "failed"
            event["error"] = str(e)

        save(load())

    time.sleep(1)
PY

# ----------------------------
# 6. MEMORY STORE
# ----------------------------
cat > memory_store/memory.py << 'PY'
import json, os, time

DB="memory.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def write(user_id,text):
    db = load()
    db.setdefault(user_id,[])
    db[user_id].append({"text":text,"time":time.time()})
    save(db)

def read(user_id):
    db = load()
    return db.get(user_id,[])
PY

# ----------------------------
# 7. KERNEL CORE
# ----------------------------
cat > kernel/core.py << 'PY'
from event_engine.engine import emit
from memory_store.memory import write

def handle(message,user_id):

    emit({
        "message":message,
        "user_id":user_id,
        "type":"message"
    })

    write(user_id,message)

    return {
        "status":"queued",
        "mode":"PHB_AUTO_SYSTEM"
    }
PY

# ----------------------------
# 8. MAIN API
# ----------------------------
cat > main.py << 'PY'
from fastapi import FastAPI, Request
from kernel.core import handle

app = FastAPI(title="PHB AUTO SYSTEM")

@app.post("/message")
async def msg(req:Request):
    d = await req.json()
    return handle(d.get("message",""), d.get("user_id","default"))

@app.get("/")
def root():
    return {"status":"PHB AUTO SYSTEM ONLINE"}
PY

# ----------------------------
# 9. SAFE RUN SCRIPT
# ----------------------------
cat > run.sh << 'SH'
#!/bin/bash

echo "🧠 PHB AUTO SYSTEM BOOTING"

cd /data/data/com.termux/files/home/phb-api

export PYTHONPATH=.

pkill -f uvicorn || true
pkill -f python || true
sleep 1

python worker_engine/worker.py &
uvicorn main:app --host 0.0.0.0 --port 8000

SH

chmod +x run.sh

echo "✅ PHB AUTO SYSTEM READY"
echo "👉 RUN: ./run.sh"
