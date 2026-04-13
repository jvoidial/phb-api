import time
from typing import Literal

Mode = Literal["analytical", "creative", "strategic", "supportive", "diagnostic"]

def _detect_mode(user_message: str, emotion: str) -> Mode:
    msg = user_message.lower()
    if any(k in msg for k in ("plan", "roadmap", "strategy", "next step", "design a better flow")):
        return "strategic"
    if any(k in msg for k in ("why", "how does", "explain", "logic", "keeps happening", "stuck at the same point")):
        return "analytical"
    if any(k in msg for k in ("idea", "brainstorm", "imagine", "what if")):
        return "creative"
    if emotion in ("stressed",):
        return "supportive"
    return "diagnostic"

def _perception_layer(user_message: str) -> dict:
    text = user_message.strip()
    lower = text.lower()
    tokens = lower.split()
    return {
        "raw": text,
        "lower": lower,
        "tokens": tokens,
        "length": len(tokens),
        "has_question": "?" in text or any(t in tokens for t in ("why", "how", "what")),
    }

def _context_layer(session_id: str, recent_context: list[dict], emotion: str, tone: str) -> dict:
    last_user = None
    all_user_msgs: list[str] = []
    for c in recent_context:
        if c.get("role") == "user":
            all_user_msgs.append(c.get("content", ""))
            last_user = c.get("content", "")
    themes = _extract_themes(all_user_msgs)
    return {
        "session_id": session_id,
        "last_user_message": last_user,
        "emotion": emotion,
        "tone": tone,
        "turns": len(recent_context),
        "themes": themes,
    }

def _extract_themes(messages: list[str]) -> list[str]:
    joined = " ".join(m.lower() for m in messages)
    themes: list[str] = []
    if any(k in joined for k in ("stuck", "blocked", "keep happening", "loop", "stuck at the same point")):
        themes.append("recurring friction / stuck loops")
    if any(k in joined for k in ("plan", "roadmap", "next step", "structure", "design a better flow")):
        themes.append("planning and structure")
    if any(k in joined for k in ("workflow", "system", "pipeline", "flow")):
        themes.append("workflow / system design")
    if any(k in joined for k in ("overwhelmed", "tired", "burnt", "draining")):
        themes.append("load / overwhelm")
    return themes

def _planning_layer(perception: dict, context: dict, mode: Mode) -> dict:
    if mode == "strategic":
        goal = "define current state, constraints, and next concrete steps"
    elif mode == "analytical":
        goal = "explain the structure and logic of why this keeps happening"
    elif mode == "creative":
        goal = "generate a few alternative angles or ideas"
    elif mode == "supportive":
        goal = "stabilise the user and reduce overwhelm before planning"
    else:
        goal = "clarify what the real question is"

    steps: list[str] = []

    if mode in ("strategic", "analytical", "diagnostic"):
        steps.append("1) Restate what you seem to be wrestling with in plain language.")
        steps.append("2) Identify the core pattern or decision point.")
        steps.append("3) Offer 1–3 concrete next moves that don’t overwhelm you.")

    if mode == "creative":
        steps.append("1) Offer 2–3 different angles or ideas.")
    if mode == "supportive":
        steps.append("1) Normalise the difficulty.")
        steps.append("2) Narrow focus to one manageable piece.")
        steps.append("3) Suggest a small, doable next action.")

    planning_skeleton = {
        "current_state": "You’re in the middle of a process and something keeps snagging.",
        "constraints": [],
        "options": [],
        "next_moves": [],
    }

    if "workflow / system design" in context["themes"]:
        planning_skeleton["constraints"].append("Your workflow/system has hidden friction points.")
    if "recurring friction / stuck loops" in context["themes"]:
        planning_skeleton["constraints"].append("You’re looping on the same kind of blockage.")
    if "planning and structure" in context["themes"]:
        planning_skeleton["options"].append("Introduce clearer phases or checkpoints.")
    if "load / overwhelm" in context["themes"]:
        planning_skeleton["constraints"].append("Your cognitive load is high; plans must stay simple.")

    if mode in ("strategic", "analytical"):
        planning_skeleton["next_moves"].append("Name the exact point in the workflow where you feel the snag.")
        planning_skeleton["next_moves"].append("Decide on one small experiment to change that point, not the whole system.")

    return {
        "goal": goal,
        "steps": steps,
        "mode": mode,
        "has_question": perception["has_question"],
        "planning_skeleton": planning_skeleton,
    }

