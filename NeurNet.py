from __future__ import annotations
import numpy as np
from typing import *
import saving
import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import ReluLayer
from pybrain.structure import SigmoidLayer
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


RELU, SIGMOID, TANH = 'relu', 'sigmoid', 'tanh'

class NeurNet:
    nn: pybrain.Network
    ds: SupervisedDataSet
    trainer: BackpropTrainer

    def __init__(self, layers: Tuple[int,], func: Union[RELU, SIGMOID, TANH] =SIGMOID, learning_rate: float =0.01):
        if func == RELU:
            hc = ReluLayer
        elif func == SIGMOID:
            hc = SigmoidLayer
        elif func == TANH:
            hc = TanhLayer
        else:
            raise Exception("Invalid func param")
        self.nn = buildNetwork(*layers, hiddenclass=hc, )
        self.ds = SupervisedDataSet(layers[0], layers[-1])
        self.trainer = BackpropTrainer(self.nn, self.ds, learningrate=learning_rate)

    def signal(self, ins: np.ndarray) -> np.ndarray:
        return self.nn.activate(ins)

    def addSample(self, ins: np.ndarray, outs: np.ndarray) -> None:
        self.ds.addSample(ins, outs)

    def train(self, epoch: int=1) -> float:
        # возвращает значение квадратичной ошибки на последней эпохе
        for i in range(epoch - 1):
            self.trainer.train()
        return self.trainer.train()

    def save(self, filename: str = 'default'):
        t = self.ds
        f, l = self.nn.indim, self.nn.outdim
        self.ds = SupervisedDataSet(f, l)
        saving.saveObj(self, filename + '.nn')
        self.ds = t

    def load(self, filename: str = 'default'):
        other = saving.loadObj(filename + '.nn')
        f, l = other.nn.indim, other.nn.outdim
        self.nn, self.ds, self.trainer = other.nn, other.ds, other.trainer
