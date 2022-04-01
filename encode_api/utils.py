def match(subject, query):
    for k, v in query.items():
        if subject.get(k, None) != v:
            return False
    else:
        return True


def select(d, q):
    return {k: d.get(k, None) for k in q}


def filter(ds, q):
    return [d for d in ds if match(d, q)]

