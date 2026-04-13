#!/usr/bin/env python3
# PHB Unified Mind-State Engine
# Symbolic model of knowledge/practice mind-modes. Not neuroscience.

import os, json, math, time
from datetime import datetime, timezone
from glob import glob

RUNTIME_DIR = "gcs/runtime"
KNOW_NODE_DIR = "gcs/data/mind_nodes"
PRACT_NODE_DIR = "gcs/data/practice_nodes"
os.makedirs(RUNTIME_DIR, exist_ok=True)
os.makedirs(KNOW_NODE_DIR, exist_ok=True)
os.makedirs(PRACT_NODE_DIR, exist_ok=True)

AXES = ["curiosity", "focus", "openness", "rigor", "creativity"]
STEP = 0.2
TICK_SECONDS = 60
INFLUENCE_LAMBDA = 0.6

TARGET_STATE = {
    "curiosity": 0.9,
    "focus": 0.85,
    "openness": 0.85,
    "rigor": 0.85,
    "creativity": 0.9
}

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def load_nodes(dirpath):
    nodes = []
    for path in glob(os.path.join(dirpath, "*.json")):
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
                            "knowledge_influence": 0.0,
                            "practice_influence": 0.0,
                            "goal_distance": 0.0
                        })
    return grid

def dist_state(a, b):
    s = 0.0
    for k in AXES:
        d = a[k] - b[k]
        s += d*d
    return math.sqrt(s / len(AXES))

def apply_influence(grid, nodes, key):
    for v in grid:
        vcoords = v["coords"]
        total = 0.0
        for n in nodes:
            ncoords = n["coords"]
            Cg = n["coherence"].get("global_index", 0.7)
            d = dist_state(vcoords, ncoords)
            I = Cg * math.exp(-d / INFLUENCE_LAMBDA)
            total += I
        v[key] = clamp(total)
    return grid

def compute_coherence(grid):
    for v in grid:
        base = 0.5
        Ik = v["knowledge_influence"]
        Ip = v["practice_influence"]
        coh = base + 0.3 * Ik + 0.2 * Ip
        v["coherence"] = round(clamp(coh), 3)
    return grid

def compute_goal_distance(grid):
    for v in grid:
        d = dist_state(v["coords"], TARGET_STATE)
        v["goal_distance"] = round(d, 3)
    return grid

def main():
    print("[PHB] Unified Mind-State Engine – starting...")
    while True:
        now = datetime.now(timezone.utc).isoformat()
        know_nodes = load_nodes(KNOW_NODE_DIR)
        pract_nodes = load_nodes(PRACT_NODE_DIR)

        grid = build_state_grid()
        grid = apply_influence(grid, know_nodes, "knowledge_influence")
        grid = apply_influence(grid, pract_nodes, "practice_influence")
        grid = compute_coherence(grid)
        grid = compute_goal_distance(grid)

        packet = {
            "engine": "PHB Unified Mind-State Engine",
            "timestamp": now,
            "axes": AXES,
            "target_state": TARGET_STATE,
            "knowledge_node_count": len(know_nodes),
            "practice_node_count": len(pract_nodes),
            "state_grid": grid,
            "note": "Symbolic mind-state model for knowledge/learning. Not neuroscience."
        }

        out_path = os.path.join(RUNTIME_DIR, "mind_unified_state.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=2)

        print(f"[PHB] Updated mind_unified_state.json at {now} with {len(grid)} states, "
              f"{len(know_nodes)} knowledge nodes, {len(pract_nodes)} practice nodes.")
        time.sleep(TICK_SECONDS)

if __name__ == "__main__":
    main()
