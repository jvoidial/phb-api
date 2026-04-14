from phb.brain.global_brain import GlobalBrain
from phb.memory.recall_engine import build_context
from phb.agent.goal_engine import generate_goals, prioritize
from phb.world_model.model import WorldModel
from phb.meta.self_reflection import reflect
from phb.brain.p2p_live import live_sync
from datetime import datetime, timezone

BRAIN = GlobalBrain()
WORLD = WorldModel()

def think(message, state=None, user_id="default"):
    brain = BRAIN.load()

    brain.setdefault("memory", {})
    brain.setdefault("timeline", [])
    brain.setdefault("meta", {})

    now = datetime.now(timezone.utc)

    # -------------------------
    # STORE MEMORY
    # -------------------------
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

    # -------------------------
    # RECALL
    # -------------------------
    context = build_context(brain["memory"], message)

    # -------------------------
    # WORLD MODEL UPDATE
    # -------------------------
    WORLD.update(message, len(brain["memory"]))

    predicted_intent = WORLD.predict_next_intent()
    memory_trend = WORLD.predict_memory_trend()

    # -------------------------
    # GOALS
    # -------------------------
    goals = prioritize(
        generate_goals(brain["memory"], brain["timeline"])
    )

    # -------------------------
    # REFLECTION + SYNC
    # -------------------------
    brain = reflect(brain)
    sync = live_sync()

    BRAIN.save(brain)

    return {
        "engine": "cognition-core-v3.90-world-model",

        "input": message,

        # 🧠 MEMORY + RECALL
        "memory_recall": context["context_summary"],

        # 🔮 WORLD MODEL OUTPUT
        "world_model": {
            "predicted_intent": predicted_intent,
            "memory_trend": memory_trend
        },

        # 🎯 GOALS
        "active_goals": goals,

        # 🧠 STATE SNAPSHOT
        "brain_snapshot": {
            "memory_count": len(brain["memory"]),
            "timeline_events": len(brain["timeline"])
        },

        "p2p_sync": sync,

        "response": f"PHB world-model processed: {message}",

        "timestamp": now.isoformat()
    }
