def run_intelligence_core(user_message: str, recent_context: dict | None = None):
    # Import inside function to avoid circular import
    from phb_companion_mind import run_companion_mind

    result = run_companion_mind(user_message, recent_context or {})

    return {
        "perception": result["raw_brain"]["perception"],
        "context": recent_context or {},
        "plan": result["raw_brain"]["plan"],
        "reasoning": result["raw_brain"]["reasoning"],
        "summary": result["final_companion_text"],
        "status": "ok",
        "her_mode": {
            "energy": result["energy"],
            "mood": result["mood"],
            "veil": result["veil"],
            "turns": result["raw_brain"]["brain_state"]["turns"],
        },
        "brain_state": result["raw_brain"]["brain_state"],
    }
