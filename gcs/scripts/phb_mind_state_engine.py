#!/usr/bin/env python3
# PHB Mind State Engine – symbolic model of knowledge/mental modes.
# Not neuroscience, not psychology. A structured metaphor engine.

import os, json, math, time
from datetime import datetime, timezone
from glob import glob

RUNTIME_DIR = "gcs/runtime"
NODE_DIR = "gcs/data/mind_nodes"
os.makedirs(RUNTIME_DIR, exist_ok=True)
os.makedirs(NODE_DIR, exist_ok=True)

AXES = ["curiosity", "focus", "openness", "rigor", "creativity"]
STEP = 0.2   # grid resolution per axis
TICK_SECONDS = 60
INFLUENCE_LAMBDA = 0.6  # falloff in state-space distance

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def load_nodes():
    nodes = []
    for path in glob(os.path.join(NODE_DIR, "*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                node = json.load(f)
                if "coords" in node and "coherence" in node:
                    nodes.append(node)
        except Exception:
            continue
    return nodes

def build_state_grid():
    grid = []
    vals = [round(i * STEP, 2) for i in range(int(1/STEP)+1)]
    for c in vals:
        for f in vals:
            for o in vals:
                for r in vals:
                    for cr in vals:
                        grid.append({
                            "coords": {
                                "curiosity": c,
                                "focus": f,
                                "openness": o,
                                "rigor": r,
                                "creativity": cr
                            },
                            "coherence": 0.0,
                            "node_influence": 0.0
                        })
    return grid

def dist_state(a, b):
    s = 0.0
    for k in AXES:
        d = a[k] - b[k]
        s += d*d
    return math.sqrt(s / len(AXES))

def apply_node_influence(grid, nodes):
    for v in grid:
        vcoords = v["coords"]
        total = 0.0
        for n in nodes:
            ncoords = n["coords"]
            Cg = n["coherence"].get("global_index", 0.7)
            d = dist_state(vcoords, ncoords)
            I = Cg * math.exp(-d / INFLUENCE_LAMBDA)
            total += I
        v["node_influence"] = clamp(total)
    return grid

def compute_coherence(grid):
    for v in grid:
        base = 0.5
        I = v["node_influence"]
        coh = base + 0.4 * I
        v["coherence"] = round(clamp(coh), 3)
    return grid

def main():
    print("[PHB] Mind State Engine – starting...")
    while True:
        now = datetime.now(timezone.utc).isoformat()
        nodes = load_nodes()
        grid = build_state_grid()
        grid = apply_node_influence(grid, nodes)
        grid = compute_coherence(grid)

        packet = {
            "engine": "PHB Mind State Engine",
            "timestamp": now,
            "axes": AXES,
            "node_count": len(nodes),
            "state_grid": grid,
            "note": "Symbolic mind-state model for knowledge/learning. Not neuroscience."
        }

        out_path = os.path.join(RUNTIME_DIR, "mind_state_coherence.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=2)

        print(f"[PHB] Updated mind_state_coherence.json at {now} with {len(grid)} states and {len(nodes)} nodes.")
        time.sleep(TICK_SECONDS)

if __name__ == "__main__":
    main()
