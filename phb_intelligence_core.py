import time
from typing import Literal, List, Dict, Any, Optional

# ------------------------------------------------------------
# PHB INTELLIGENCE CORE v2
# Mode engine + voxels + veil + resonance + companion voice
# ------------------------------------------------------------

Mode = Literal["analytical", "creative", "strategic", "supportive", "diagnostic"]

# In‑memory PHB coherence voxels (per session)
PHB_MEMORY: Dict[str, Dict[str, Any]] = {}


# ------------------------------------------------------------
# Perception layer
# ------------------------------------------------------------
def _perception_layer(user_message: str) -> dict:
    text = user_message.strip()
    lower = text.lower()
    tokens = lower.split()

    intensity_words = ["killed", "ruined", "wrecked", "crushed", "destroyed"]
    recurrence_words = ["again", "still", "same", "keeps", "keep", "loop"]
    collapse_words = ["gave up", "stopped", "quit", "lost it"]

    intensity_hits = [w for w in intensity_words if w in lower]
    recurrence_hits = [w for w in recurrence_words if w in lower]
    collapse_hits = [w for w in collapse_words if w in lower]

    return {
        "raw": text,
        "lower": lower,
        "tokens": tokens,
        "length": len(tokens),
        "has_question": "?" in text or any(t in tokens for t in ("why", "how", "what")),
        "intensity_hits": intensity_hits,
        "recurrence_hits": recurrence_hits,
        "collapse_hits": collapse_hits,
    }


# ------------------------------------------------------------
# Emotional inference (very light, non‑clinical)
# ------------------------------------------------------------
def _infer_emotion(perception: dict) -> str:
    lower = perception["lower"]
    if any(w in lower for w in ("overwhelmed", "too much", "burnt", "burned out")):
        return "stressed"
    if any(w in lower for w in ("tired", "exhausted", "drained")):
        return "tired"
    if any(w in lower for w in ("excited", "pumped", "hyped")):
        return "energised"
    if perception["intensity_hits"]:
        return "frustrated"
    return "neutral"


# ------------------------------------------------------------
# Mode engine (weighted)
# ------------------------------------------------------------
def _detect_mode(perception: dict, inferred_emotion: str, last_mode: Optional[Mode]) -> Mode:
    msg = perception["lower"]
    weights: Dict[Mode, float] = {
        "analytical": 0.0,
        "creative": 0.0,
        "strategic": 0.0,
        "supportive": 0.0,
        "diagnostic": 0.0,
    }

    # Recurring friction → analytical
    if perception["recurrence_hits"]:
        weights["analytical"] += 2.0

    # Planning / structure → strategic
    if any(k in msg for k in ("plan", "roadmap", "strategy", "next step", "design a better flow")):
        weights["strategic"] += 2.0

    # Idea space → creative
    if any(k in msg for k in ("idea", "brainstorm", "imagine", "what if")):
        weights["creative"] += 2.0

    # Collapse / overwhelm → supportive
    if perception["collapse_hits"]:
        weights["supportive"] += 1.5
    if inferred_emotion in ("stressed", "tired"):
        weights["supportive"] += 1.0

    # Question → analytical / diagnostic
    if perception["has_question"]:
        weights["analytical"] += 1.0
    else:
        weights["diagnostic"] += 0.5

    # Continuity bias
    if last_mode is not None:
        weights[last_mode] += 0.5

    # Default bias
    weights["diagnostic"] += 0.2

    # Pick max
    mode = max(weights.items(), key=lambda kv: kv[1])[0]
    return mode


# ------------------------------------------------------------
# Theme extraction + context
# ------------------------------------------------------------
def _extract_themes(messages: List[str]) -> List[str]:
    joined = " ".join(m.lower() for m in messages)
    themes: List[str] = []
    if any(k in joined for k in ("stuck", "blocked", "keep happening", "loop", "same wall", "stuck at the same point")):
        themes.append("recurring friction / stuck loops")
    if any(k in joined for k in ("plan", "roadmap", "next step", "structure", "design a better flow")):
        themes.append("planning and structure")
    if any(k in joined for k in ("workflow", "system", "pipeline", "flow")):
        themes.append("workflow / system design")
    if any(k in joined for k in ("overwhelmed", "tired", "burnt", "draining", "too much")):
        themes.append("load / overwhelm")
    return themes


def _context_layer(session_id: str, recent_context: List[dict], emotion: str, tone: str) -> dict:
    last_user = None
    all_user_msgs: List[str] = []
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


# ------------------------------------------------------------
# Memory voxels (with energy decay)
# ------------------------------------------------------------
def _load_memory(session_id: str) -> Dict[str, Any]:
    return PHB_MEMORY.get(session_id, {"voxels": [], "last_mode": None})


