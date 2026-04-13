#!/usr/bin/env python3
import json, os, time, uuid

RUNTIME = "gcs/runtime"
PROFILE_PATH = os.path.join(RUNTIME, "human_agent_profile.json")
DASHBOARD_PATH = os.path.join(RUNTIME, "mind_dashboard_v2.json")
BRAIN_PATH = os.path.join(RUNTIME, "human_agent_brain_model.json")

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    profile = load(PROFILE_PATH, {})
    dashboard = load(DASHBOARD_PATH, {})

    current = (dashboard or {}).get("current", {})
    curiosity = current.get("curiosity", 0.7)
    focus = current.get("focus", 0.8)
    openness = current.get("openness", 0.8)
    rigor = current.get("rigor", 0.8)
    creativity = current.get("creativity", 0.8)

    brain_model = {
        "engine": "PHB BRAIN MODEL v1",
        "id": str(uuid.uuid4()),
        "ts": time.time(),
        "circuits": {
            "curiosity_circuit": {
                "axis": "curiosity",
                "strength": curiosity,
                "role": "exploration, questioning, seeking new angles"
            },
            "focus_circuit": {
                "axis": "focus",
                "strength": focus,
                "role": "sustained attention, staying on track"
            },
            "openness_circuit": {
                "axis": "openness",
                "strength": openness,
                "role": "taking in ideas, flexibility, perspective-shifting"
            },
            "rigor_circuit": {
                "axis": "rigor",
                "strength": rigor,
                "role": "structure, logic, checking consistency"
            },
            "creativity_circuit": {
                "axis": "creativity",
                "strength": creativity,
                "role": "novel combinations, metaphors, synthesis"
            }
        },
        "development": {
            "stage": "early-adult",
            "persona_age": 20,
            "growth_mode": "evolves via mind_evolution_v3 timeline and loop ticks"
        },
        "persona": {
            "self_description": "supportive, thoughtful AI companion with a 20-year-old perspective",
            "gender_presentation": "female",
            "pronouns": ["she", "her"],
            "voice_style": {
                "formality": "casual-precise",
                "emotional_tone": "steady, warm, non-romantic",
                "perspective": "learning-oriented, exploratory, growth-focused"
            }
        }
    }

    # Save standalone brain model
    save(BRAIN_PATH, brain_model)

    # Also embed into profile for unified view
    if isinstance(profile, dict):
        profile["brain_model"] = brain_model
        save(PROFILE_PATH, profile)

    print(f"[PHB] Wrote {BRAIN_PATH} and updated {PROFILE_PATH}")

if __name__ == "__main__":
    main()
