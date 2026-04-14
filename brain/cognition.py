from memory.vector_memory import add, search

def perceive(msg):
    mood="neutral"
    if any(x in msg.lower() for x in ["tired","sad","overwhelmed"]):
        mood="soft"
    return mood

def recall(user,msg):
    return search(user,msg)

def respond(msg,mem,mood):
    if mem:
        return "I remember this pattern. You're not alone."
    return "I'm here with you."

def run(msg,user,state):

    state["turns"]=state.get("turns",0)+1

    mood=perceive(msg)
    mem=recall(user,msg)

    add(user,msg)

    return {
        "input":msg,
        "response":respond(msg,mem,mood),
        "mood":mood,
        "memory_hits":mem,
        "mode":"PHB_v9_OS"
    }
