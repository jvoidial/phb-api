class StateDiff:
    def compare(self, before, after):
        diffs = {}

        for node in before["nodes"]:
            b = before["nodes"][node].get("load", 0)
            a = after["nodes"][node].get("load", 0)
            diffs[node] = a - b

        return diffs