def _reasoning_domains(perception: dict, context: dict, emotion: str) -> dict:
    """
    Safety-first multi-domain reasoning.
    No diagnosis. Only factors + questions.
    """
    msg = perception["lower"]
    themes = context.get("themes", [])

    body = {
        "signals": [],
        "questions": [
            "Have you been more tired, wired, or low-energy than usual lately?",
            "Has your sleep, food, or basic rhythm been off in a way you can feel?"
        ],
    }
    mind = {
        "signals": [],
        "questions": [
            "Is there a story you tell yourself at this snag point (e.g. 'I always fail here')?",
            "Does this feel more like anxiety, boredom, perfectionism, or something else?"
        ],
    }
    workflow = {
        "signals": [],
        "questions": [
            "Is this snag tied to a specific tool, step, or handoff in your process?",
            "Would this feel easier if the step were smaller or framed differently?"
        ],
        }

def _internal_dialogue(perception: dict, context: dict, plan: dict) -> list[str]:
    voices: list[str] = []

    voices.append(f"[planner] Goal: {plan['goal']}. Mode: {plan['mode']}.")

    if context["last_user_message"]:
        voices.append(f"[context] Last user message: “{context['last_user_message']}”.")

    if context["themes"]:
        voices.append("[themes] I’m noticing these themes in this session: " + ", ".join(context["themes"]) + ".")

    if plan["has_question"]:
        voices.append("[analyst] There’s a question or implicit request for explanation/decision here.")
    else:
        voices.append("[analyst] This might be more of a state description; I should help turn it into a clear question or next step.")

    if plan["steps"]:
        voices.append("[strategist] I’ll roughly follow these steps: " + " ".join(plan["steps"]))

    return voices

def _expression_layer(
    perception: dict,
    context: dict,
    plan: dict,
    dialogue: list[str],
) -> str:
    base = "Here’s how I’m reading this: "

    if context["last_user_message"]:
        base += f"you’ve recently said “{context['last_user_message']}”, and this feels like another pass at the same knot. "
    else:
        base += "you’re opening a new thread here. "

    if context["themes"]:
        base += "Across this session I’m picking up themes around " + ", ".join(context["themes"]) + ". "

    if plan["mode"] == "strategic":
        mode_line = "I’ll treat this as a planning problem and focus on concrete next moves."
    elif plan["mode"] == "analytical":
        mode_line = "I’ll treat this as a logic/structure question and make the pattern explicit."
    elif plan["mode"] == "creative":
        mode_line = "I’ll treat this as an idea‑space and offer a few different angles."
    elif plan["mode"] == "supportive":
        mode_line = "I’ll keep things steady and manageable so this doesn’t feel overwhelming."
    else:
        mode_line = "I’ll first clarify what the real question is before going deeper."

    return base + mode_line

def run_intelligence_core(
    session_id: str,
    user_message: str,
    recent_context: list[dict],
    emotion: str,
    tone: str,
) -> dict:
    ts = time.time()
    perception = _perception_layer(user_message)
    context = _context_layer(session_id, recent_context, emotion, tone)
    mode = _detect_mode(user_message, emotion)
    plan = _planning_layer(perception, context, mode)
    reasoning_domains = _reasoning_domains(perception, context, emotion)
    resonance = _resonance_resolve_engine(reasoning_domains, plan, emotion)
    dialogue = _internal_dialogue(perception, context, plan)
    summary = _expression_layer(perception, context, plan, dialogue)

    return {
        "ts": ts,
        "mode": mode,
        "perception": perception,
        "context": context,
        "plan": plan,
        "reasoning_domains": reasoning_domains,
        "resonance": resonance,
        "internal_dialogue": dialogue,
        "summary": summary,
    }

# ------------------------------------------------------------
# Public wrapper expected by phb_api.py
# ------------------------------------------------------------
def generate_companion_reply(user_message: str) -> dict:
    """
    Thin wrapper so the API can call the intelligence core
    without needing session management or context plumbing.
    """
    session_id = "default"
    recent_context = []
    emotion = "neutral"
    tone = "warm"

    core = run_intelligence_core(
        session_id=session_id,
        user_message=user_message,
        recent_context=recent_context,
        emotion=emotion,
        tone=tone,
    )

    # Convert core output into the API's expected structure
    return {
        "engine": "PHB INTELLIGENCE CORE v1",
        "id": f"core-{int(core['ts'])}",
        "ts": core["ts"],
        "user_message": user_message,
        "reply": {
            "text": core["summary"],
            "mode": core["mode"],
            "orientation": "growth-directed",
        },
        "meta": {
            "api": "PHB Universal API",
            "version": "v1",
        },
        "core": core,
    }
