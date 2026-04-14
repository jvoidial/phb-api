import time
from datetime import datetime, timezone

def generate_goals(memory, timeline):
    """
    Simple goal inference engine from memory patterns
    """

    goals = []

    memory_count = len(memory)
    event_count = len(timeline)

    # basic emergence rules (safe heuristic system)
    if memory_count > 10:
        goals.append("stabilize_memory_growth")

    if event_count > 10:
        goals.append("compress_timeline_history")

    if memory_count > 20:
        goals.append("extract_learning_patterns")

    if not goals:
        goals.append("observe_and_learn")

    return goals


def prioritize(goals):
    return sorted(goals, key=lambda x: len(x), reverse=True)
