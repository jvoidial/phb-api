from phb.brain.global_brain import GlobalBrain
from datetime import datetime, timezone

# 🧠 brainstep: cognition linked to global brain state
BRAIN = GlobalBrain()

def think(message, state=None, user_id="default"):
    """
    PHB brainstep cognition core:
    - reads unified global brain state
    - returns structured cognition response
    """

    brain = BRAIN.load()

    return {
        "engine": "cognition-core-brainstep-v1",
        "input": message,
        "user_id": user_id,

        "brain_snapshot": {
            "system": brain.get("system"),
            "memory_layers": list(brain.get("memory", {}).keys()),
            "timeline_events": len(brain.get("timeline", []))
        },

        "state": state or {},
        "response": f"PHB brainstep processed: {message}",

        "timestamp": datetime.now(timezone.utc).isoformat()
    }
