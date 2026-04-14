
from datetime import datetime, timezone

def decompose_goal(message):
    """
    Break input into multi-step plan
    """

    base_steps = [
        "interpret_intent",
        "retrieve_context",
        "generate_solution",
        "validate_output"
    ]

    # dynamic expansion
    if "learn" in message:
        base_steps.insert(2, "store_knowledge")

    if "predict" in message:
        base_steps.insert(2, "run_prediction_model")

    return {
        "goal": message,
        "steps": base_steps,
        "created": datetime.now(timezone.utc).isoformat(),
        "status": "planned"
    }
