import numpy as np

spinner = ['-', '/', '|', '\\']

def evaluate(sup, que):
    if len(sup) == 0 or len(que) == 0:
        return 0
    
    for v in sup:
        if v in que:
            return 1
    return 0

def sigmoid(z):
    result = 1.0 / (1.0 + np.exp(-z))
    result = np.clip(result, 1e-8, 1-(1e-8))
    return result
