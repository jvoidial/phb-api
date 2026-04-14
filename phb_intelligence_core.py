def run_intelligence_core(user_message: str = "", recent_context: dict = None):
    if recent_context is None:
        recent_context = {}
    return {
        "perception": f"Received: {user_message}",
        "context": recent_context,
        "plan": "stable",
        "reasoning": "fixed signature",
        "summary": f"User: {user_message}",
        "status": "ok"
    }
