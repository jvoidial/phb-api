class Improver:
    def suggest(self, snapshot, score):
        suggestions = []

        if score < 70:
            suggestions.append("⚠️ Optimize task scheduler load")

        if snapshot["memory_users"] > 50:
            suggestions.append("🧠 Consider memory pruning strategy")

        if snapshot["agents"] > 20:
            suggestions.append("🤖 Agent pooling recommended")

        if not suggestions:
            suggestions.append("🟢 System stable")

        return suggestions
