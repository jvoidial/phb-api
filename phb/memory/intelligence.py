from datetime import datetime, timezone

def score_memory(entry):
    score = 1

    text = entry.get("input", "").lower()

    if len(text) > 20:
        score += 1

    if any(k in text for k in ["important", "remember", "critical"]):
        score += 3

    if any(k in text for k in ["learn", "brain", "system"]):
        score += 2

    return score

def categorize(memory):
    important = []
    recent = []

    for k, v in memory.items():
        score = score_memory(v)

        if score >= 4:
            important.append(v)

        recent.append(v)

    recent = sorted(recent, key=lambda x: x.get("time", ""), reverse=True)[:5]

    return {
        "important": important,
        "recent": recent
    }
