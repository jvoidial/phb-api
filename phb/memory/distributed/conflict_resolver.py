class ConflictResolver:
    def resolve(self, entries):
        if not entries:
            return None

        # simple strategy: latest wins
        return sorted(entries, key=lambda x: len(str(x["value"])), reverse=True)[0]
