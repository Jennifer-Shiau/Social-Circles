spinner = ['-', '/', '|', '\\']

def evaluate(sup, que):
    if len(sup) == 0 or len(que) == 0:
        return 0
    
    for v in sup:
        if v in que:
            return 1
    return 0
