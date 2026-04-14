
from phb.brain.global_brain import GlobalBrain
from phb.memory.recall_engine import build_context
from phb.agent.goal_engine import generate_goals, prioritize
from phb.world_model.model import WorldModel
from phb.planner.planner import decompose_goal
from phb.execution.engine import add_task, get_state
from phb.meta.self_reflection import reflect
from phb.brain.p2p_live import live_sync
from datetime import datetime, timezone

BRAIN = GlobalBrain()
WORLD = WorldModel()

def think(message, state=None, user_id="default"):

    brain = BRAIN.load()
    brain.setdefault("memory", {})
    brain.setdefault("timeline", [])

    now = datetime.now(timezone.utc)

    # -----------------------
    # MEMORY WRITE
    # -----------------------
    brain["memory"][str(now.timestamp())] = message
    brain["timeline"].append({"event": "input", "msg": message})

    # -----------------------
    # RECALL
    # -----------------------
    context = build_context(brain["memory"], message)

    # -----------------------
    # WORLD MODEL
    # -----------------------
    WORLD.update(message, len(brain["memory"]))

    prediction = WORLD.predict_next_intent()

    # -----------------------
    # GOALS
    # -----------------------
    goals = prioritize(generate_goals(brain["memory"], brain["timeline"]))

    # -----------------------
    # LONG HORIZON PLANNING (NEW)
    # -----------------------
    plan = decompose_goal(message)

    add_task(plan)

    queue_state = get_state()

    # -----------------------
    # SYNC + REFLECTION
    # -----------------------
    brain = reflect(brain)
    live_sync()

    BRAIN.save(brain)

    return {
        "engine": "cognition-core-v4-long-horizon",

        "input": message,

        "memory_recall": context["context_summary"],

        "world_model_prediction": prediction,

        "active_goals": goals,

        "execution_queue": queue_state,

        "plan": plan,

        "brain_snapshot": {
            "memory_count": len(brain["memory"]),
            "timeline_events": len(brain["timeline"])
        },

        "response": f"PHB long-horizon agent processed: {message}",

        "timestamp": now.isoformat()
    }
