#!/bin/bash

echo "🧠 PHB MEMORY SCHEMA NORMALISATION PATCH..."

cat << 'PYEOF' > phb/memory/recall_engine.py
def normalize(entry):
    """
    Ensure all memory entries are dict-based
    """
    if isinstance(entry, dict):
        return entry

    return {
        "input": str(entry),
        "timestamp": None
    }


def retrieve_relevant(memory_store, query):
    results = []

    for k, entry in memory_store.items():
        entry = normalize(entry)

        text = entry.get("input", "")

        if query.lower() in text.lower():
            results.append(entry)

    return results


def build_context(memory_store, query):
    relevant = retrieve_relevant(memory_store, query)

    return {
        "context_summary": [r.get("input", "") for r in relevant[-5:]]
    }
PYEOF

echo "🔄 Restart required after patch"
