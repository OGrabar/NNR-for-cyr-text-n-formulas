from tkinter import *

class InfLabel(Frame):
    def __init__(self, parent=None, height=4):
        Frame.__init__(self, parent)
        lab = Label(self, height=height)
        lab.pack()
        self.lab = lab
        self.counter = 0
        self.text = ""

    def delStr(self, msec):
        end = self.text.find("\n")
        self.text = self.text[end+1:]
        self.lab.configure(text=self.text)
        self.counter -= msec

    def print(self, text="", msec = 3000):
        if text != "":
            self.text += text + "\n"
            self.lab.configure(text=self.text)
            self.after(msec + self.counter, lambda: self.delStr(msec))
            self.counter += msec