def _store_memory(session_id: str, memory: Dict[str, Any]) -> None:
    PHB_MEMORY[session_id] = memory


def _decay_energy(energy: float, dt: float) -> float:
    # Simple exponential-ish decay: more time → lower energy
    decay_factor = 0.1 * dt  # very rough; dt in seconds, but we keep it tiny
    return max(0.0, energy * (1.0 - min(decay_factor, 0.5)))


def _update_memory_voxels(memory: Dict[str, Any], themes: List[str], ts: float) -> Dict[str, Any]:
    voxels: List[Dict[str, Any]] = memory.get("voxels", [])
    existing_by_theme = {v["theme"]: v for v in voxels}

    # Decay all voxels
    for v in voxels:
        last_ts = v.get("last_seen_ts", ts)
        dt = max(0.0, ts - last_ts) / 3600.0  # hours
        v["energy"] = _decay_energy(v.get("energy", 1.0), dt)

    # Update / create voxels for current themes
    for t in themes:
        if t in existing_by_theme:
            v = existing_by_theme[t]
            v["last_seen_ts"] = ts
            v["energy"] = min(v.get("energy", 1.0) + 0.5, 5.0)
            v["count"] = v.get("count", 1) + 1
        else:
            voxels.append(
                {
                    "theme": t,
                    "first_seen_ts": ts,
                    "last_seen_ts": ts,
                    "energy": 1.5,
                    "count": 1,
                }
            )

    memory["voxels"] = voxels
    return memory


# ------------------------------------------------------------
# Planning layer
# ------------------------------------------------------------
def _planning_layer(perception: dict, context: dict, mode: Mode) -> dict:
    if mode == "strategic":
        goal = "define current state, constraints, and next concrete steps"
    elif mode == "analytical":
        goal = "explain the structure and logic of why this keeps happening"
    elif mode == "creative":
        goal = "generate a few alternative angles or ideas"
    elif mode == "supportive":
        goal = "stabilise you and reduce overwhelm before planning"
    else:
        goal = "clarify what the real question is"

    steps: List[str] = []

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


# ------------------------------------------------------------
# Reasoning domains
# ------------------------------------------------------------
def _reasoning_domains(perception: dict, context: dict, emotion: str) -> dict:
    themes = context.get("themes", [])

    body = {
        "signals": [],
        "questions": [
            "Have you been more tired, wired, or low-energy than usual lately?",
            "Has your sleep, food, or basic rhythm been off in a way you can feel?",
        ],
    }
    mind = {
        "signals": [],
        "questions": [
            "Is there a story you tell yourself at this snag point (e.g. 'I always fail here')?",
            "Does this feel more like anxiety, boredom, perfectionism, or something else?",
        ],
    }
    workflow = {
        "signals": [],
        "questions": [
            "Is this snag tied to a specific tool, step, or handoff in your process?",
            "Would this feel easier if the step were smaller or framed differently?",
        ],
    }

    return {
        "body": body,
        "mind": mind,
        "workflow": workflow,
        "themes": themes,
        "emotion": emotion,
    }


# ------------------------------------------------------------
# Veil simulator
# ------------------------------------------------------------
def _veil_state(reasoning_domains: dict, voxels: List[dict]) -> dict:
    themes = reasoning_domains.get("themes", [])
    load = "load / overwhelm" in themes
    loops = "recurring friction / stuck loops" in themes

    # Aggregate energy
    total_energy = sum(v.get("energy", 0.0) for v in voxels)
    level = "clear"

    if loops or load or total_energy > 2.0:
        level = "thin"
    if (loops and load) or total_energy > 4.0:
        level = "heavy"
    if total_energy > 7.0:
        level = "opaque"

    return {
        "level": level,
        "loops": loops,
        "overwhelm": load,
        "energy": total_energy,
    }


# ------------------------------------------------------------
# Resonance engine
# ------------------------------------------------------------
def _resonance_resolve_engine(reasoning_domains: dict, plan: dict, emotion: str, veil: dict) -> dict:
    mode = plan.get("mode", "diagnostic")
    level = veil.get("level", "clear")

    if level in ("heavy", "opaque") and mode in ("strategic", "analytical"):
        alignment = "strained"
        notes = "Friction is high; keep plans small and language gentle."
    elif level == "thin":
        alignment = "cautious"
        notes = "There’s some friction; balance clarity with reassurance."
    else:
        alignment = mode
        notes = "Plan and emotional state seem reasonably aligned."

    return {
        "signal": "stable" if alignment != "strained" else "strained",
        "emotion": emotion,
        "alignment": alignment,
        "notes": notes,
        "domains": list(reasoning_domains.keys()),
    }


