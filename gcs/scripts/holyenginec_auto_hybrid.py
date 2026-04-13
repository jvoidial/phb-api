#!/usr/bin/env python3
import numpy as np
import os
import time
import requests

# ================================
# HOLYENGINE-C – NGROK-ONLY HYBRID
# AI-ADAPTIVE GLOBAL PHB
# ================================

GRID_SIZE = 128
TIME_STEPS = 500
DT = 0.01
K_RESONANCE = 3.14
NOISE_LEVEL = 0.08
FEEDBACK_GAIN = 0.15  # reduced for stability

STATE_FILE = os.path.expanduser("~/gcs/data/phb_global_state.npy")
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

# --- NGROK CONFIG ---
NGROK_ENDPOINT = "http://127.0.0.1:4040/api/tunnels"

# --- BUGASPGERE FIELD ---
def init_bugaspgere_field(n):
    x = np.linspace(-1, 1, n)
    y = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    phi = np.sin(K_RESONANCE * R) / (R + 1e-6)
    phi += NOISE_LEVEL * np.random.randn(n, n)
    return phi

# --- VEIL OBSERVATION ---
def veil_observation(phi):
    return np.tanh(phi)

# --- AI FEEDBACK ---
def adaptive_feedback(phi, psi):
    energy = np.mean(phi**2)
    return FEEDBACK_GAIN * (1 + 0.2 * (energy - 0.5))

# --- CAT EOF ---
def cat_eof_feedback(phi, psi, gain):
    return phi + gain * (phi * psi)

# --- EVOLVE FUNCTION ---
def evolve_bugaspgere(phi):
    laplacian = (
        -4*phi
        + np.roll(phi, 1, axis=0)
        + np.roll(phi, -1, axis=0)
        + np.roll(phi, 1, axis=1)
        + np.roll(phi, -1, axis=1)
    )
    phi_new = phi + DT * (K_RESONANCE**2 * phi + laplacian)
    return np.clip(phi_new, -10, 10)  # prevent overflow

# --- GLOBAL PHB STATE LOAD/WRITE ---
def load_global_phi():
    try:
        tunnels = requests.get(NGROK_ENDPOINT, timeout=2).json()
        public_url = tunnels["tunnels"][0]["public_url"]
        r = requests.get(f"{public_url}/phb_global_state.npy", timeout=2)
        with open(STATE_FILE, "wb") as f: f.write(r.content)
        return np.load(STATE_FILE)
    except:
        return np.load(STATE_FILE) if os.path.exists(STATE_FILE) else init_bugaspgere_field(GRID_SIZE)

def save_global_phi(phi):
    np.save(STATE_FILE, phi)
    try:
        tunnels = requests.get(NGROK_ENDPOINT, timeout=2).json()
        public_url = tunnels["tunnels"][0]["public_url"]
        requests.post(f"{public_url}/phb_global_state.npy", files={'file': open(STATE_FILE, 'rb')}, timeout=2)
    except: pass

# --- MAIN LOOP ---
def run_holyenginec_auto():
    phi = load_global_phi()
    while True:
        for _ in range(TIME_STEPS):
            phi = evolve_bugaspgere(phi)
            psi = veil_observation(phi)
            gain = adaptive_feedback(phi, psi)
            phi = cat_eof_feedback(phi, psi, gain)
        save_global_phi(phi)
        time.sleep(0.1)

if __name__ == "__main__":
    run_holyenginec_auto()
