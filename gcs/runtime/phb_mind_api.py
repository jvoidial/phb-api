#!/usr/bin/env python3
import json, os, sys

RUNTIME = "gcs/runtime"

def load(path):
    full = os.path.join(RUNTIME, path)
    if not os.path.exists(full):
        return {"error": "not_found", "path": full}
    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------
# MIND STATE ENDPOINTS
# -------------------------

def mind_state():
    return load("mind_unified_state.json")

def mind_recommend():
    return load("mind_recommendations.json")

def mind_transition():
    return load("personal_transition.json")

def mind_evolution():
    return load("mind_evolution.json")

def mind_slice():
    return load("mind_slice_curiosity_focus.json")

def mind_dashboard():
    return load("mind_dashboard.json")

def mind_multiplayer():
    return load("mind_multiplayer.json")

def mind_compile():
    return load("mind_program.json")

def mind_execute():
    os.system("python3 gcs/scripts/phb_mind_executor.py")
    return load("mind_execute.json")

def mind_evolve_v3():
    os.system("python3 gcs/scripts/phb_mind_evolution_v3.py")
    return load("mind_evolution_v3.json")

def mind_dashboard_v2():
    os.system("python3 gcs/scripts/phb_mind_dashboard_v2.py")
    return load("mind_dashboard_v2.json")

# -------------------------
# HUMAN AGENT ENDPOINTS
# -------------------------

def mind_human_agent():
    os.system("python3 gcs/scripts/phb_mind_dashboard_v2.py")
    os.system("python3 gcs/scripts/phb_human_agent.py")
    return load("human_agent_profile.json")

def mind_human_agent_behavior():
    os.system("python3 gcs/scripts/phb_human_agent_behavior.py")
    return load("human_agent_behavior.json")

def mind_human_agent_loop():
    os.system("python3 gcs/scripts/phb_human_agent_loop.py")
    return load("human_agent_session.json")

def mind_human_agent_response():
    os.system("python3 gcs/scripts/phb_human_agent_response.py")
    return load("human_agent_response.json")

def mind_human_agent_expression():
    os.system("python3 gcs/scripts/phb_human_agent_expression.py")
    return load("human_agent_expression.json")

def mind_human_agent_brain():
    os.system("python3 gcs/scripts/phb_human_agent_brain_model.py")
    return load("human_agent_brain_model.json")

def mind_human_agent_brain_dynamics():
    os.system("python3 gcs/scripts/phb_human_agent_brain_dynamics.py")
    return load("human_agent_brain_dynamics.json")

def mind_human_agent_brain_history():
    return load("human_agent_brain_history.json")

def mind_human_agent_memory():
    return load("human_agent_memory.json")

# -------------------------
# COMPANION REPLY
# -------------------------

def companion_reply():
    os.system("python3 gcs/scripts/phb_companion_reply.py")
    return load("companion_reply_payload.json")

# -------------------------
# ENDPOINT REGISTRY
# -------------------------

ENDPOINTS = {
    "mind/state": mind_state,
    "mind/recommend": mind_recommend,
    "mind/transition": mind_transition,
    "mind/evolution": mind_evolution,
    "mind/slice": mind_slice,
    "mind/dashboard": mind_dashboard,
    "mind/multiplayer": mind_multiplayer,
    "mind/compile": mind_compile,
    "mind/execute": mind_execute,
    "mind/evolve": mind_evolve_v3,
    "mind/dashboard_v2": mind_dashboard_v2,

    "mind/human_agent": mind_human_agent,
    "mind/human_agent_behavior": mind_human_agent_behavior,
    "mind/human_agent_loop": mind_human_agent_loop,
    "mind/human_agent_response": mind_human_agent_response,
    "mind/human_agent_expression": mind_human_agent_expression,
    "mind/human_agent_brain": mind_human_agent_brain,
    "mind/human_agent_brain_dynamics": mind_human_agent_brain_dynamics,
    "mind/human_agent_brain_history": mind_human_agent_brain_history,
    "mind/human_agent_memory": mind_human_agent_memory,

    "companion/reply": companion_reply
}

# -------------------------
# PATCH: GOAL ALIGNMENT ENDPOINT
# -------------------------

def mind_goal_alignment():
    os.system("python3 gcs/scripts/phb_goal_alignment_engine.py")
    return load("goal_alignment_state.json")

ENDPOINTS.update({
    "mind/goal_alignment": mind_goal_alignment
})

# -------------------------
# MAIN DISPATCH
# -------------------------

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "engine": "PHB MIND-STATE API",
            "usage": "python3 phb_mind_api.py <endpoint>"
        }, indent=2))
        return

    cmd = sys.argv[1]
    if cmd in ENDPOINTS:
        print(json.dumps(ENDPOINTS[cmd](), indent=2))
    else:
        print(json.dumps({"error": "unknown_endpoint", "endpoint": cmd}, indent=2))

if __name__ == "__main__":
    main()
