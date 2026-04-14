from phb.brain.global_brain import GlobalBrain
from phb.memory.recall_engine import build_context
from phb.agent.goal_engine import generate_goals, prioritize
from phb.meta.self_reflection import reflect
from phb.brain.p2p_live import live_sync
from datetime import datetime, timezone

BRAIN = GlobalBrain()

def think(message, state=None, user_id="default"):
    brain = BRAIN.load()

    brain.setdefault("memory", {})
    brain.setdefault("timeline", [])
    brain.setdefault("meta", {})

    now = datetime.now(timezone.utc)

    # ------------------------
    # STORE MEMORY
    # ------------------------
    brain["memory"][str(now.timestamp())] = {
        "input": message,
        "user": user_id,
        "time": now.isoformat()
    }

    brain["timeline"].append({
        "event": "input",
        "message": message,
        "time": now.isoformat()
    })

    # ------------------------
    # MEMORY RECALL
    # ------------------------
    context = build_context(brain["memory"], message)

    # ------------------------
    # GOAL GENERATION (NEW)
    # ------------------------
    goals = generate_goals(brain["memory"], brain["timeline"])
    goals = prioritize(goals)

    # ------------------------
    # REFLECTION + SYNC
    # ------------------------
    brain = reflect(brain)
    sync = live_sync()

    BRAIN.save(brain)

    # ------------------------
    # RESPONSE
    # ------------------------
    return {
        "engine": "cognition-core-v3.80-agent-loop",
        "input": message,

        "memory_recall": context["context_summary"],

        "active_goals": goals,

        "brain_snapshot": {
            "memory_count": len(brain["memory"]),
            "timeline_events": len(brain["timeline"])
        },

        "p2p_sync": sync,

        "response": f"PHB agent processed: {message}",
        "timestamp": now.isoformat()
    }
