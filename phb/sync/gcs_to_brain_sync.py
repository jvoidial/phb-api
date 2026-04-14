import json
from phb.sync.gcs_json_sync import export_json
from phb.brain.global_brain import GlobalBrain

brain = GlobalBrain()

def sync():
    print("🧠 Syncing GCS → GLOBAL BRAIN")

    gcs_state = export_json()
    updated = brain.update_from_gcs(gcs_state)

    print("✔ Brain updated")
    return updated

if __name__ == "__main__":
    sync()
