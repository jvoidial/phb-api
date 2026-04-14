from datetime import datetime, timezone

def reflect(brain):
    memory = brain.get("memory", {})

    reflection = {
        "total_memories": len(memory),
        "last_update": datetime.now(timezone.utc).isoformat(),
        "status": "stable"
    }

    if len(memory) > 10:
        reflection["status"] = "learning"
    if len(memory) > 50:
        reflection["status"] = "evolving"

    brain["meta"]["reflection"] = reflection
    return brain
