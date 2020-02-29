from tkinter import *
from InfLabel import *
from NeurNet import *

class NeuroFrame(Frame):
    RESUME = "Продолжить обучение"
    STOP = "Остановить обучение"
    def __init__(self, parent, neuro):
        super().__init__(parent)
        self.neuro = neuro
        self.stoped = False
        self.makeWidgets(neuro)

    def makeWidgets(self, neuro: NeurNet):
        fInfo = Frame(self)
        fInfo.pack(side=BOTTOM)
        Label(fInfo, text="Информация о нейросети").pack(side=TOP)
        # элементы с информацией о структуре и результатах обучения нейросети
        txt: str = ''
        for lay in neuro.first.layers:
            txt += str(lay.weights)
            txt += '\n'

        #Label(fInfo, text="Матрица весов:\n" + txt).pack()


        fConfig = Frame(self)
        fConfig.pack()
        Label(fConfig, text="Конфигурация нейросети").pack(side=TOP)
        # инструменты для изменения конфигурации нейросети


        Button(fConfig, text="Начать обучение", command=self.begin).pack()
        self.bttnStopRes = Button(fConfig, text=NeuroFrame.RESUME,
               command=self.stopResume)
        self.bttnStopRes.pack()

        self.inf = InfLabel(self)
        self.inf.pack(side=BOTTOM)
        self.print = self.inf.print

    def begin(self):
        self.print("Начало обучения нейросети")
        #self.neuro.begin()
        self.bttnStopRes.configure(text=NeuroFrame.STOP)

    def stopResume(self):
        if self.stoped:
            text = "Обучение нейросети продолжено"
            self.bttnStopRes.configure(text=NeuroFrame.STOP)

        else:
            text = "Обучение нейросети простановлено"
            self.bttnStopRes.configure(text=NeuroFrame.RESUME)

        self.stoped = not self.stoped

        self.print(text)
        self.neuro.stopRes()


