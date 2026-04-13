#!/usr/bin/env python3
import json

with open("gcs/runtime/coherence_state.json","r",encoding="utf-8") as f:
    data = json.load(f)

voxels = data["voxel_grid"]
# sort by coherence descending
voxels_sorted = sorted(voxels, key=lambda v: v["coherence"], reverse=True)

print("Top 20 coherence voxels:")
for v in voxels_sorted[:20]:
    print(
        f"lat={v['lat']:6.2f}, lon={v['lon']:7.2f}, "
        f"coh={v['coherence']:.3f}, "
        f"templ_inf={v['temple_influence']:.3f}, env={v['environment_factor']:.3f}"
    )
