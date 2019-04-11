from tkinter import *
from tkinter.filedialog import *
from PIL import Image as IMG
from InfLabel import *
import io
import threading as th

IMGDIRECTORY = ""
FORMAT = 'png'


class CanvasDraw(Frame):
    IMGCOUNTER = 0
    DWIDTH, DHEIGHT = 500, 500
    DIAM_POINT = 20
    K = 50 # На DIAM_POINT пикселей приходится K точек

    def __init__(self, parent=None, color='white'):
        Frame.__init__(self, parent)
        self.start = None
        self.makeWidgets(color)

    def makeWidgets(self, color):
        #self.pack(expand=YES, fill=BOTH)

        canv = Canvas(self, width = CanvasDraw.DWIDTH,
                      height = CanvasDraw.DHEIGHT, bg=color)
        canv.pack(expand=YES, fill=BOTH)

        canv.bind('<ButtonPress-1>', self.onClick)
        canv.bind('<B1-Motion>', self.onMove)
        canv.bind('<B1-ButtonRelease>', self.onRelease)

        self.canv = canv

        Label(self, height=1).pack() # отступить вниз


        toolbar = Frame(self)
        toolbar.pack()
        self.toolbar = toolbar

        bttnClear = Button(toolbar, text = 'Очистить полотно',
                           command = self.clear)
        bttnSave = Button(toolbar, text = 'Сохранить изображение',
                          command = self.imgReady)
        bttnSignal = Button(toolbar, text = 'Отправить сигнал нейросети',
                            command = self.signal)

        self.bttnClear = bttnClear
        self.bttnSave = bttnSave
        self.bttnSignal = bttnSignal

        bttnClear.pack(side=LEFT)
        bttnSave.pack(side = LEFT)
        bttnSignal.pack(side=LEFT)

        inf = InfLabel(self)#Label(self, height=2)
        self.inf = inf
        inf.pack()

    def onClick(self, event):
        self.start = (event.x, event.y)
        self.drawPoint(event.x, event.y)

    def onMove(self, event):
        self.drawPoint(event.x, event.y)
        x0, y0 = self.start[0], self.start[1]

        self.addPoints(x0, y0, event.x, event.y)

        self.start = (event.x, event.y)

    def onRelease(self, event):
        self.start = None

    def drawPoint(self, x, y, color = 'black'):
        x1 = x - CanvasDraw.DIAM_POINT/2
        x2 = x + CanvasDraw.DIAM_POINT / 2
        y1 = y - CanvasDraw.DIAM_POINT / 2
        y2 = y + CanvasDraw.DIAM_POINT / 2
        self.canv.create_oval(x1, y1, x2, y2, fill=color)

    def addPoints(self, x1, y1, x2, y2):
        self.canv.create_line(x1, y1, x2, y2, width = CanvasDraw.DIAM_POINT)

    def saveImg(self, filename, format='png'):
        CanvasDraw.IMGCOUNTER += 1

        ps = self.canv.postscript(colormode='color')

        img = IMG.open(io.BytesIO(ps.encode('utf-8')))
        img.save(filename + '.' + format)

        self.after(1, lambda: self.print("Изображение сохранено как: " + \
                   filename + '.' + format))

    def imgReady(self):
        filename = str(CanvasDraw.IMGCOUNTER)
        t = th.Thread(target=self.saveImg, args=(filename, FORMAT))
        t.start()

    def clear(self):
        self.canv.delete(ALL)
        self.print("Полотно очищено")

    def print(self, text=''):
        self.inf.print(text)
        """
        #self.inf.update_idletasks()
        self.inf.after_cancel(ALL)
        self.inf.configure(text=text)

        self.inf.after(4000, lambda : self.inf.configure(text=''))"""

    def signal(self):
        # Будет раелизовано позже
        # <...>
        # signal = PrimitiveImage(<params>)
        # self.output.turn(signal)
        #self.neuro.signal()
        self.print("Сигнал отправлен")

if __name__ == '__main__':
    c = CanvasDraw()
    c.pack()
    c.mainloop()
