import time

def run(msg):
    if "time" in msg.lower():
        return time.ctime()
    return None
