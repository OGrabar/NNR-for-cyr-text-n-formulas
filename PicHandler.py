from PIL import Image, ImageFilter


Primitive = lambda size, image: image.convert('L').point(lambda a: 255 * (a > 230), mode='1').resize((size, size))


class PicHandler:

    def __init__(self, name):
        self.name = name
        self.image = Image.open(f'{self.name}.jpg')
        self.width, self.height = self.image.size


    def Alter(self, size):
        altered = self.image.filter(ImageFilter.GaussianBlur(10))
        self.image = Primitive(size, altered)
        self.width, self.height = self.image.size
        self.image.save(f'{self.name} altered.jpg')


    Show = lambda self: self.image.show()


    def BlocksOfPixels(self, side):

        block_amount = int(self.height / side)
        a = [[] * block_amount ** 2]

        if block_amount != self.height / side:
            raise Exception('blocks of a given size cannot be fully fit in the image')

        for s in range(block_amount):
            for k in range(block_amount):
                for i in range(side):
                    str = ''.join('10'[bool(self.image.getpixel((j + k * side, i + s * side)))] for j in range(side))
                    a[k + s * block_amount].append(str)

        return a


if __name__ == '__main__':
    pic = [PicHandler(f'{name}') for name in '0123456789']


    for p in pic:
        p.Alter(30)
        p.Show()
        a = p.BlocksOfPixels(30)
