#!/usr/bin/env python3
import json, os

RUNTIME = "gcs/runtime"
DASH_PATH = os.path.join(RUNTIME, "mind_dashboard_v2.json")
OUT_PATH = os.path.join(RUNTIME, "human_agent_profile.json")

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def level(x):
    if x < 0.4: return "low"
    if x < 0.7: return "medium"
    return "high"

def main():
    dash = load(DASH_PATH)
    cur = dash["current"]
    target = dash["target"]
    evo = dash.get("evolution_v3", {})

    # MIND: cognitive style
    mind_profile = {
        "curiosity_level": level(cur["curiosity"]),
        "focus_level": level(cur["focus"]),
        "openness_level": level(cur["openness"]),
        "rigor_level": level(cur["rigor"]),
        "creativity_level": level(cur["creativity"]),
        "reasoning_style": "structured-creative" if cur["rigor"] >= 0.7 and cur["creativity"] >= 0.7 else
                           "exploratory" if cur["curiosity"] >= 0.7 else
                           "balanced",
        "exploration_bias": round(cur["curiosity"] - cur["focus"], 3),
        "novelty_bias": round(cur["creativity"] - cur["rigor"], 3)
    }

    # BODY: tempo / energy (symbolic)
    coherence_last = evo.get("coherence_last", None)
    dist_last = evo.get("dist_last", None)
    body_profile = {
        "tempo": "calm-focused" if coherence_last and coherence_last > 0.9 else
                 "warming-up" if coherence_last and coherence_last > 0.7 else
                 "scattered",
        "stability": "high" if coherence_last and coherence_last > 0.9 else
                     "medium" if coherence_last and coherence_last > 0.7 else
                     "low",
        "distance_to_target": dist_last,
        "activation_state": "near-target" if dist_last is not None and dist_last < 0.05 else
                            "en-route" if dist_last is not None and dist_last < 0.15 else
                            "far"
    }

    # SOUL: intention / orientation (symbolic)
    soul_profile = {
        "orientation": "growth-directed",
        "target_signature": {
            "curiosity": target["curiosity"],
            "focus": target["focus"],
            "openness": target["openness"],
            "rigor": target["rigor"],
            "creativity": target["creativity"]
        },
        "core_tendencies": [
            "seek understanding" if cur["curiosity"] >= 0.6 else "maintain stability",
            "integrate ideas" if cur["openness"] >= 0.6 and cur["creativity"] >= 0.6 else "refine known patterns",
            "aim for clarity" if cur["focus"] >= 0.6 else "explore possibilities"
        ]
    }

    out = {
        "engine": "PHB HUMAN AGENT PROFILE",
        "mind": mind_profile,
        "body": body_profile,
        "soul": soul_profile
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"[PHB] Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
