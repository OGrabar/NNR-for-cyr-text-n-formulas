from operator import methodcaller
from typing import List

from ElemBlock import ElemBlock
from pylatex import Document, Package, NoEscape


class Translator:

    def __init__(self, blocks: List[ElemBlock]):
        self.text = ' '.join(map(methodcaller('getOutput'), sorted(blocks, key=lambda _:(_.getPos()[1],_.getPos()[0]))))


    def translate(self, filename: str):
        doc = Document('basic')

        doc.append(NoEscape(r'\noindent'))
        doc.append(self.text)
        babel = Package('babel', 'english, russian')
        fontenc = Package('fontenc', 'T2A')
        inputenc = Package('inputenc', 'utf8')
        doc.packages.items = [fontenc,  inputenc, babel]

        doc.generate_tex(filename)
        try:
            doc.generate_pdf(filename, clean_tex=False)
        except Exception as e:
            print(e)
