from memory_agent import MemoryAgent
from emotion_agent import EmotionAgent
from reasoning_agent import ReasoningAgent

memory = MemoryAgent()
emotion = EmotionAgent()
reasoning = ReasoningAgent()

def run_agent(message, state):

    mood = emotion.detect(message)

    memory.store(message, mood)

    context = memory.recall(message)

    plan = reasoning.plan(message, context, state)

    response = reasoning.respond(message, context, mood, plan)

    return {
        "input": message,
        "mood": mood,
        "plan": plan,
        "response": response,
        "memory_hits": context
    }
