from __future__ import annotations
from typing import *
from itertools import *
import numpy as np
from math import sqrt

class Framer:
    INF = 9999999
    SIZE = 30

    @staticmethod
    def getPosById(id: int, matrixSize: int) -> Tuple[int, int]:
        # первая координата -- номер строки, вторая -- номер столбца

        x = id // matrixSize
        y = id - matrixSize * x
        return x, y

    @staticmethod
    def getIdByPos(pos: Tuple[int, int], matrixSize: int) -> int:
        return pos[0] * matrixSize + pos[1]

    @staticmethod
    def compare_graphs(first: np.ndarray, second: np.ndarray) -> List[Tuple[int], Tuple[int]]:
        # возвращает список кортежей -- перестановок строк и столбцов, которые позволяют привести first к second
        if first.shape != second.shape:
            raise Exception("Matrix shapes!")

        res = []

        for h_perm in permutations(range(len(first)), len(first)):
            v_perm = h_perm
            matrix = first[h_perm, :][:, v_perm]
            if matrix == second:
                res.append(h_perm)

        return res

    @staticmethod
    def distance(p1: int, p2: int, matrixSize: int) -> float:
        pos1, pos2 = Framer.getPosById(p1, matrixSize), Framer.getPosById(p2, matrixSize)
        dx, dy = pos1[0] - pos2[0], pos1[1] - pos2[1]
        return sqrt(dx*dx + dy*dy)

    @staticmethod
    def getIsomorphic(v: int, perm: Tuple[int]) -> int:
        return perm.index(v)

    @staticmethod
    def delSS(matrix: np.ndarray, ss: List[int]) -> np.ndarray:
        # вычеркивает из матрицы столбцы и строки из ss
        dx = np.delete(matrix, ss, 0)
        return np.delete(dx, ss, 1)

    @staticmethod
    def compare(first: np.ndarray, first_nums: List[int], second: np.ndarray, second_nums: List[int],
                enclosed_vertexes1: List[int] =list(), enclosed_vertexes2: List[int] =list(), size: int = Framer.SIZE) \
            -> float:
        # метод сравнивает скелеты символов и возвращает коэффициент различия -- неотрицательное число
        # кол-во вершин в скелетах должно быть одинаковым
        # enclosed_vertexes -- номера вершин, которые игнорируются при сравнении
        if first.shape != second.shape:
            raise Exception("Matrix shapes!")

        def resizeSkeleton(nums: List[int], size: int, sizeX: int, sizeY: int) -> List[int]:
            # данный метод растягивает скелет символа по вертикали и горизонтали (вписывая в квадрат sizeXx * sizeY)
            # size -- размер поля, в котором зашифрованы позиции пикселей с помощью nums
            positions = [Framer.getPosById(num, size) for num in nums]
            max_x, max_y = 0, 0
            for x, y in positions:
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

            kx, ky = sizeX / max_x, sizeY / max_y
            for i in range(len(positions)):
                x, y = positions[i]
                x *= kx
                y *= ky
                positions[i] = (x, y)

            return [Framer.getIdByPos(pos, size) for pos in positions]


        m1, m2 = Framer.delSS(first, enclosed_vertexes1), Framer.delSS(second, enclosed_vertexes2)
        nums1, nums2 = resizeSkeleton(first_nums, size, size, size), \
                       resizeSkeleton(second_nums, size, size, size)
        perms = Framer.compare_graphs(m1, m2)
        if len(perms) == 0:
            return Framer.INF

        else:
            results: List[float] = []
            for perm in perms:
                results.append(0)
                # очередь из непройденных вершин: состоит только из вершин из разомкнутой части символа
                queue = {v for v in range(len(m1))}
                done = set() # пройденные вершины

                while len(queue):
                    act1 = queue.pop()
                    act2 = Framer.getIsomorphic(act1, perm)
                    results[-1] += Framer.distance(nums1[act1], nums2[act2], size)
                    done.add(act1)

            return min(results)
