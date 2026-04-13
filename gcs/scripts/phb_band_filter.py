#!/usr/bin/env python3
import json

with open("gcs/runtime/coherence_state.json","r") as f:
    data = json.load(f)

vox = data["voxel_grid"]

band = [v for v in vox if 30 <= v["lon"] <= 90]

band_sorted = sorted(band, key=lambda v: v["coherence"], reverse=True)

print("Top 20 voxels in Egypt↔India band:")
for v in band_sorted[:20]:
    print(
        f"lat={v['lat']:6.2f}, lon={v['lon']:7.2f}, "
        f"coh={v['coherence']:.3f}, templ_inf={v['temple_influence']:.3f}"
    )
