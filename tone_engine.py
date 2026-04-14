def humanize(mood, memory_hits, message):

    base = ""

    if mood == "soft":
        base = "I’m here with you… "
    elif mood == "warm":
        base = "Hey, I’m really glad you’re here. "
    else:
        base = "I’m listening. "

    if memory_hits:
        base += "I remember you mentioned something similar before. "

    if "tired" in message:
        base += "It sounds like things have been a bit heavy lately."

    return base
