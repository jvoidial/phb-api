from phb_intelligence_core import run_intelligence_core

def run_intelligence_core_1(session_id, user_message, recent_context=None, emotion=None, tone=None):
    return run_intelligence_core(
        session_id=session_id,
        user_message=user_message,
        recent_context=recent_context,
        emotion=emotion,
        tone=tone,
    )
