#!/bin/bash

echo "🧠 PATCH: ENABLE BRAIN LEARNING + MEMORY WRITE"

mkdir -p phb/cognition

cat << 'PYEOF' > phb/cognition/core.py
from phb.brain.global_brain import GlobalBrain
from datetime import datetime, timezone

BRAIN = GlobalBrain()

def think(message, state=None, user_id="default"):
    brain = BRAIN.load()

    # --- INIT STRUCTURE ---
    if "memory" not in brain:
        brain["memory"] = {}

    if "timeline" not in brain:
        brain["timeline"] = []

    # --- WRITE MEMORY ---
    brain["memory"][str(datetime.now(timezone.utc).timestamp())] = {
        "user": user_id,
        "input": message
    }

    # --- WRITE TIMELINE ---
    brain["timeline"].append({
        "event": "interaction",
        "message": message,
        "user": user_id,
        "time": datetime.now(timezone.utc).isoformat()
    })

    # --- SAVE ---
    BRAIN.save(brain)

    return {
        "engine": "cognition-core-brainstep-v2",
        "input": message,
        "user_id": user_id,
        "brain_snapshot": {
            "system": brain.get("system"),
            "memory_layers": list(brain.get("memory", {}).keys()),
            "timeline_events": len(brain.get("timeline", []))
        },
        "state": state,
        "response": f"PHB learned: {message}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
PYEOF

# clear cache
find . -name "__pycache__" -type d -exec rm -rf {} +

# restart
pkill -f uvicorn || true
sleep 1
bash phb-api/run.sh &

sleep 3

echo "🧪 Testing learning..."

curl -s -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{"message":"learning test"}'

echo ""
echo "🟢 BRAIN LEARNING PATCH COMPLETE"
