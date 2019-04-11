import numpy as np
from math import *

def sigmoid(x):
    return 1/(1+e**(-x))

class Layer:
    def __init__(self, ins, outs, weights, func = sigmoid):
        if weights.shape != (outs, ins):
            raise Exception("Матрица весов")
        self.nIns = ins
        self.nOuts = outs
        self.weights = weights
        self.func = func

    def signal(self, ins):
        if len(ins) != self.nIns:
            raise Exception("Количество входов")
        res = self.weights @ ins

        for i in res:
            res[i] = self.func(res[i])

        return res
