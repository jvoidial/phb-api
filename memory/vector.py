def vectorize(text):
    vec = {}
    for w in text.lower().split():
        vec[w] = vec.get(w, 0) + 1
    return vec


def similarity(a, b):
    keys = set(a) | set(b)
    return sum(a.get(k, 0) * b.get(k, 0) for k in keys)
