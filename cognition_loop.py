from memory_core import add, search

def think(msg,user_id,state):

    state["turns"]=state.get("turns",0)+1

    mood="neutral"
    if any(x in msg.lower() for x in ["tired","sad","overwhelmed"]):
        mood="soft"

    mem=search(user_id,msg)

    if mem:
        response="I remember you. You're not alone."
    else:
        response="I'm here with you."

    add(user_id,msg)

    return {
        "input":msg,
        "response":response,
        "mood":mood,
        "memory_hits":mem,
        "mode":"PHB_v8_PATCHED"
    }
