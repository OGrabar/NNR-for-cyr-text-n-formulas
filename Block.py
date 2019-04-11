from Layer import *


class Block:
    def __init__(self, network, isFirst=True, prevBlocks=None, n=2, nns=(1, 2)):
        # n -- кол-во слоев + 1,
        # nns -- кол-во нейронов в каждом слое, первый элемент -- кол-во входов,
        # последний -- кол-во выходов
        self.layers = [Layer(  nns[i], nns[i+1],
                              np.random.randint( -1, 1, (nns[i+1], nns[i]) )  )
                       for i in range(n-1)]

        self.isFirst = isFirst
        self.prevBlocks = prevBlocks
        self.n = n-1

        self.network = network

        self.nIns = self.layers[0].nIns
        self.nOuts = self.layers[n-1].nOuts

    def signal(self, ins):
        res = ins
        for i in range(self.n):
            res = self.layers[i].signal(res)

        return res

    def getOuts(self): # получить сигнал от предыдущих блоков и обработать
        if not self.isFirst:
            ins = np.zeros(self.nIns)
            for prev in self.prevBlocks:
                ins += prev.getOuts()

        else:
            ins = self.network.getIns()

        return self.signal(ins)