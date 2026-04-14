import math
from datetime import datetime, timezone

# simple lightweight similarity (no heavy ML deps)
def similarity(a, b):
    a_words = set(str(a).lower().split())
    b_words = set(str(b).lower().split())

    if not a_words or not b_words:
        return 0.0

    intersection = a_words.intersection(b_words)
    union = a_words.union(b_words)

    return len(intersection) / len(union)


def retrieve_relevant(memory_store, query, top_k=5):
    scored = []

    for ts, entry in memory_store.items():
        text = entry.get("input", "")

        score = similarity(query, text)

        scored.append({
            "timestamp": ts,
            "entry": entry,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]


def build_context(memory_store, query):
    results = retrieve_relevant(memory_store, query)

    context = {
        "query": query,
        "matches": results,
        "context_summary": [
            r["entry"]["input"] for r in results if r["score"] > 0
        ]
    }

    return context
