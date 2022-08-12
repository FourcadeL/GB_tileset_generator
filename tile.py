# class object tile

from PIL import Image
import numpy as np

from exceptions import *

# define if tile equality  must test for flip versions of the tile
FLIP_EQUALITY = True

class Tile:
    # Matrix of indexed colors
    pixels = None

    # used palette for the tile
    palette = None


    def __init__(self, palette, data=None):
        self.palette = palette
        if data:
            if len(data) != 8*8:
                raise DataException("Data should describe 8*8 pixels")
            palette_colors = self.palette.colors()
            for c in data:
                if not c in palette_colors:
                    raise DataException("Unmapped color in given data")
            pixels = np.array(data, np.int32)
            self.pixels = pixels.reshape(8, 8)
        else:
            self.pixels = np.zeros((8, 8), np.int32)
        return

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # TODO : test for palette, array values and flip
            return self.__dict__ == other.__dict__
        else:
            return False

    def flip_h(self):
        self.pixels = np.flip(self.pixels, axis=1)
        return

    def flip_v(self):
        self.pixels = np.flip(self.pixels, axis=0)
        return






class Palette:
    # dictionnaire des couleurs disponibles : int -> Color
    dict_colors = None

    def __init__(self):
        self.dict_colors = {}
        return

    # adds a new color and return its index
    # (if already in palette, return the index)
    def add_color(self, color):
        for k, c in self.dict_colors.items():
            if c == color:
                return k
        key = len(self.dict_colors)
        self.dict_colors[key] = color
        return key

    # return the list of available colors (indexes)
    def colors(self):
        return list(self.dict_colors.keys())


class Color:
    r = None
    g = None
    b = None
    trans = None

    def __init__(self, tuple_rgba):
        self.r, self.g, self.b, tmp = tuple_rgba
        self.trans = (tmp < 255)
        return

    # impléments member equality
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)



def test():
    im = Image.open("test_logo.png")
    im = im.convert("RGBA")
    print("testing")
    pa = Palette()
    for i in range(8*8):
        pa.add_color(Color((i, 2*i, 3, 4)))
    ti = Tile(pa, pa.colors())
    print("Done")
    return

if __name__ == "__main__":
    test()