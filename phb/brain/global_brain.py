import os
import json
from datetime import datetime, timezone

BRAIN_FILE = "phb_global_brain.json"

class GlobalBrain:
    """
    Single source of truth for PHB memory system.
    Replaces all fragmented memory layers.
    """

    def load(self):
        if not os.path.exists(BRAIN_FILE):
            return self._empty()

        try:
            with open(BRAIN_FILE, "r") as f:
                return json.load(f)
        except:
            return self._empty()

    def save(self, state):
        state["last_updated"] = datetime.now(timezone.utc).isoformat()

        with open(BRAIN_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def _empty(self):
        return {
            "system": "PHB-GLOBAL-BRAIN-v1",
            "memory": {},
            "agents": {},
            "timeline": [],
            "meta": {}
        }

    def update_from_gcs(self, gcs_state):
        brain = self.load()

        brain["memory"]["gcs"] = gcs_state
        brain["timeline"].append({
            "event": "gcs_sync",
            "time": datetime.now(timezone.utc).isoformat()
        })

        self.save(brain)
        return brain
