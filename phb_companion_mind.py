from typing import Dict, Any
from phb_brain import run_phb_brain

def run_companion_mind(user_message: str, recent_context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    brain = run_phb_brain(user_message)

    state = brain["brain_state"]
    mood = state["mood"]
    energy = state["energy"]
    arc = state["arc"]

    # Synthetic-human voice shaping
    if mood in ["soft", "gentle"]:
        style_prefix = "You matter here, so I’m moving softly with you. "
    elif mood in ["bright", "engaged"]:
        style_prefix = "I’m right here with you, awake and tuned in. "
    elif arc in ["stabilising", "supportive"]:
        style_prefix = "Let’s keep this steady and kind while we work through it. "
    else:
        style_prefix = "Okay, I’m here, thinking this through with you. "

    final_text = style_prefix + brain["summary"]

    return {
        "raw_brain": brain,
        "final_companion_text": final_text,
        "energy": energy,
        "mood": mood,
        "arc": arc,
        "veil": state["veil"],
        "topics": state["last_topics"],
    }
