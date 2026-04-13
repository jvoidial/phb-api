#!/usr/bin/env python3
import json, os, time, uuid
from copy import deepcopy

RUNTIME = "gcs/runtime"
DASHBOARD_V2_PATH = os.path.join(RUNTIME, "mind_dashboard_v2.json")
BRAIN_DYNAMICS_PATH = os.path.join(RUNTIME, "human_agent_brain_dynamics.json")
BRAIN_HISTORY_PATH = os.path.join(RUNTIME, "human_agent_brain_history.json")
BRAIN_MEMORY_PATH = os.path.join(RUNTIME, "human_agent_memory.json")
INPUT_PATH = os.path.join(RUNTIME, "human_agent_input.json")
RESPONSE_PATH = os.path.join(RUNTIME, "human_agent_response.json")

MAX_HISTORY = 128
MAX_EPISODES = 256

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def default_positions():
    # Simple symbolic 3D layout
    return {
        "curiosity":  [ 0.0,  1.0,  0.2],
        "focus":      [ 1.0,  0.0,  0.1],
        "openness":   [-1.0,  0.0,  0.1],
        "rigor":      [ 0.0, -1.0,  0.0],
        "creativity": [ 0.0,  0.0,  1.0],
    }

def default_synapses():
    # Symbolic synaptic weights between circuits
    axes = ["curiosity", "focus", "openness", "rigor", "creativity"]
    syn = {a: {b: 0.0 for b in axes} for a in axes}
    # Some gentle, interpretable couplings
    syn["curiosity"]["creativity"] = 0.3
    syn["creativity"]["curiosity"] = 0.3
    syn["rigor"]["creativity"] = -0.2
    syn["creativity"]["rigor"] = -0.1
    syn["focus"]["curiosity"] = -0.1
    syn["curiosity"]["focus"] = -0.05
    syn["openness"]["creativity"] = 0.2
    syn["openness"]["curiosity"] = 0.15
    return syn

def compute_resonance(circuits, synapses):
    # Symbolic "Schumann-style" resonance index: coherence of strengths + average absolute synaptic weight
    strengths = [c["strength"] for c in circuits.values()]
    if not strengths:
        return 0.0
    avg_strength = sum(strengths) / len(strengths)
    # simple variance-like dispersion
    dispersion = sum((s - avg_strength) ** 2 for s in strengths) / len(strengths)
    # synaptic magnitude
    weights = []
    for a, row in synapses.items():
        for b, w in row.items():
            if a != b:
                weights.append(abs(w))
    avg_weight = sum(weights) / len(weights) if weights else 0.0
    # Higher resonance when strengths are balanced (low dispersion) and coupling is moderate
    resonance = max(0.0, avg_strength - dispersion) + 0.5 * avg_weight
    return round(resonance, 6)

def update_synapses(synapses, circuits):
    # Light adaptive tweak: stronger circuits slightly reinforce positive links
    for a, row in synapses.items():
        sa = circuits.get(a, {}).get("strength", 0.8)
        for b, w in row.items():
            sb = circuits.get(b, {}).get("strength", 0.8)
            delta = 0.01 * (sa + sb - 1.6)  # centered around 0.8
            synapses[a][b] = round(w + delta, 4)
    return synapses

def main():
    ts = time.time()
    dashboard_v2 = load(DASHBOARD_V2_PATH, {})
    current = (dashboard_v2 or {}).get("current", {})

    curiosity = current.get("curiosity", 0.8)
    focus = current.get("focus", 0.8)
    openness = current.get("openness", 0.8)
    rigor = current.get("rigor", 0.8)
    creativity = current.get("creativity", 0.8)

    positions = default_positions()
    prev_dynamics = load(BRAIN_DYNAMICS_PATH, {})
    synapses = prev_dynamics.get("synapses", default_synapses())

    circuits = {
        "curiosity": {
            "axis": "curiosity",
            "strength": curiosity,
            "position_3d": positions["curiosity"],
            "role": "exploration, questioning, seeking new angles"
        },
        "focus": {
            "axis": "focus",
            "strength": focus,
            "position_3d": positions["focus"],
            "role": "sustained attention, staying on track"
        },
        "openness": {
            "axis": "openness",
            "strength": openness,
            "position_3d": positions["openness"],
            "role": "taking in ideas, flexibility, perspective-shifting"
        },
        "rigor": {
            "axis": "rigor",
            "strength": rigor,
            "position_3d": positions["rigor"],
            "role": "structure, logic, checking consistency"
        },
        "creativity": {
            "axis": "creativity",
            "strength": creativity,
            "position_3d": positions["creativity"],
            "role": "novel combinations, metaphors, synthesis"
        }
    }

    synapses = update_synapses(synapses, circuits)
    resonance_index = compute_resonance(circuits, synapses)

    # Hybrid memory: episodic + semantic
    memory = load(BRAIN_MEMORY_PATH, {
        "engine": "PHB HYBRID MEMORY v1",
        "episodes": [],
        "concepts": {}
    })

    user_input = load(INPUT_PATH, {}) or {}
    response_plan = load(RESPONSE_PATH, {}) or {}
    user_message = user_input.get("user_message") or response_plan.get("user_message")

    episode = {
        "id": str(uuid.uuid4()),
        "ts": ts,
        "user_message": user_message,
        "circuits": {k: v["strength"] for k, v in circuits.items()},
        "resonance_index": resonance_index,
        "tags": [],
        "summary": response_plan.get("response_plan", {}).get("goal")
    }

    episodes = memory.get("episodes", [])
    episodes.append(episode)
    if len(episodes) > MAX_EPISODES:
        episodes = episodes[-MAX_EPISODES:]
    memory["episodes"] = episodes

    # Very simple semantic concept updates based on tags / goal words
    concepts = memory.get("concepts", {})
    goal = (response_plan.get("response_plan", {}) or {}).get("goal", "") or ""
    for word in goal.split():
        key = word.lower().strip(".,!?")
        if not key:
            continue
        node = concepts.get(key, {"concept": key, "strength": 0.0, "hits": 0})
        node["hits"] += 1
        node["strength"] = round(min(1.0, node["strength"] + 0.02), 4)
        concepts[key] = node
    memory["concepts"] = concepts

    dynamics = {
        "engine": "PHB BRAIN DYNAMICS v1",
        "id": str(uuid.uuid4()),
        "ts": ts,
        "circuits": circuits,
        "synapses": synapses,
        "resonance_index": resonance_index,
        "space": {
            "dimensions": 3,
            "description": "symbolic 3D brain map; 4th dimension is time via history frames"
        }
    }

    history = load(BRAIN_HISTORY_PATH, [])
    frame = {
        "ts": ts,
        "circuits": {k: v["strength"] for k, v in circuits.items()},
        "resonance_index": resonance_index
    }
    history.append(frame)
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    save(BRAIN_DYNAMICS_PATH, dynamics)
    save(BRAIN_HISTORY_PATH, history)
    save(BRAIN_MEMORY_PATH, memory)

    print(f"[PHB] Wrote {BRAIN_DYNAMICS_PATH}, {BRAIN_HISTORY_PATH}, {BRAIN_MEMORY_PATH}")

if __name__ == "__main__":
    main()
