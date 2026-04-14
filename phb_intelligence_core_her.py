from phb_brain import run_phb_brain

# Clean, unified HER wrapper using the new PHB brain module
def run_intelligence_core(user_message: str, recent_context: dict | None = None):
    brain_result = run_phb_brain(user_message)

    return {
        "perception": brain_result["perception"],
        "context": recent_context or {},
        "plan": brain_result["plan"],
        "reasoning": brain_result["reasoning"],
        "summary": brain_result["summary"],
        "status": "ok",
        "her_mode": {
            "energy": brain_result["brain_state"]["energy"],
            "mood": brain_result["brain_state"]["mood"],
            "veil": brain_result["brain_state"]["veil"],
            "turns": brain_result["brain_state"]["turns"],
        },
        "brain_state": brain_result["brain_state"],
    }
