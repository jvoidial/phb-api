from phb.brain.p2p_sync import sync

def live_sync():
    try:
        sync()
        return True
    except:
        return False
