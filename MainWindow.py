from CanvasDraw import *
from tkinter import *
from NeuroFrame import *
from NeurNet import *


class Main(Tk):
    def __init__(self, neuro = NeurNet()):
        super().__init__()
        self.neuro = neuro
        self.makeWidgets(neuro)

    def makeWidgets(self, neuro):
        self.mainFrame = Frame(self)
        self.mainFrame.pack()
        self.canv = CanvasDraw(self.mainFrame)
        self.canv.pack(side=LEFT)

        Label(self.mainFrame, width=2).pack(side=LEFT) # отступить немного вправо
        self.neuroFrame = NeuroFrame(self.mainFrame, self.neuro)
        self.neuroFrame.pack(side=RIGHT)







if __name__ == '__main__':
    Main().mainloop()
