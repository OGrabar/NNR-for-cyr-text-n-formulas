from operator import methodcaller
from typing import List

from ElemBlock import ElemBlock
from pylatex import Document, Package, NoEscape, Math


class Translator:

    def __init__(self, blocks: List[ElemBlock]):
        self.blocks = sorted(blocks, key=lambda _:_.getPos()[::-1])


    def translate(self, filename: str):
        doc = Document('basic')

        doc.append(NoEscape(r'\noindent'))

        for block in self.blocks:
            doc.append([Math(data=[NoEscape(out:=block.getOutput())], inline=True), out]['\\' not in out])

        babel = Package('babel', 'english, russian')
        fontenc = Package('fontenc', 'T2A')
        inputenc = Package('inputenc', 'utf8')
        doc.packages.items = [fontenc,  inputenc, babel]

        doc.generate_tex(filename)
        try:
            doc.generate_pdf(filename, clean_tex=False)
        except Exception as e:
            print(e)
