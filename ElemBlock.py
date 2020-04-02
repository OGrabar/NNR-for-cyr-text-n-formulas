class ElemBlock:

    def __init__(self, text, pos):
        self.text=text
        self.pos=pos

    def getOutput(self):
        return self.text

    def getPos(self):
        return self.pos

    def __repr__(self):
        return f'({self.text}, {self.pos})'