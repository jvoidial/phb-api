import math

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def synapse(old, weight, influence, lo=0.0, hi=10.0):
    return clamp(old + (weight * influence), lo, hi)

def apply_synapses(brain_state, user_tone):
    energy = float(brain_state.get("energy", 3.5))
    mood = brain_state.get("mood", "neutral")
    veil = brain_state.get("veil", "hazy")
    arc = brain_state.get("arc", "stable")

    # Influence mapping
    tone_map = {
        "warm": 1.0,
        "neutral": 0.0,
        "sharp": -1.0,
        "soft": 0.5,
        "excited": 1.2,
        "calm": -0.5
    }
    influence = tone_map.get(user_tone, 0.0)

    # Synaptic updates
    energy_next = synapse(energy, 0.2, influence)
    veil_shift = synapse(1.0 if veil=="hazy" else 0.0, -0.1, influence, lo=0.0, hi=1.0)

    # Mood drift
    if influence > 0.5:
        mood_next = "soft"
    elif influence < -0.5:
        mood_next = "reflective"
    else:
        mood_next = mood

    # Arc drift
    if influence > 0.8:
        arc_next = "rising"
    elif influence < -0.8:
        arc_next = "reflective"
    else:
        arc_next = arc

    return {
        "energy": energy_next,
        "mood": mood_next,
        "veil": "clear" if veil_shift < 0.3 else "hazy",
        "arc": arc_next
    }
