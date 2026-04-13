def run_engine(input_text: str, mode: str = "robot") -> dict:
    text = input_text.lower().strip()

    if "forward" in text:
        return {
            "intent": "move_forward",
            "action": "motor.forward",
            "confidence": 0.9,
            "state": {
                "raw": input_text,
                "tokens": text.split(),
                "intent": "move_forward",
                "mode": mode,
            },
        }

    if "back" in text:
        return {
            "intent": "move_back",
            "action": "motor.back",
            "confidence": 0.9,
            "state": {
                "raw": input_text,
                "tokens": text.split(),
                "intent": "move_back",
                "mode": mode,
            },
        }

    return {
        "intent": "unknown",
        "action": "none",
        "confidence": 0.1,
        "state": {
            "raw": input_text,
            "tokens": text.split(),
            "intent": "unknown",
            "mode": mode,
        },
    }