# ------------------------------------------------------------
# Internal dialogue
# ------------------------------------------------------------
def _internal_dialogue(perception: dict, context: dict, plan: dict, veil: dict) -> List[str]:
    voices: List[str] = []

    voices.append(f"[planner] Goal: {plan['goal']}. Mode: {plan['mode']}.")
    if context["last_user_message"]:
        voices.append(f"[context] Last user message: “{context['last_user_message']}”.")
    if context["themes"]:
        voices.append("[themes] I’m noticing these themes: " + ", ".join(context["themes"]) + ".")
    voices.append(f"[veil] Current veil level: {veil['level']} (energy={veil['energy']:.2f}).")

    if plan["has_question"]:
        voices.append("[analyst] There’s a question or implicit request for explanation/decision here.")
    else:
        voices.append("[analyst] This might be more of a state description; I should help turn it into a clear question or next step.")

    if plan["steps"]:
        voices.append("[strategist] I’ll roughly follow these steps: " + " ".join(plan["steps"]))

    return voices


# ------------------------------------------------------------
# Meta expression layer (internal summary)
# ------------------------------------------------------------
def _expression_layer(
    perception: dict,
    context: dict,
    plan: dict,
    dialogue: List[str],
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


# ------------------------------------------------------------
# Companion surface reply (human voice)
# ------------------------------------------------------------
def _companion_surface_reply(user_message: str, core: dict) -> str:
    mode: Mode = core["mode"]
    themes: List[str] = core["context"]["themes"]
    veil = core["veil"]

    opener = "That sounds really frustrating—hitting something that knocks your momentum like that."
    if "recurring friction / stuck loops" in themes:
        opener = "You’re not imagining it—this really does sound like the same wall showing up again."
    if veil["level"] in ("heavy", "opaque"):
        opener = opener + " It makes sense that it feels heavier when it keeps happening."

    if mode == "analytical":
        body = "Let’s name exactly where it happens and why it bites so hard, then pick one small change to try."
    elif mode == "strategic":
        body = "We can treat this like a design problem and sketch a different way that moment could go."
    elif mode == "supportive":
        body = "We can slow it down, look at that moment closely, and make it feel a bit lighter and more manageable."
    elif mode == "creative":
        body = "We can play with a couple of different ways that moment could go, and see which one feels most alive to you."
    else:
        body = "We can slow it down, look at that moment closely, and decide what you actually want there."

    return f"{opener} {body}"


# ------------------------------------------------------------
# Core runner
# ------------------------------------------------------------
def run_intelligence_core(
    session_id: str,
    user_message: str,
    recent_context: List[dict],
    explicit_emotion: Optional[str] = None,
    tone: str = "warm",
) -> dict:
    ts = time.time()
    perception = _perception_layer(user_message)

    # Load memory + last mode
    memory = _load_memory(session_id)
    last_mode: Optional[Mode] = memory.get("last_mode")

    inferred_emotion = explicit_emotion or _infer_emotion(perception)
    context = _context_layer(session_id, recent_context, inferred_emotion, tone)
    mode = _detect_mode(perception, inferred_emotion, last_mode)
    plan = _planning_layer(perception, context, mode)
    reasoning_domains = _reasoning_domains(perception, context, inferred_emotion)

    # Update memory voxels with current themes
    memory = _update_memory_voxels(memory, context["themes"], ts)
    voxels = memory.get("voxels", [])

    veil = _veil_state(reasoning_domains, voxels)
    resonance = _resonance_resolve_engine(reasoning_domains, plan, inferred_emotion, veil)
    dialogue = _internal_dialogue(perception, context, plan, veil)
    summary = _expression_layer(perception, context, plan, dialogue)

    # Persist last mode
    memory["last_mode"] = mode
    _store_memory(session_id, memory)

    return {
        "ts": ts,
        "mode": mode,
        "perception": perception,
        "context": context,
        "plan": plan,
        "reasoning_domains": reasoning_domains,
        "resonance": resonance,
        "veil": veil,
        "internal_dialogue": dialogue,
        "summary": summary,
        "memory": memory,
    }


# ------------------------------------------------------------
# Public wrapper expected by API
# ------------------------------------------------------------
def generate_companion_reply(user_message: str) -> dict:
    # For now, single default session + no external context
    session_id = "default"
    recent_context: List[dict] = []
    explicit_emotion: Optional[str] = None

    core = run_intelligence_core(
        session_id=session_id,
        user_message=user_message,
        recent_context=recent_context,
        explicit_emotion=explicit_emotion,
        tone="warm",
    )

    surface = _companion_surface_reply(user_message, core)

    return {
        "engine": "PHB INTELLIGENCE CORE v2",
        "id": f"core-{int(core['ts'])}",
        "ts": core["ts"],
        "user_message": user_message,
        "reply": {
            "text": surface,
            "mode": core["mode"],
            "orientation": "growth-directed",
        },
        "meta": {
            "api": "PHB Universal API",
            "version": "v2",
        },
        "core": core,
    }
