import os

from Parser import Parser
from Recognizer import Recognizer
from Translator import Translator
from Formula import Formula
from createNeurNet import createNeurNet


class Reader:

    def __init__(self, filename: str, path='images/'):
        s = lambda a: a.split('.', 1)
        *a, = filter(lambda a: [s(a)[0] == s(filename)[0], a == filename][len(s(filename)) > 1], {*os.listdir(path)})

        if len(a) > 1:
            raise ValueError(f'there are two or more files with such a name "{filename}" in the directory "{path}" - '
                             'try to specify the extension of a file')
        elif not len(a):
            raise ValueError(f'there is no image "{filename}" in the directory "{path}"')
        else:
            self.name = a[0]


    def read(self):
        p = Parser(self.name)                                # how to interact with Parser?
        t, *text_blocks = p.getTextBlocks()         # ?
        formula_blocks = p.getFormulaBlocks()       # ?
        re = Recognizer(t, createNeurNet())

        recognized = [re.rec()]
        for i in text_blocks:
            re.setBlock(i)
            recognized.append(re.rec())
        recognized += [Formula(i).getFormula() for i in formula_blocks]

        t = Translator(recognized)
        t.translate(self.name.split('.')[0])
