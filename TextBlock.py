from PicHandler import PicHandler
import numpy as np

from Position import *

class TextBlock:

    def __init__ (self, position:Position, pic_handler:PicHandler):
        self.position = position
        self.pic_handler = pic_handler

    def getPos(self) -> Position:
        return self.position

    def getImg(self) -> PicHandler:
        """
        Мб потребует правок
        """
        #FixMe
        pos = self.position
        box = (pos.x, pos.y, pos.x + pos.width, pos.y - pos.height)
        return PicHandler(np.array(self.pic_handler.img.crop(box)))
