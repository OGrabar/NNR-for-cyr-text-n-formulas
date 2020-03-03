import numpy as np
from PIL import Image, PngImagePlugin, JpegImagePlugin, BmpImagePlugin
import cv2
import os
from matplotlib import pyplot as plt
from pythreshold.utils import *
from typing import Tuple, Union
from functools import reduce


class PicHandler:

    def __init__(self, o : Union[str, np.ndarray, PngImagePlugin.PngImageFile, JpegImagePlugin.JpegImageFile, BmpImagePlugin.BmpImageFile], path='images/'):
        '''
        Creates a gray (white n black) image, based on 2-d np.ndarray.
        To specify the current directory, use path='.'

        :param o: object of either `str` or `np.ndarray`. `str` is the filename or the filename with extension
        :param path: `str`, optional. A path to the filename or to the filename with extension
        '''
        if isinstance(o, str):
            s = lambda a: a.split('.', 1)
            *a, = filter(lambda a: [s(a)[0]==s(o)[0], a==o][len(s(o))>1], {*os.listdir(path)})

            if len(a) > 1:
                raise ValueError(f'there are two or more files with such a name "{o}" in the directory "{path}" - '
                                'try to specify the extension of a file')
            elif not len(a):
                raise ValueError(f'there is no image "{o}" in the directory "{path}"')
            else:
                self.name = a[0]

            img = cv2.imread(f'{[path,""][path=="."]}{self.name}', cv2.IMREAD_UNCHANGED)
        elif isinstance(o, np.ndarray):
            self.name = '.'
            img = o
        else:
            self.name = o.filename
            img = np.array(o)

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                # *a, b = cv2.split(img)
                # self.img = reduce(cv2.add, (*a, cv2.bitwise_not(b)))
                *_, b = cv2.split(img)
                self.img = cv2.bitwise_not(b)
            else:
                self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif len(img.shape) == 2:
            self.img = img
        else:
            raise ValueError('the input data to be interpreted as an image has more then 3 dimensions')


    def resize(self, size: Union[int, Tuple[int,int]]) -> None:
        '''
        Resizes the 'self.img'. If the 'size' is `tuple`, nonproportial resize, if `int` - proportional
        :param size: (width `int`, height `int`) or `int`
        :return: None
        '''
        if isinstance(size, int):
            n, m = map(lambda a: int(size / max(self.img.shape) * a), self.img.shape)
            self.img = cv2.resize(self.img, (m, n), [cv2.INTER_AREA, cv2.INTER_CUBIC][(size, size) < self.img.shape])
            M = np.float32([[1, 0, ((size - m) // 2) * (m < size)], [0, 1, ((size - n) // 2) * (n < size)]])
            self.img = cv2.warpAffine(self.img, M, (size, size), borderValue=int(np.amax(self.img)))
        else:
            self.img = cv2.resize(self.img, size, [cv2.INTER_AREA, cv2.INTER_CUBIC][size < self.img.shape])


    def alter(self):
        '''
        Applies filter on the 'self.img'
        :return: None
        '''
        kernel = np.ones((3, 3), np.uint8)
        self.img = apply_threshold(self.img,bradley_roth_threshold(self.img))
        self.img = cv2.erode(self.img, kernel, iterations=2)


    ''' Opens the image window. Closed by pressing any button '''
    _show = lambda self,n=None,i=None: [cv2.imshow(['_',self.name][n is None],[i,self.img][i is None]),cv2.waitKey(0),cv2.destroyAllWindows()]


    def blocksOfPixels(self, mode:Union[str,int]=None) -> np.ndarray:
        '''
        Returns the image as matrix.
        :param mode: `str` or `int`. To change the value of white color (255 to mode)
        :return: `np.dnarray`
        '''
        if mode:
            try:
                mode = int(mode)
            except (ValueError, TypeError):
                raise Exception(f'"{mode}" cannot be converted to int')
            return np.vectorize(lambda _: min(_, mode))(self.img)
        return self.img


    ''' Returns the image as a vector `np.array` '''
    vectorOfPixels = lambda self, mode=None: self.blocksOfPixels(mode).flatten()