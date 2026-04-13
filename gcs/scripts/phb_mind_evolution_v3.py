#!/usr/bin/env python3
import json, os, math, random

RUNTIME = "gcs/runtime"
STATE_PATH = os.path.join(RUNTIME, "mind_unified_state.json")
CURRENT_PATH = os.path.join(RUNTIME, "current_state.json")
AGENTS_PATH = os.path.join(RUNTIME, "agents_config.json")
OUT_PATH = os.path.join(RUNTIME, "mind_evolution_v3.json")

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clamp(x): return max(0.0, min(1.0, x))

def dist(a, b, axes):
    s = 0.0
    for k in axes:
        d = a[k] - b[k]
        s += d*d
    return math.sqrt(s / len(axes))

def step_toward(coords, target, axes, strength):
    out = {}
    for k in axes:
        out[k] = clamp(coords[k] + strength * (target[k] - coords[k]))
    return out

def add_noise(coords, axes, scale):
    out = {}
    for k in axes:
        out[k] = clamp(coords[k] + random.uniform(-scale, scale))
    return out

def nearest_state(states, coords, axes):
    return min(states, key=lambda s: dist(s["coords"], coords, axes))

def evolve_single(current, target, axes, states, steps=20, base_strength=0.15, noise_scale=0.03):
    timeline = []
    coords = current.copy()
    for t in range(steps):
        nearest = nearest_state(states, coords, axes)
        Ik = nearest["knowledge_influence"]
        Ip = nearest["practice_influence"]
        strength = base_strength * (0.5 * Ik + 0.5 * Ip)
        coords = step_toward(coords, target, axes, strength)
        coords = add_noise(coords, axes, noise_scale * (1.0 - Ik))
        d = dist(coords, target, axes)
        coherence = 1.0 - d  # symbolic coherence proxy
        energy = {
            "stability": clamp(1.0 - noise_scale),
            "volatility": noise_scale
        }
        timeline.append({
            "t": t,
            "coords": {k: round(coords[k], 3) for k in axes},
            "dist_to_target": round(d, 3),
            "coherence": round(coherence, 3),
            "energy": energy
        })
    return coords, timeline

def main():
    state = load(STATE_PATH)
    axes = state["axes"]
    target = state["target_state"]
    states = state["state_grid"]
    current = load(CURRENT_PATH)["coords"]

    end_coords, timeline = evolve_single(current, target, axes, states)

    out = {
        "engine": "PHB MIND EVOLUTION v3",
        "axes": axes,
        "target": target,
        "start": current,
        "end": end_coords,
        "timeline": timeline
    }

    # optional multi-agent hook
    if os.path.exists(AGENTS_PATH):
        agents_cfg = load(AGENTS_PATH)["agents"]
        evolved_agents = []
        for ag in agents_cfg:
            ag_start = ag["coords"]
            ag_end, ag_timeline = evolve_single(ag_start, target, axes, states, steps=10)
            evolved_agents.append({
                "id": ag["id"],
                "label": ag.get("label"),
                "start": ag_start,
                "end": ag_end,
                "timeline": ag_timeline
            })
        out["agents"] = evolved_agents

    save(OUT_PATH, out)
    print(f"[PHB] Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
