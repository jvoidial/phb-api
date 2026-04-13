#!/usr/bin/env python3
import json

with open("gcs/runtime/mind_state_coherence.json","r",encoding="utf-8") as f:
    data = json.load(f)

states = data["state_grid"]
states_sorted = sorted(states, key=lambda s: s["coherence"], reverse=True)

print("Top 20 mind states:")
for s in states_sorted[:20]:
    c = s["coords"]
    print(
        f"coh={s['coherence']:.3f} | "
        f"C={c['curiosity']:.2f} F={c['focus']:.2f} "
        f"O={c['openness']:.2f} R={c['rigor']:.2f} Cr={c['creativity']:.2f} "
        f"node_inf={s['node_influence']:.3f}"
    )
