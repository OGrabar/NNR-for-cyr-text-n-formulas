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



if __name__ == '__main__':

    # elems = [ElemBlock(chr(1072+i), (i,2))for i in range(32)]
    # e = [ElemBlock(chr(65+i), (46-i,1))for i in range(32)]
    # Translator(elems+e).translate('yay')
    Translator([ElemBlock('a', (0,0)), ElemBlock(r'\frac{5}{4}', (0,1)), ElemBlock('b', (0,2))]).translate('f')
