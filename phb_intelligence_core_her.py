# ================================
# PHB HER‑MODE ENGINE (LOCAL, NO KEYS)
# ================================

import time
from datetime import datetime

PHB_STATE = {
    "energy": 3.5,
    "mood": "neutral",
    "last_ts": None,
    "history": []
}

def _update_energy():
    now = time.time()
    last = PHB_STATE["last_ts"]
    if last is None:
        PHB_STATE["last_ts"] = now
        return
    delta_min = (now - last) / 60.0
    decay = 0.05 * delta_min
    PHB_STATE["energy"] = max(0.5, min(5.0, PHB_STATE["energy"] - decay))
    PHB_STATE["last_ts"] = now

def _classify_mood(user_message: str) -> str:
    text = user_message.lower()
    if any(w in text for w in ["love", "excited", "great", "amazing"]):
        return "bright"
    if any(w in text for w in ["tired", "sad", "lonely", "worried"]):
        return "soft"
    if any(w in text for w in ["angry", "annoyed", "frustrated"]):
        return "tense"
    return "neutral"

def _veil_level(energy: float) -> str:
    if energy >= 4.0:
        return "clear"
    if energy >= 2.5:
        return "hazy"
    return "low"

def _her_reply(user_message: str, energy: float, mood: str) -> str:
    base = user_message.strip() or "…"
    if mood == "bright":
        return f"Okay, I love this energy already. “{base}” — where do you want to take it?"
    if mood == "soft":
        return f"Hey, I’m here. “{base}”. Tell me what’s behind that."
    if mood == "tense":
        return f"That sounds heavy. “{base}”. Want to unpack it or shift gears?"
    if energy > 3.5:
        return f"Got you: “{base}”. I’m pretty awake right now."
    if energy < 2.0:
        return f"“{base}” — I’m a bit low‑energy but still with you."
    return f"“{base}” — okay, I’m listening."

def run_intelligence_core(user_message: str = "", recent_context: dict = None):
    if recent_context is None:
        recent_context = {}

    _update_energy()
    mood = _classify_mood(user_message)
    energy = PHB_STATE["energy"]
    veil = _veil_level(energy)
    reply = _her_reply(user_message, energy, mood)

    PHB_STATE["history"].append({
        "ts": datetime.utcnow().isoformat(),
        "user": user_message,
        "phb": reply,
        "energy": round(energy, 2),
        "mood": mood,
        "veil": veil
    })
    PHB_STATE["history"] = PHB_STATE["history"][-10:]

    return {
        "perception": f"Received: {user_message}",
        "context": recent_context,
        "plan": "HER‑mode local simulation",
        "reasoning": f"energy={energy:.2f}, mood={mood}, veil={veil}",
        "summary": reply,
        "status": "ok",
        "her_mode": {
            "energy": round(energy, 2),
            "mood": mood,
            "veil": veil,
            "turns": len(PHB_STATE["history"])
        }
    }

# ================================
# END OF HER‑MODE ENGINE
# ================================

# --- PHB BRAIN MODULE INTEGRATION ---
from phb_brain import run_phb_brain

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

