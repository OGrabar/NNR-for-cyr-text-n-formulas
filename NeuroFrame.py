from tkinter import *

class NeuroFrame(Frame):
    def __init__(self, parent, neuro):
        super().__init__(parent)
        self.neuro = neuro
        self.makeWidgets(neuro)

    def makeWidgets(self, neuro):
        fInfo = Frame(self)
        fInfo.pack(side=TOP)
        Label(fInfo, text="Информация о нейросети").pack(side=TOP)
        # элементы с информацией о структуре и результатах обучения нейросети


        fConfig = Frame(self)
        fConfig.pack(side=BOTTOM)
        Label(fConfig, text="Конфигурация нейросети")
        # инструменты для изменения конфигурации нейросети


        Button(fConfig, text="")


