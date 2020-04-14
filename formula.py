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
    HAS_LIMITS = {'frac', 'int', 'sum'}
    INF = 9999
    CENTER_DY = 0.15


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

    def recognize_structure(self, elemBlocks: List[ElemBlock], limits: List[Tuple[ElemBlock, Dict]]) -> None:
        # метод создает tex-код для данной формулы
        Formula.sortBlocks(elemBlocks)
        self.texCode = ''

        for block in elemBlocks:
            self.texCode += block.getOutput()
            if Formula.hasLimits(block):
                lims = Formula.findLimits(block, limits)

                s = ''
                if block.getOutput() != FRAC:
                    s += '_'

                for lowBlock in lims[Formula.LOW]:
                    s += lowBlock.getOutput()
                self.texCode += '{%s}' % s

                s = ''
                if block.getOutput() != FRAC:
                    s += '^'

                for topBlock in lims[Formula.TOP]:
                    s += topBlock.getOutput()
                self.texCode += '{%s}' % s
