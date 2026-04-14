import math
from typing import List, Dict, Any, Optional


class PHBBrainState:
    def __init__(
        self,
        energy: float = 3.5,
        mood: str = "neutral",
        veil: str = "hazy",
        turns: int = 0,
        arc: str = "stable",
        last_topics: Optional[List[str]] = None,
    ):
        self.energy = energy
        self.mood = mood
        self.veil = veil
        self.turns = turns
        self.arc = arc
        self.last_topics = last_topics or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "energy": self.energy,
            "mood": self.mood,
            "veil": self.veil,
            "turns": self.turns,
            "arc": self.arc,
            "last_topics": self.last_topics[-10:],
        }


class PHBBrain:
    """
    Unified PHB brain module:
    - perception (input understanding)
    - emotional state
    - short-term memory
    - tone shaping
    - reasoning
    - expressive output
    """

    def __init__(self):
        self.state = PHBBrainState()
        self.memory: List[Dict[str, Any]] = []

    # ---------- PERCEPTION LAYER ----------

    def perceive(self, user_message: str) -> Dict[str, Any]:
        text = user_message.strip()
        lower = text.lower()

        intent = "chat"
        if "help" in lower or "stuck" in lower or "broken" in lower:
            intent = "support"
        elif "idea" in lower or "design" in lower or "imagine" in lower:
            intent = "creative"
        elif "deploy" in lower or "curl " in lower or "error" in lower:
            intent = "technical"

        emotional_temp = "neutral"
        if any(x in lower for x in ["angry", "annoyed", "frustrated", "wtf"]):
            emotional_temp = "tense"
        elif any(x in lower for x in ["love this", "so good", "excited", "hyped"]):
            emotional_temp = "bright"
        elif any(x in lower for x in ["tired", "exhausted", "drained"]):
            emotional_temp = "low"
        elif any(x in lower for x in ["confused", "lost", "unsure"]):
            emotional_temp = "uncertain"

        topics = []
        if "deploy" in lower or "railway" in lower:
            topics.append("deployment")
        if "docker" in lower:
            topics.append("docker")
        if "brain" in lower or "mind" in lower:
            topics.append("cognitive")
        if "phb" in lower:
            topics.append("phb")
        if "companion" in lower:
            topics.append("companion")

        return {
            "raw": text,
            "intent": intent,
            "emotional_temp": emotional_temp,
            "topics": topics,
        }

    # ---------- EMOTIONAL ENGINE ----------

    def update_emotional_state(self, perception: Dict[str, Any]) -> None:
        self.state.turns += 1

        # Energy decay / boost
        if perception["emotional_temp"] == "bright":
            self.state.energy = min(5.0, self.state.energy + 0.2)
        elif perception["emotional_temp"] == "tense":
            self.state.energy = max(1.0, self.state.energy - 0.1)
        elif perception["emotional_temp"] == "low":
            self.state.energy = max(1.0, self.state.energy - 0.2)
        else:
            # gentle drift toward mid
            if self.state.energy < 3.5:
                self.state.energy += 0.05
            elif self.state.energy > 3.5:
                self.state.energy -= 0.05

        # Mood selection
        mood = "neutral"
        if perception["emotional_temp"] == "tense":
            mood = "steady_support"
        elif perception["emotional_temp"] == "bright":
            mood = "bright"
        elif perception["emotional_temp"] == "low":
            mood = "soft"
        elif perception["emotional_temp"] == "uncertain":
            mood = "clarifying"
        else:
            # base on energy
            if self.state.energy >= 4.0:
                mood = "engaged"
            elif self.state.energy <= 2.5:
                mood = "gentle"
            else:
                mood = "neutral"

        self.state.mood = mood

        # Veil based on energy
        if self.state.energy >= 4.2:
            self.state.veil = "clear"
        elif self.state.energy <= 2.3:
            self.state.veil = "foggy"
        else:
            self.state.veil = "hazy"

        # Arc based on recent emotional temps
        temps = [m.get("perception", {}).get("emotional_temp") for m in self.memory[-6:]]
        temps = [t for t in temps if t]
        if temps.count("tense") >= 3:
            self.state.arc = "stabilising"
        elif temps.count("bright") >= 3:
            self.state.arc = "expansive"
        elif temps.count("low") >= 3:
            self.state.arc = "supportive"
        else:
            self.state.arc = "stable"

        # Topics
        self.state.last_topics.extend(perception["topics"])

    # ---------- MEMORY LAYER ----------

    def remember(self, perception: Dict[str, Any], plan: str, reasoning: str) -> None:
        self.memory.append(
            {
                "perception": perception,
                "plan": plan,
                "reasoning": reasoning,
                "state": self.state.to_dict(),
            }
        )
        # keep memory bounded
        if len(self.memory) > 50:
            self.memory = self.memory[-50:]

    # ---------- TONE SHAPING ----------

    def choose_tone(self) -> str:
        mood = self.state.mood
        veil = self.state.veil
        arc = self.state.arc

        # blended adaptive tone
        if mood in ["bright", "engaged"]:
            return "bright_expressive"
        if mood in ["soft", "gentle"] or arc == "supportive":
            return "soft_warm"
        if mood == "clarifying" or arc == "stabilising":
            return "calm_articulate"
        if veil == "foggy":
            return "slow_grounded"
        return "balanced_companion"

    # ---------- REASONING LAYER ----------

    def plan_response(self, perception: Dict[str, Any]) -> str:
        intent = perception["intent"]
        temp = perception["emotional_temp"]
        topics = perception["topics"]

        if intent == "support":
            return "stabilise_and_reassure"
        if intent == "technical":
            if temp in ["tense", "uncertain"]:
                return "clarify_and_guide"
            return "explain_and_confirm"
        if intent == "creative":
            return "explore_and_amplify"
        # default chat
        if "companion" in topics or "phb" in topics or "cognitive" in topics:
            return "reflect_and_co_think"
        return "light_companion_reply"

    # ---------- EXPRESSION LAYER ----------

    def generate_summary(
        self,
        perception: Dict[str, Any],
        tone: str,
        plan: str,
    ) -> str:
        msg = perception["raw"]

        # base acknowledgement
        base = f"“{msg}” — "

        if tone == "soft_warm":
            if plan == "stabilise_and_reassure":
                return base + "I’m here with you. Let’s steady this together, one clear step at a time."
            if plan == "clarify_and_guide":
                return base + "okay, I can feel the friction in this. Let’s untangle it gently and make it make sense."
            return base + "I’m listening, softly, and I’m taking you seriously."

        if tone == "bright_expressive":
            if plan == "explore_and_amplify":
                return base + "I love where you’re pointing—let’s push this idea further and see what else it can become."
            return base + "I’m awake with you on this—let’s move with it."

        if tone == "calm_articulate":
            if plan == "clarify_and_guide":
                return base + "let me lay this out clearly so it feels less tangled and more navigable."
            return base + "I’m going to keep this grounded and clear so you can see the whole shape."

        if tone == "slow_grounded":
            return base + "I’m moving a little slower here, on purpose—so we don’t miss anything important."

        # balanced_companion
        if plan == "reflect_and_co_think":
            return base + "I’m thinking this through with you, not above you—let’s map the shape of it together."
        if plan == "explain_and_confirm":
            return base + "got you. I’ll explain what’s happening and make sure it actually lands."
        if plan == "light_companion_reply":
            return base + "okay, I’m here, tuned in, and ready to move with whatever you throw next."

        return base + "okay, I’m here and tracking you."

    # ---------- PUBLIC INTERFACE ----------

    def process(self, user_message: str) -> Dict[str, Any]:
        perception = self.perceive(user_message)
        self.update_emotional_state(perception)
        plan = self.plan_response(perception)
        tone = self.choose_tone()
        summary = self.generate_summary(perception, tone, plan)

        reasoning = (
            f"energy={self.state.energy:.2f}, "
            f"mood={self.state.mood}, "
            f"veil={self.state.veil}, "
            f"arc={self.state.arc}, "
            f"tone={tone}, "
            f"plan={plan}"
        )

        self.remember(perception, plan, reasoning)

        return {
            "perception": f"Received: {user_message}",
            "plan": plan,
            "reasoning": reasoning,
            "summary": summary,
            "brain_state": self.state.to_dict(),
        }


# Singleton-style brain instance for simple integration
_phb_brain_instance: Optional[PHBBrain] = None


def get_phb_brain() -> PHBBrain:
    global _phb_brain_instance
    if _phb_brain_instance is None:
        _phb_brain_instance = PHBBrain()
    return _phb_brain_instance


def run_phb_brain(user_message: str) -> Dict[str, Any]:
    brain = get_phb_brain()
    return brain.process(user_message)
# force copy Tue Apr 14 15:13:40 BST 2026
