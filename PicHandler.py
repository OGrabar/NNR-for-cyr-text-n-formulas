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