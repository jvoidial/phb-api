#!/bin/bash

# 1. Remove ANY existing run_intelligence_core definition (broken or partial)
sed -i '/def run_intelligence_core/,/^}/d' phb_intelligence_core_her.py

# 2. Append a clean, correctly-indented unified brain function
cat << 'EOB' >> phb_intelligence_core_her.py

# --- Unified PHB Brain Integration (clean reinsert) ---
from phb_brain import run_phb_brain

def run_intelligence_core(user_message: str, recent_context: dict | None = None):
    brain_result = run_phb_brain(user_message)

    return {
        "perception": brain_result["perception"],
        "context": recent_context or {},
        "plan": brain_result["plan"],
        "reasoning": brain_result["reasoning"],
        "summary": brain_result["summary"],
        "status": "ok",
        "her_mode": {
            "energy": brain_result["brain_state"]["energy"],
            "mood": brain_result["brain_state"]["mood"],
            "veil": brain_result["brain_state"]["veil"],
            "turns": brain_result["brain_state"]["turns"],
        },
        "brain_state": brain_result["brain_state"],
    }
EOB

echo "Indentation fix applied."
