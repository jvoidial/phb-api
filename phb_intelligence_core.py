# PHB Intelligence Core (FIXED SAFE VERSION)

def run_intelligence_core(*args, **kwargs):
    try:
        user_message = kwargs.get("user_message") or (args[0] if len(args) > 0 else "")
        recent_context = kwargs.get("recent_context") or kwargs.get("context") or (args[1] if len(args) > 1 else {})

        return {
            "perception": f"Received: {user_message}",
            "context": recent_context or {},
            "plan": "PHB stable core execution",
            "reasoning": "Unified argument-safe core",
            "summary": f"User said: {user_message}",
            "status": "ok"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
