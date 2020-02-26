from NeurNet import *

def createNeurNet():
    #lay1 = Layer(5, 20)
    #lay2 = Layer(20, 10)
    #lay3 = Layer(10, 5)

    nIns = 900
    nOuts = 10

    block = Block((nIns, 1000, nOuts))
    nn = NeurNet(block, block)

    return nn