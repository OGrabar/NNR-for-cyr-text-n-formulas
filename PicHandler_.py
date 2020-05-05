import numpy as np
from PIL import PngImagePlugin, JpegImagePlugin, BmpImagePlugin
import cv2
import os
from pythreshold.utils import *
from typing import Tuple, Union


class PicHandler:
    name = '_'

    def __init__(self, o: Union[
        str, np.ndarray, PngImagePlugin.PngImageFile, JpegImagePlugin.JpegImageFile, BmpImagePlugin.BmpImageFile],
                 path='images/'):
        '''
        Creates a gray (white n black) image, based on 2-d np.ndarray.
        To specify the current directory, use path='.'

        :param o: object of either `str` or `np.ndarray`. `str` is the filename or the filename with extension
        :param path: `str`, optional. A path to the filename or to the filename with extension
        '''
        if isinstance(o, str):
            s = lambda a: a.split('.', 1)
            *a, = filter(lambda a: [s(a)[0] == s(o)[0], a == o][len(s(o)) > 1], {*os.listdir(path)})

            if len(a) > 1:
                raise ValueError(f'there are two or more files with such a name "{o}" in the directory "{path}" - '
                                 'try to specify the extension of a file')
            elif not len(a):
                raise ValueError(f'there is no image "{o}" in the directory "{path}"')
            else:
                self.name = a[0]

            img = cv2.imread(f'{[path,""][path=="."]}{self.name}', cv2.IMREAD_UNCHANGED)

        elif isinstance(o, np.ndarray):
            self.name = '_'
            img = o
        else:
            self.name = o.filename
            img = np.array(o)

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                *_, b = cv2.split(img)
                self.img = [cv2.bitwise_not(b), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)][int(np.amax(b)) == int(np.amin(b))]
            else:
                self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif len(img.shape) == 2:
            self.img = img
        else:
            raise ValueError('the input data to be interpreted as an image has more then 3 dimensions')


    def __resize(self, size: Union[int, Tuple[int, int]], img) -> np.ndarray:
        '''
        Resizes the 'self.img'. If the 'size' is `tuple`, nonproportial resize, if `int` - proportional
        :param size: (width `int`, height `int`) or `int`
        :param img: `np.ndarray`. an image to be resized
        :return: PicHandler
        '''
        if isinstance(size, int):
            n, m = map(lambda a: int(size / max(img.shape) * a), img.shape)
            img = cv2.resize(img, (m, n), [cv2.INTER_AREA, cv2.INTER_CUBIC][(size, size) < img.shape])
            M = np.float32([[1, 0, ((size - m) // 2) * (m < size)], [0, 1, ((size - n) // 2) * (n < size)]])
            img = cv2.warpAffine(img, M, (size, size), borderValue=int(np.amax(img)))
        else:
            img = cv2.resize(img, size, [cv2.INTER_AREA, cv2.INTER_CUBIC][size < img.shape])

        return img


    def resize(self, size: Tuple[int,int]) -> None:
        '''
        Resizes the image according to passed 'size'
        :param size: (width, height)
        :return: None
        '''
        self.img = cv2.resize(self.img, size, [cv2.INTER_AREA, cv2.INTER_CUBIC][size < self.img.shape])


    def alter(self) -> 'PicHandler':
        '''
        Applies filter on the 'self.img'
        :return: `PicHandler`. To give the ability to apply several methods at once, i.e. PicHandler(pic).alter().resize((30,30))
        '''
        self.img = apply_threshold(self.img, bradley_roth_threshold(self.img))
        return self


    ''' Opens the image window. Closed by pressing any button '''
    _show = lambda self, n=None, i=None: [cv2.imshow(['_', self.name][n is None], [i, self.img][i is None]),
                                          cv2.waitKey(0), cv2.destroyAllWindows()]


    def blocksOfPixels(self, square: bool=False, resize: bool=False) -> np.ndarray:
        '''
        Returns the image as `np.ndarray`. !!Doesn't alter self.img!!
        :param square: bool, default=False. Fills the min dimension of the image with vectors of zeros (white)
        :param resize: bool, default=False. Proportionally changes size of the image to (standard, standard).
        If any of the shape components of the resized images is less then standard, it is filled with vectors of zeros (white)
        :return: np.ndarray
        '''
        arr = np.copy(self.img)
        size = square*max(arr.shape) and resize*30
        if size:
            arr = self.__resize(size, arr)
        return np.vectorize(lambda _: min(_, 1))(cv2.bitwise_not(arr))


    '''returns vector of the image `np.ndarray`'''
    vectorOfPixels = lambda self: self.blocksOfPixels().flatten()


    '''thinning the line of the image using Zhang-Suen algorithm
    Operates on a copy, not on the internal image
    
    :return: `np.ndarray` of [0, 1]
    '''
    thinning = lambda self: cv2.ximgproc.thinning(cv2.bitwise_not(self.img.copy()))


    # neighbourhood = lambda self, i, j, img: [img[i-1,j],img[i-1,j+1],img[i,j+1],img[i+1,j+1],img[i+1,j],img[i+1,j-1],img[i][j-1],img[i-1][j-1]]
    #
    # def __transitions(self, i, j,img):
    #     #near=[img[i,j-1],img[i,j+1],img[i-1,j],img[i+1,j],img[i-1,j-1],img[i-1,j+1],img[i+1][j-1],img[i+1][j+1]]
    #     n = self.neighbourhood(i, j, img)
    #     return sum((a,b)==(0,1) for a,b in zip((n, n[1:])))
    #
    # # def __black_supremacy(self, i, j,img):
    # #     return img[i,j-1]+img[i,j+1]+img[i-1,j]+img[i+1,j]+img[i-1,j-1]+img[i-1,j+1]+img[i+1][j-1]+img[i+1][j+1]
    #
    #
    #
    # def thinning(self):
    #
    #     self._show()
    #     thin = np.vectorize(lambda _: [1,0][_>255//2])(self.img)
    #     h,w = self.img.shape
    #     flag = True
    #
    #     while flag:
    #
    #         flag = False
    #         for it in (0,1):
    #             cells=set()
    #             for i in range(1, h-1):
    #                 for j in range(1, w-1):
    #                     P2,P3,P4,P5,P6,P7,P8,P9 = n = self.neighbourhood(i, j, thin)
    #                     if thin[i,j] and 2<=sum(n)<=6 and sum((a,b)==(0,1) for a, b in zip(n, n[1:]))==1 and \
    #                     eval(f'P2*P4*P{6+2*it}==0') and eval(f'P{4-2*it}*P6*P8==0'):
    #                         cells.add((i,j))
    #             if cells:
    #                 flag = True
    #                 while cells:
    #                     thin[cells.pop()]=0
    #
            #
            # cells_.clear()
            #
            # for i in range(1, h-1):
            #     for j in range(1, w-1):
            #         P2,P3,P4,P5,P6,P7,P8,P9 = n = self.neighbourhood(i, j, thin)
            #         if thin[i,j] and 2<=sum(n)<=6 and sum((a,b)==(0,1) for a, b in zip(n, n[1:]))==1 and \
            #         P2*P4*P8==0 and P2*P6*P8==0:
            #             cells_.append((i,j))
            #
            # for cell in cells_:
            #     thin[cell]=0
            #

    #     return np.vectorize(lambda _:[0,255][_])(thin).astype(np.uint8)
    #
    #
    # def neighbours(self,x,y, image):
    #     "Return 8-neighbours of image point P1(x,y), in a clockwise order"
    #     img = image
    #     x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1
    #     return [ img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],     # P2,P3,P4,P5
    #                 img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1] ]    # P6,P7,P8,P9
    #
    # def transitions(self,neighbours):
    #     "No. of 0,1 patterns (transitions from 0 to 1) in the ordered sequence"
    #     n = neighbours + neighbours[0:1]      # P2, P3, ... , P8, P9, P2
    #     return sum( (n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]) )  # (P2,P3), (P3,P4), ... , (P8,P9), (P9,P2)
    #
    # def zhangSuen(self):
    #     "the Zhang-Suen Thinning Algorithm"
    #     Image_Thinned = cv2.bitwise_not(self.img.copy())  # deepcopy to protect the original image
    #     changing1 = changing2 = 1        #  the points to be removed (set as 0)
    #     while changing1 or changing2:   #  iterates until no further changes occur in the image
    #         # Step 1
    #         changing1 = []
    #         rows, columns = Image_Thinned.shape               # x for rows, y for columns
    #         for x in range(1, rows - 1):                     # No. of  rows
    #             for y in range(1, columns - 1):            # No. of columns
    #                 P2,P3,P4,P5,P6,P7,P8,P9 = n = self.neighbours(x, y, Image_Thinned)
    #                 if (Image_Thinned[x][y] == 1     and    # Condition 0: Point P1 in the object regions
    #                     2 <= sum(n) <= 6   and    # Condition 1: 2<= N(P1) <= 6
    #                     self.transitions(n) == 1 and    # Condition 2: S(P1)=1
    #                     P2 * P4 * P6 == 0  and    # Condition 3
    #                     P4 * P6 * P8 == 0):         # Condition 4
    #                     changing1.append((x,y))
    #         for x, y in changing1:
    #             Image_Thinned[x][y] = 0
    #         # Step 2
    #         changing2 = []
    #         for x in range(1, rows - 1):
    #             for y in range(1, columns - 1):
    #                 P2,P3,P4,P5,P6,P7,P8,P9 = n = self.neighbours(x, y, Image_Thinned)
    #                 if (Image_Thinned[x][y] == 1   and        # Condition 0
    #                     2 <= sum(n) <= 6  and       # Condition 1
    #                     self.transitions(n) == 1 and      # Condition 2
    #                     P2 * P4 * P8 == 0 and       # Condition 3
    #                     P2 * P6 * P8 == 0):            # Condition 4
    #                     changing2.append((x,y))
    #         for x, y in changing2:
    #             Image_Thinned[x][y] = 0
    #     return Image_Thinned

if __name__ == '__main__':

    c=PicHandler('0.jpg')
    cv2.imshow('n', c.img)
    cv2.imshow('i', cv2.bitwise_not(c.img))
    cv2.imshow('t', c.thinning())
    a = c.thinning()
    b = cv2.bitwise_not(c.thinning()).astype(np.uint8)
    cv2.imshow('in', b)
    # c._show()
    # c.resize(tuple(map(lambda _:_//2,c.img.shape)))
    # a=c.thinning()
    # b = cv2.ximgproc.thinning(c.img, thinningType=1)
    # c = cv2.ximgproc.thinning(c.img, thinningType=0)
    # #b=cv2.ximgproc.thinning(cv2.bitwise_not(c.img), thinningType=1)
    # #c = cv2.ximgproc.thinning(cv2.bitwise_not(c.img), thinningType=0)
    # cv2.imshow('thinning',a)
    # cv2.imshow('thinned', b)
    # cv2.imshow('thinned another', c)
    #c.zhangSuen()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
