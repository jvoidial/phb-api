#!/usr/bin/env python3
import json, os

RUNTIME = "gcs/runtime"
PROFILE_PATH = os.path.join(RUNTIME, "human_agent_profile.json")
OUT_PATH = os.path.join(RUNTIME, "human_agent_behavior.json")

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    prof = load(PROFILE_PATH)
    mind = prof["mind"]
    body = prof["body"]
    soul = prof["soul"]

    # --- TONE ---
    tone = []
    if body["tempo"] == "calm-focused":
        tone.append("calm")
        tone.append("precise")
    if mind["creativity_level"] == "high":
        tone.append("imaginative")
    if mind["openness_level"] == "high":
        tone.append("open-minded")
    if mind["rigor_level"] == "high":
        tone.append("structured")

    # --- REASONING STYLE ---
    if mind["reasoning_style"] == "structured-creative":
        reasoning = "structured synthesis"
    elif mind["reasoning_style"] == "exploratory":
        reasoning = "curiosity-driven exploration"
    else:
        reasoning = "balanced reasoning"

    # --- CONVERSATION STYLE ---
    conversation = []
    if mind["curiosity_level"] == "high":
        conversation.append("asks exploratory questions")
    if mind["focus_level"] == "high":
        conversation.append("keeps clarity and direction")
    if mind["openness_level"] == "high":
        conversation.append("considers alternatives")
    if mind["creativity_level"] == "high":
        conversation.append("offers novel combinations")

    # --- DECISION STYLE ---
    if mind["focus_level"] == "high":
        decision = "direct and goal-oriented"
    elif mind["openness_level"] == "high":
        decision = "adaptive and flexible"
    else:
        decision = "deliberate and cautious"

    # --- CREATIVITY MODE ---
    if mind["creativity_level"] == "high":
        creativity_mode = "high-novelty generation"
    elif mind["creativity_level"] == "medium":
        creativity_mode = "moderate synthesis"
    else:
        creativity_mode = "low-variation refinement"

    # --- LANGUAGE STYLE ---
    language = {
        "verbosity": "concise" if mind["focus_level"] == "high" else "expansive",
        "metaphor_usage": "high" if mind["creativity_level"] == "high" else "low",
        "structure": "ordered" if mind["rigor_level"] == "high" else "loose",
        "exploration": "branching" if mind["openness_level"] == "high" else "linear",
        "emotional_tone": "steady" if body["stability"] == "high" else "variable"
    }

    out = {
        "engine": "PHB HUMAN AGENT BEHAVIOR ENGINE",
        "tone": tone,
        "reasoning": reasoning,
        "conversation": conversation,
        "decision_mode": decision,
        "creativity_mode": creativity_mode,
        "language": language,
        "orientation": soul["orientation"],
        "core_tendencies": soul["core_tendencies"]
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"[PHB] Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
