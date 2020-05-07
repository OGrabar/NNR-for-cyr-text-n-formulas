"""
Формула -- совокупность математических символов, составляющая единую семантическую единицу
Класс Formula используется для представления мат. формул; при вызове конструктора формируется tex-код,
соответствующий данной формуле
"""

from __future__ import annotations
from typing import *
from ElemBlock import ElemBlock


FRAC = '\\frac'

class Formula:
    texCode: str
    rank: int  # ранг (важность)
    center: Tuple[int, int]
    subformulas: Dict[Union[Formula.TOP, Formula.LOW], Formula] # пределы: верхний и нижний

    TOP = 'top'
    LOW = 'low'
    HAS_LIMITS = {'\\frac', '\\int', '\\sum'}
    INF = 9999
    CENTER_DY = 0.15
    NOSYMB = {'\\frac'}


    def __init__(self, elemBlocks: List[ElemBlock]):
        self.subformulas = dict()
        limits, elemBlocks = self.recognizeLimits(elemBlocks)
        self.recognize_structure(elemBlocks, limits)

    def recognizeLimits(self, elemBlocks: List[ElemBlock]) \
            -> Tuple[List[Tuple[ElemBlock, Dict[Union[Formula.TOP, Formula.LOW], List[ElemBlock]]]], List[ElemBlock]]:
        # данный метод выделяет все подформулы, которые являются пределами; возвращает список кортежей:
        # блок-родитель -- словарь с пределами;
        # а также список оставшихся elemBlock'ов

        done = set()
        res = []

        for block in elemBlocks:
            if Formula.hasLimits(block):
                topBlocks = Formula.findBlocks(block, elemBlocks, Formula.TOP)
                lowBlocks = Formula.findBlocks(block, elemBlocks, Formula.LOW)

                res.append(
                    (block, {Formula.TOP : topBlocks, Formula.LOW: lowBlocks})
                )

                [done.add(block) for block in (topBlocks + lowBlocks)]

        return res, [block for block in elemBlocks if block not in done]

    @staticmethod
    def hasLimits(block: ElemBlock) -> bool:
        # Возвращает True, если block содержит символ, имеющий верхний и нижний пределы, иначе False
        if block.getOutput() in Formula.HAS_LIMITS:
            return True
        else:
            return False

    @staticmethod
    def findBlocks(block: ElemBlock, elemBlocks: List[ElemBlock], side: Union[Formula.TOP, Formula.LOW]) \
             -> List[ElemBlock]:
        # возвращает список блоков из elemBlocks, находящихся в стороне side о block

        def findBorders(block: ElemBlock, elemBlocks: List[ElemBlock]) -> Tuple[int, int]:
            # функция находит левую и правую границы зоны, отводимой для записи пределов block
            limitBlocks = [b for b in elemBlocks if Formula.hasLimits(b) and b != block]
            left, right = 0, Formula.INF

            for b in limitBlocks:
                pos = b.getPos()
                if pos.left() > left:
                    left = pos.left()
                elif pos.right() < right:
                    right = pos.right()

            bl, br = block.getPos().left(), block.getPos().right()

            return bl - (bl - left) / 2, br + (right - br) / 2

        res = []
        if side == Formula.TOP:
            yLine = block.getPos().top()
        else:
            yLine = block.getPos().bottom()

        bl, br = findBorders(block, elemBlocks)
        for b in elemBlocks:
            if b != block and bl < b.getPos().left() and br > b.getPos().right():
                if Formula.inDirection(yLine, b, side):
                    res.append(b)

        return res

    @staticmethod
    def onLine(yLine: int, block: ElemBlock) -> bool:
        cy = block.getPos().center().y
        if abs(cy - yLine) / block.getPos().h < Formula.CENTER_DY:
            return True
        else:
            return False

    @staticmethod
    def inDirection(yLine: int, block: ElemBlock, side: Union[Formula.TOP, Formula.LOW]) -> bool:
        if side == Formula.TOP:
            if block.getPos().top() < yLine:
                return True
        else:
            if block.getPos().bottom() > yLine:
                return True

        return False

    @staticmethod
    def sortBlocks(elemBlocks: List[ElemBlock]) -> None:
        # сортирует список блоков (в порядке возрастания горизонтальной координаты)
        for i in range(len(elemBlocks)):
            for j in range(i + 1, len(elemBlocks) - 1):
                x1 = elemBlocks[i].getPos().center().x
                x2 = elemBlocks[j].getPos().center().x
                if x1 > x2:
                    elemBlocks[i], elemBlocks[j] = elemBlocks[j], elemBlocks[i]

    @staticmethod
    def findLimits(elemBlock: ElemBlock, limits: List) -> Dict:
        for b, d in limits:
            if b == elemBlock:
                return d

    @staticmethod
    def noSymb(string: str) -> bool:
        # Возвращает True, если данная команда Latex имеет пределы, передаваемые в аргументах {}{}
        if string in Formula.NOSYMB:
            return True
        else:
            return False

    @staticmethod
    def findDirection(yLine: int, second: ElemBlock) -> int:
        # 0 -- на одном уровне; 1 -- second - степень first; -1 -- second - индекс first
        y2 = second.getPos().center().y
        if Formula.onLine(yLine, second):
            return 0
        elif yLine < y2:
            return 1
        else:
            return -1

    def recognize_structure(self, elemBlocks: List[ElemBlock], limits: List[Tuple[ElemBlock, Dict]]) -> None:
        # метод создает tex-код для данной формулы
        Formula.sortBlocks(elemBlocks)
        self.texCode = ''
        yLine = elemBlocks[0].getPos().center().y

        #for i in range(len(elemBlocks)):
        #    block = elemBlocks[i]
        for block in elemBlocks:

            # добавление пределов для block (если они есть)
            if Formula.hasLimits(block):
                self.texCode += block.getOutput()
                lims = Formula.findLimits(block, limits)

                s = ''
                symb = not Formula.noSymb(block.getOutput())
                if symb:
                    s += '_'

                for lowBlock in lims[Formula.LOW]:
                    s += lowBlock.getOutput()
                self.texCode += '{%s}' % s

                s = ''
                if symb:
                    s += '^'

                for topBlock in lims[Formula.TOP]:
                    s += topBlock.getOutput()
                self.texCode += '{%s}' % s

            direct = Formula.findDirection(yLine, block)
            if direct == -1:
                # block -- индекс
                self.texCode += '_{%s}' % block.getOutput()
            elif direct == 1:
                # block -- степень
                self.texCode += '^{%s}' % block.getOutput()
            else:
                # block идет на одном уровне с предыдущим символом
                self.texCode += '{%s}' % block.getOutput()
                yLine = block.getPos().center().y

