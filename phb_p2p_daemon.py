import time
from phb.brain.p2p_sync import sync

print("🌐 PHB P2P BRAIN SYNC STARTED")

while True:
    try:
        sync()
        print("✔ Brain synced across peers")
    except Exception as e:
        print("⚠️ Sync error:", e)

    time.sleep(10)
