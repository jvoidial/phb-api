from phb.brain.global_brain import GlobalBrain
from phb.memory.recall_engine import build_context
from phb.memory.intelligence import categorize
from phb.meta.self_reflection import reflect
from phb.brain.p2p_live import live_sync
from datetime import datetime, timezone

BRAIN = GlobalBrain()

def think(message, state=None, user_id="default"):
    brain = BRAIN.load()

    brain.setdefault("memory", {})
    brain.setdefault("timeline", {})
    brain.setdefault("meta", {})

    now = datetime.now(timezone.utc)

    # -----------------------
    # 🧠 RECALL BEFORE WRITE
    # -----------------------
    context = build_context(brain["memory"], message)

    # -----------------------
    # STORE MEMORY
    # -----------------------
    brain["memory"][str(now.timestamp())] = {
        "user": user_id,
        "input": message,
        "time": now.isoformat()
    }

    brain["timeline"][str(now.timestamp())] = {
        "event": "interaction",
        "message": message
    }

    # -----------------------
    # INTELLIGENCE + REFLECTION
    # -----------------------
    categorized = categorize(brain["memory"])
    brain = reflect(brain)
    sync_status = live_sync()

    BRAIN.save(brain)

    return {
        "engine": "cognition-core-v4-recall",
        "input": message,
        "user_id": user_id,

        # 🧠 NEW: MEMORY RECALL OUTPUT
        "memory_recall": {
            "matched_context": context["context_summary"],
            "top_matches": context["matches"]
        },

        "brain_snapshot": {
            "memory_count": len(brain["memory"]),
            "timeline_events": len(brain["timeline"]),
            "important_memories": len(categorized["important"])
        },

        "reflection": brain["meta"].get("reflection"),
        "p2p_sync": sync_status,

        "response": f"PHB recalled + processed: {message}",
        "timestamp": now.isoformat()
    }
