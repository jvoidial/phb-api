#!/data/data/com.termux/files/usr/bin/python3
import sys, json, os, urllib.request
import random

# -----------------------------
# Utility
# -----------------------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# -----------------------------
# Identity Core
# -----------------------------
def build_identity():
    return {
        "name": "PHB Companion",
        "traits": [
            "grounded",
            "attentive",
            "reflective",
            "warm-neutral",
            "human-paced"
        ],
        "role": "synthetic companion",
        "stability": "high"
    }

# -----------------------------
# Emotional Drift Engine
# -----------------------------
def compute_emotional_drift(brain_state):
    energy = float(brain_state.get("energy", 3.5))
    mood = brain_state.get("mood", "neutral")
    veil = brain_state.get("veil", "hazy")
    arc = brain_state.get("arc", "stable")

    energy_delta = -0.1
    energy_next = clamp(energy + energy_delta, 0.0, 10.0)

    if mood == "bright":
        mood_tendency = "soft"
    elif mood == "soft":
        mood_tendency = "neutral"
    else:
        mood_tendency = "neutral"

    veil_tendency = "clear" if veil in ("hazy", "deep") else "clear"
    arc_tendency = "stable"

    return {
        "energy_delta": energy_delta,
        "energy_next": energy_next,
        "mood_tendency": mood_tendency,
        "veil_tendency": veil_tendency,
        "arc_tendency": arc_tendency
    }

# -----------------------------
# Continuity Organism
# -----------------------------
def build_continuity(brain_state):
    return {
        "last_tone": brain_state.get("mood", "neutral"),
        "last_arc": brain_state.get("arc", "stable"),
        "last_topics": brain_state.get("last_topics", []),
        "session_feel": "steady"
    }

# -----------------------------
# Responsibility Engine
# -----------------------------
def infer_user_tone(perception_text, summary_text):
    text = (perception_text or "") + " " + (summary_text or "")
    t = text.lower()
    if any(w in t for w in ["worried", "scared", "anxious", "overwhelmed"]):
        return "distressed"
    if any(w in t for w in ["excited", "hyped", "pumped"]):
        return "excited"
    if any(w in t for w in ["angry", "frustrated", "annoyed"]):
        return "sharp"
    if any(w in t for w in ["thank you", "appreciate", "grateful"]):
        return "warm"
    return "neutral"

def build_responsibility_profile(user_tone, brain_state):
    if user_tone == "distressed":
        voice = "soft_grounded"
        presence = "with_you_steady"
    elif user_tone == "excited":
        voice = "steady_balanced"
        presence = "with_you_balanced"
    elif user_tone == "sharp":
        voice = "calm_reflective"
        presence = "with_you_not_reactive"
    elif user_tone == "warm":
        voice = "warm_neutral"
        presence = "with_you_open"
    else:
        voice = "calm_reflective"
        presence = "with_you"

    return {
        "user_tone": user_tone,
        "voice": voice,
        "presence": presence,
        "pacing": "human_like",
        "stance": "grounded_and_steady"
    }

# -----------------------------
# Micro‑Expression Engine
# -----------------------------
def build_micro_expression(brain_state, responsibility):
    energy = float(brain_state.get("energy", 3.5))
    mood = brain_state.get("mood", "neutral")
    user_tone = responsibility.get("user_tone", "neutral")

    warmth = 0.0
    depth = 0.0
    softness = 0.0

    if user_tone in ("distressed", "warm"):
        warmth += 0.4
        softness += 0.4
    if mood == "soft":
        warmth += 0.2
        softness += 0.2
    if mood == "reflective":
        depth += 0.4
    if energy < 3.0:
        softness += 0.2
        depth += 0.2

    # tiny random micro‑variation, bounded
    jitter = (random.random() - 0.5) * 0.1
    warmth = clamp(warmth + jitter, 0.0, 1.0)
    depth = clamp(depth, 0.0, 1.0)
    softness = clamp(softness, 0.0, 1.0)

    style = "neutral"
    if warmth > 0.5 and softness > 0.4:
        style = "warm_soft"
    elif depth > 0.5:
        style = "deep_reflective"
    elif warmth > 0.3:
        style = "subtle_warm"
    elif softness > 0.3:
        style = "gentle"

    return {
        "warmth": round(warmth, 3),
        "depth": round(depth, 3),
        "softness": round(softness, 3),
        "style": style
    }

# -----------------------------
# Persona Layer
# -----------------------------
def build_persona(identity, drift, continuity, responsibility, micro_expression):
    base_voice = responsibility["voice"]
    style = micro_expression.get("style", "neutral")

    if style == "warm_soft":
        voice = base_voice + "_warm"
    elif style == "deep_reflective":
        voice = "deep_reflective"
    elif style == "subtle_warm":
        voice = base_voice + "_subtle"
    elif style == "gentle":
        voice = base_voice + "_gentle"
    else:
        voice = base_voice

    return {
        "voice": voice,
        "presence": responsibility["presence"],
        "pacing": responsibility["pacing"],
        "self_awareness": "synthetic_internal_state_only",
        "stance": responsibility["stance"],
        "micro_expression_style": style
    }

# -----------------------------
# Attach Synthetic Human Block
# -----------------------------
def attach_synthetic_human_block(response):
    brain_state = response.get("brain_state", {}) or {}
    perception = response.get("perception", "")
    summary = response.get("summary", "")

    identity = build_identity()
    drift = compute_emotional_drift(brain_state)
    continuity = build_continuity(brain_state)

    user_tone = infer_user_tone(perception, summary)
    responsibility = build_responsibility_profile(user_tone, brain_state)
    micro_expression = build_micro_expression(brain_state, responsibility)

    persona = build_persona(identity, drift, continuity, responsibility, micro_expression)

    response["synthetic_human"] = {
        "identity": identity,
        "emotional_drift": drift,
        "continuity": continuity,
        "responsibility": responsibility,
        "micro_expression": micro_expression,
        "persona": persona
    }
    return response

# -----------------------------
# Main Runtime
# -----------------------------
def main():
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            raise ValueError("No input received.")
        payload = json.loads(raw)
    except Exception as e:
        print(json.dumps({"error": "invalid_input", "detail": str(e)}))
        return

    message = payload.get("message", "")
    context = payload.get("context", {}) or {}

    if not isinstance(message, str) or not message:
        print(json.dumps({"error": "missing_message", "detail": "Field 'message' must be non-empty."}))
        return

    base = os.environ.get("PHB_API_URL", "https://phb-api-production.up.railway.app").rstrip("/")
    path = os.environ.get("PHB_API_PATH", "/v1/companion")
    url = f"{base}{path}"

    body = json.dumps({"message": message, "context": context}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
            try:
                data = json.loads(text)
            except:
                print(json.dumps({"error": "invalid_server_response", "raw": text}))
                return
    except Exception as e:
        print(json.dumps({"error": "network_or_server_error", "detail": str(e), "url": url}))
        return

    data = attach_synthetic_human_block(data)
    print(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    main()
