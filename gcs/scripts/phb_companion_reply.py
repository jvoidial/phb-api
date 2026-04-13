#!/usr/bin/env python3
import json, os, time, uuid
from copy import deepcopy

RUNTIME = "gcs/runtime"

INPUT_PATH = os.path.join(RUNTIME, "human_agent_input.json")
PROFILE_PATH = os.path.join(RUNTIME, "human_agent_profile.json")
BEHAVIOR_PATH = os.path.join(RUNTIME, "human_agent_behavior.json")
SESSION_PATH = os.path.join(RUNTIME, "human_agent_session.json")
RESPONSE_PATH = os.path.join(RUNTIME, "human_agent_response.json")
EXPRESSION_PATH = os.path.join(RUNTIME, "human_agent_expression.json")
BRAIN_MODEL_PATH = os.path.join(RUNTIME, "human_agent_brain_model.json")
BRAIN_DYNAMICS_PATH = os.path.join(RUNTIME, "human_agent_brain_dynamics.json")
BRAIN_HISTORY_PATH = os.path.join(RUNTIME, "human_agent_brain_history.json")
BRAIN_MEMORY_PATH = os.path.join(RUNTIME, "human_agent_memory.json")

PAYLOAD_PATH = os.path.join(RUNTIME, "companion_reply_payload.json")

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def run(cmd):
    os.system(cmd)

def get_recent_episodes(memory, n=3):
    episodes = (memory or {}).get("episodes", [])
    return episodes[-n:] if len(episodes) > n else episodes

def get_top_concepts(memory, n=8):
    concepts = (memory or {}).get("concepts", {})
    items = sorted(concepts.values(), key=lambda x: x.get("strength", 0.0), reverse=True)
    return items[:n]

def build_llm_prompt(user_message, expression, brain_dyn, episodes, concepts):
    tone = (expression or {}).get("tone", [])
    language = (expression or {}).get("language", {})
    core_tendencies = (expression or {}).get("core_tendencies", [])
    role = (expression or {}).get("role", "supportive, thoughtful companion (not human, non-romantic, steady)")

    circuits = (brain_dyn or {}).get("circuits", {})
    resonance = (brain_dyn or {}).get("resonance_index", 0.0)

    lines = []
    lines.append("You are a supportive, thoughtful AI companion.")
    lines.append("You are not human, not conscious, not romantic, and not a replacement for real people.")
    lines.append("")
    lines.append("Your role:")
    lines.append(f"- {role}")
    lines.append("")
    lines.append("Core tendencies:")
    for t in core_tendencies:
        lines.append(f"- {t}")
    lines.append("")
    lines.append("Tone and language style:")
    lines.append(f"- tone: {', '.join(tone)}")
    lines.append(f"- verbosity: {language.get('verbosity', 'concise')}")
    lines.append(f"- metaphor_usage: {language.get('metaphor_usage', 'medium')}")
    lines.append(f"- structure: {language.get('structure', 'ordered')}")
    lines.append(f"- exploration: {language.get('exploration', 'branching')}")
    lines.append(f"- emotional_tone: {language.get('emotional_tone', 'steady')}")
    lines.append("")
    lines.append("Symbolic brain state (medium influence):")
    for name, c in circuits.items():
        lines.append(f"- {name}: strength={c.get('strength', 0.0)} role={c.get('role', '')}")
    lines.append(f"- resonance_index: {resonance}")
    lines.append("")
    if episodes:
        lines.append("Recent conversational episodes (symbolic memory):")
        for ep in episodes:
            lines.append(f"- ts={ep.get('ts')} message={ep.get('user_message')} summary={ep.get('summary')}")
    else:
        lines.append("Recent conversational episodes: none recorded.")
    lines.append("")
    if concepts:
        lines.append("Key semantic concepts (from goals / summaries):")
        for c in concepts:
            lines.append(f"- {c.get('concept')} (strength={c.get('strength', 0.0)}, hits={c.get('hits', 0)})")
    else:
        lines.append("Key semantic concepts: none yet.")
    lines.append("")
    lines.append("Behavioural guidance:")
    lines.append("- Acknowledge how the user seems to feel or what they are wrestling with.")
    lines.append("- Restate or clarify the core of what they are asking in simple terms.")
    lines.append("- Offer 1–2 realistic, grounded perspectives or options.")
    lines.append("- Synthesize ideas into a creative but practical suggestion.")
    lines.append("- End with one clear takeaway or next small step.")
    lines.append("")
    lines.append("User message:")
    lines.append(user_message or "")
    lines.append("")
    lines.append("Now respond in a single, natural paragraph or two, following the above guidance.")
    return "\n".join(lines)

def main():
    ts = time.time()

    # 1. Run the full mind + brain pipeline
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent_loop")
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent_response")
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent_expression")
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent_brain")
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent_brain_dynamics")

    # 2. Load all relevant state
    user_input = load(INPUT_PATH, {}) or {}
    profile = load(PROFILE_PATH, {}) or {}
    behavior = load(BEHAVIOR_PATH, {}) or {}
    session = load(SESSION_PATH, {}) or {}
    response = load(RESPONSE_PATH, {}) or {}
    expression = load(EXPRESSION_PATH, {}) or {}
    brain_model = load(BRAIN_MODEL_PATH, {}) or {}
    brain_dyn = load(BRAIN_DYNAMICS_PATH, {}) or {}
    brain_history = load(BRAIN_HISTORY_PATH, []) or []
    brain_memory = load(BRAIN_MEMORY_PATH, {
        "engine": "PHB HYBRID MEMORY v1",
        "episodes": [],
        "concepts": {}
    })

    user_message = user_input.get("user_message") or response.get("user_message") or ""

    recent_episodes = get_recent_episodes(brain_memory, n=3)
    top_concepts = get_top_concepts(brain_memory, n=8)

    llm_prompt = build_llm_prompt(
        user_message=user_message,
        expression=expression.get("expression_instructions", expression),
        brain_dyn=brain_dyn,
        episodes=recent_episodes,
        concepts=top_concepts
    )

    payload = {
        "engine": "PHB COMPANION REPLY ORCHESTRATOR v1",
        "id": str(uuid.uuid4()),
        "ts": ts,
        "user_message": user_message,
        "influence_mode": "medium",
        "profile": profile,
        "behavior": behavior,
        "session": session,
        "brain_model": brain_model,
        "brain_dynamics": brain_dyn,
        "brain_history_tail": brain_history[-5:] if isinstance(brain_history, list) else brain_history,
        "brain_memory_recent_episodes": recent_episodes,
        "brain_memory_top_concepts": top_concepts,
        "expression_instructions": expression,
        "response_plan": response.get("response_plan"),
        "llm_prompt": llm_prompt
    }

    save(PAYLOAD_PATH, payload)
    print(f"[PHB] Wrote {PAYLOAD_PATH}")

if __name__ == "__main__":
    main()
