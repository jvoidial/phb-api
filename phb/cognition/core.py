from phb.brain.global_brain import GlobalBrain
from phb.memory.intelligence import categorize
from phb.meta.self_reflection import reflect
from phb.brain.p2p_live import live_sync
from datetime import datetime, timezone

BRAIN = GlobalBrain()

def think(message, state=None, user_id="default"):
    brain = BRAIN.load()

    # init structures
    brain.setdefault("memory", {})
    brain.setdefault("timeline", [])
    brain.setdefault("meta", {})

    now = datetime.now(timezone.utc)

    # store memory
    brain["memory"][str(now.timestamp())] = {
        "user": user_id,
        "input": message,
        "time": now.isoformat()
    }

    # timeline
    brain["timeline"].append({
        "event": "interaction",
        "message": message,
        "time": now.isoformat()
    })

    # 🧠 intelligence layer
    categorized = categorize(brain["memory"])

    # 🔁 self reflection
    brain = reflect(brain)

    # 🌍 P2P live sync
    sync_status = live_sync()

    # save
    BRAIN.save(brain)

    return {
        "engine": "cognition-core-v3-intelligent",
        "input": message,
        "user_id": user_id,
        "brain_snapshot": {
            "system": brain.get("system"),
            "memory_count": len(brain["memory"]),
            "important_memories": len(categorized["important"]),
            "recent_memories": len(categorized["recent"]),
            "timeline_events": len(brain["timeline"])
        },
        "reflection": brain["meta"].get("reflection"),
        "p2p_sync": sync_status,
        "response": f"PHB intelligently processed: {message}",
        "timestamp": now.isoformat()
    }
