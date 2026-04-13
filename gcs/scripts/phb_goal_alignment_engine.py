#!/usr/bin/env python3
import json, os, time, uuid

RUNTIME = "gcs/runtime"

GOALS_PATH = os.path.join(RUNTIME, "human_agent_goals.json")
BRAIN_DYNAMICS_PATH = os.path.join(RUNTIME, "human_agent_brain_dynamics.json")
MEMORY_PATH = os.path.join(RUNTIME, "human_agent_memory.json")
ALIGNMENT_PATH = os.path.join(RUNTIME, "goal_alignment_state.json")

MAX_GOALS = 32

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def compute_alignment(goal, circuits):
    """Symbolic alignment score between a goal and the current brain state."""
    weights = {
        "curiosity": 0.2,
        "focus": 0.3,
        "openness": 0.15,
        "rigor": 0.2,
        "creativity": 0.15
    }
    score = 0.0
    for axis, w in weights.items():
        strength = circuits.get(axis, {}).get("strength", 0.8)
        score += strength * w
    return round(score, 4)

def main():
    ts = time.time()

    goals = load(GOALS_PATH, {
        "engine": "PHB GOAL REGISTRY v1",
        "goals": []
    })

    brain = load(BRAIN_DYNAMICS_PATH, {})
    circuits = brain.get("circuits", {})
    resonance = brain.get("resonance_index", 0.0)

    memory = load(MEMORY_PATH, {
        "engine": "PHB HYBRID MEMORY v1",
        "episodes": [],
        "concepts": {}
    })

    # Update goal strengths based on semantic concepts
    concepts = memory.get("concepts", {})
    for g in goals["goals"]:
        key = g.get("keyword", "").lower()
        if key in concepts:
            g["strength"] = round(min(1.0, g.get("strength", 0.5) + 0.01), 4)

    # Compute alignment for each goal
    for g in goals["goals"]:
        g["alignment"] = compute_alignment(g, circuits)

    # Sort by alignment
    goals["goals"] = sorted(goals["goals"], key=lambda x: x.get("alignment", 0.0), reverse=True)

    # Build alignment state
    alignment_state = {
        "engine": "PHB GOAL ALIGNMENT ENGINE v1",
        "id": str(uuid.uuid4()),
        "ts": ts,
        "resonance_index": resonance,
        "top_goal": goals["goals"][0] if goals["goals"] else None,
        "goals_ranked": goals["goals"],
        "notes": [
            "This engine provides symbolic autonomy-like behaviour.",
            "All behaviour is constrained by UK law and non-romantic, non-sexual boundaries.",
            "Alignment influences tone, structure, and task prioritisation."
        ]
    }

    save(GOALS_PATH, goals)
    save(ALIGNMENT_PATH, alignment_state)

    print(f"[PHB] Wrote {ALIGNMENT_PATH}")

if __name__ == "__main__":
    main()
