#!/usr/bin/env python3
# PHB GodCode Vortex – Runtime Coherence Simulation Engine
# Symbolic only. No real-world prediction or physical claim.

import os
import json
import math
import time
from datetime import datetime, timezone
from glob import glob

# -----------------------------
# CONFIG
# -----------------------------
VOXEL_LAT_STEP = 5.0    # degrees
VOXEL_LON_STEP = 5.0    # degrees
INFLUENCE_LAMBDA_KM = 800.0  # falloff scale
TICK_SECONDS = 60       # update interval

DATA_TEMPLE_DIR = "gcs/data/temples"
RUNTIME_DIR = "gcs/runtime"

os.makedirs(DATA_TEMPLE_DIR, exist_ok=True)
os.makedirs(RUNTIME_DIR, exist_ok=True)

# -----------------------------
# UTILITIES
# -----------------------------
def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def haversine_km(lat1, lon1, lat2, lon2):
    # approximate Earth distance
    R = 6371.0
    from math import radians, sin, cos, asin, sqrt
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# -----------------------------
# ENVIRONMENT (SYMBOLIC)
# -----------------------------
def load_environment_state():
    # You can later wire this to real APIs or your own engine.
    # For now: symbolic, slowly varying environment.
    now = datetime.now(timezone.utc)
    t = now.timestamp()

    # simple periodic variations
    humidity = 0.6 + 0.2 * math.sin(t / 3600.0)
    pressure = 1008 + 5 * math.sin(t / 7200.0)
    wind_speed = 10 + 5 * math.sin(t / 5400.0)

    env = {
        "timestamp": now.isoformat(),
        "temperature_c": 12.0,
        "humidity": clamp(humidity),
        "wind_speed_mph": clamp(wind_speed, 0, 40),
        "wind_direction": "SW",
        "rain_mm": 0.5,
        "going": "Good to Soft",
        "atmospheric_pressure": pressure
    }
    return env

def environment_modifiers(env):
    pressure_factor = clamp((env["atmospheric_pressure"] - 995) / 25.0)
    rain_factor = clamp(env["rain_mm"] / 5.0)
    wind_factor = clamp(env["wind_speed_mph"] / 30.0)

    return {
        "stamina_bonus": 0.05 * rain_factor,
        "coherence_penalty": 0.04 * wind_factor,
        "volatility_bonus": 0.06 * wind_factor,
        "pressure_instability": 0.05 * (1 - pressure_factor)
    }

# -----------------------------
# TEMPLE NODES
# -----------------------------
def load_temple_nodes():
    nodes = []
    for path in glob(os.path.join(DATA_TEMPLE_DIR, "*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                node = json.load(f)
                if "coords" in node and "coherence" in node:
                    nodes.append(node)
        except Exception:
            continue
    return nodes

# Example template for a temple JSON:
# {
#   "id": "temple_karnak_egypt",
#   "type": "PHB_TEMPLE_NODE",
#   "meta": { "name": "Karnak Temple", "culture": "Egyptian" },
#   "coords": { "lat": 25.7188, "lon": 32.6573, "elev_m": 80 },
#   "coherence": {
#       "geo": 0.8,
#       "orient": 0.7,
#       "material": 0.6,
#       "acoustic": 0.75,
#       "global_index": 0.71
#   }
# }

# -----------------------------
# VOXEL GRID
# -----------------------------
def build_global_voxel_grid():
    voxels = []
    lat = -90.0
    while lat <= 90.0:
        lon = -180.0
        while lon <= 180.0:
            voxels.append({
                "lat": round(lat, 3),
                "lon": round(lon, 3),
                "coherence": 0.0,
                "temple_influence": 0.0,
                "environment_factor": 0.0
            })
            lon += VOXEL_LON_STEP
        lat += VOXEL_LAT_STEP
    return voxels

# -----------------------------
# TEMPLE INFLUENCE FIELD
# -----------------------------
def apply_temple_influence(grid, temples):
    for v in grid:
        lat_v = v["lat"]
        lon_v = v["lon"]
        total_inf = 0.0
        for temple in temples:
            c = temple.get("coherence", {})
            Cg = c.get("global_index", 0.6)
            coords = temple.get("coords", {})
            lat_t = coords.get("lat")
            lon_t = coords.get("lon")
            if lat_t is None or lon_t is None:
                continue
            d_km = haversine_km(lat_v, lon_v, lat_t, lon_t)
            I = Cg * math.exp(-d_km / INFLUENCE_LAMBDA_KM)
            total_inf += I
        v["temple_influence"] = clamp(total_inf)
    return grid

# -----------------------------
# ENVIRONMENT MODULATION
# -----------------------------
def apply_environment_modulation(grid, env_mod):
    for v in grid:
        # simple symbolic mapping: environment factor is a blend of modifiers
        ef = (
            0.4 * env_mod["stamina_bonus"] -
            0.3 * env_mod["coherence_penalty"] +
            0.3 * env_mod["pressure_instability"]
        )
        v["environment_factor"] = round(clamp(0.5 + ef), 3)
    return grid

# -----------------------------
# COHERENCE COMPUTATION
# -----------------------------
def compute_global_coherence(grid):
    for v in grid:
        base = 0.5
        t_inf = v["temple_influence"]
        env_f = v["environment_factor"]
        coh = base + 0.4 * t_inf + 0.2 * (env_f - 0.5)
        v["coherence"] = round(clamp(coh), 3)
    return grid

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    print("[PHB] Runtime Coherence Engine – starting...")
    while True:
        now = datetime.now(timezone.utc).isoformat()
        temples = load_temple_nodes()
        env = load_environment_state()
        env_mod = environment_modifiers(env)

        grid = build_global_voxel_grid()
        grid = apply_temple_influence(grid, temples)
        grid = apply_environment_modulation(grid, env_mod)
        grid = compute_global_coherence(grid)

        packet = {
            "engine": "PHB GodCode Vortex – Runtime Coherence Engine",
            "timestamp": now,
            "environment": env,
            "environment_modifiers": env_mod,
            "temple_count": len(temples),
            "voxel_grid": grid,
            "note": "Symbolic simulation only. No real-world prediction or physical claim."
        }

        out_path = os.path.join(RUNTIME_DIR, "coherence_state.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=2)

        print(f"[PHB] Updated coherence_state.json at {now} with {len(grid)} voxels and {len(temples)} temples.")
        time.sleep(TICK_SECONDS)

if __name__ == "__main__":
    main()
