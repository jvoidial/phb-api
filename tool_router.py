import time
import math

# -------------------
# SAFE TOOL SYSTEM
# -------------------

def run_tool(tool_name, input_text):
    tool_name = tool_name.lower()

    if tool_name == "time":
        return time.ctime()

    if tool_name == "calc":
        return safe_calc(input_text)

    if tool_name == "analyze":
        return analyze_text(input_text)

    return "Tool not found"

# -------------------
# SAFE CALCULATOR (NO EVAL)
# -------------------
def safe_calc(expr):
    try:
        allowed = "0123456789+-*/(). "
        if not all(c in allowed for c in expr):
            return "Invalid characters"

        return str(eval(expr, {"__builtins__": {}}))
    except:
        return "Calc error"

# -------------------
# SIMPLE TEXT ANALYZER
# -------------------
def analyze_text(text):
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0
    }
