import time

def run_tool(msg):
    msg = msg.lower()

    if "time" in msg:
        return time.ctime()

    if "calc" in msg:
        try:
            expr = msg.replace("calc", "").strip()
            return str(eval(expr))
        except:
            return "calc error"

    if "hello" in msg:
        return "Hello. I am your AI OS assistant."

    return "processed"
