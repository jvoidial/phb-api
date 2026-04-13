#!/usr/bin/env python3
import json

STATE_PATH = "gcs/runtime/mind_unified_state.json"

with open(STATE_PATH,"r",encoding="utf-8") as f:
    data = json.load(f)

states = data["state_grid"]

# fix openness, rigor, creativity at 0.8 and slice curiosity x focus
slice_o = 0.8
slice_r = 0.8
slice_cr = 0.8

def approx(x, target, eps=0.01):
    return abs(x - target) <= eps

grid2d = []
for s in states:
    c = s["coords"]
    if approx(c["openness"], slice_o) and approx(c["rigor"], slice_r) and approx(c["creativity"], slice_cr):
        grid2d.append({
            "curiosity": c["curiosity"],
            "focus": c["focus"],
            "coherence": s["coherence"],
            "knowledge_influence": s["knowledge_influence"],
            "practice_influence": s["practice_influence"]
        })

out = {
  "axes": ["curiosity","focus"],
  "fixed": {"openness": slice_o, "rigor": slice_r, "creativity": slice_cr},
  "points": grid2d
}

with open("gcs/runtime/mind_slice_curiosity_focus.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("Wrote gcs/runtime/mind_slice_curiosity_focus.json")
