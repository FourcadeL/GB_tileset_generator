# class object tile

from PIL import Image
import numpy as np

from exceptions import *

FLIP_EQUALITY = False # define if tile equality  must test for flip versions of the tile
TILE_SIZE = 8 # number of pixels by tiles (tiles are always squares)

class MetaTile:
    """Class for creation of meta-tiles
    - composed of multiple tiles mosaic
    - all made from the same palette
    - size must be a multiple of TILE_SIZE"""

    # Matrix of tiles
    tiles = None

    # Used palette
    palette = None

    def __init__(self, source_png, width=8, height=8):
        """initialize a meta-tile"""
        #TODO
        source_width, source_height = source_png.size
        for i in range(width//TILE_SIZE):
            for j in range(height//TILE_SIZE):
                colors = []
                #CREATE PALETTE from color list
                for k in range(TILE_SIZE):
                    for l in range(TILE_SIZE):
                        c = source_png.getpixel(i*TILE_SIZE + k, j*TILE_SIZE + l)
                #CREATE TILE FROM image and palette
        return





class Tile:
    """Class containing the data for a single unit tile
    (i.e. a square of size TILE_SIZE)"""
    # Matrix of indexed colors
    pixels = None

    # used palette for the tile
    palette = None


    def __init__(self, palette, data=None):
        self.palette = palette
        if data:
            if len(data) != TILE_SIZE*TILE_SIZE:
                raise DataException("Data should describe 8*8 pixels")
            palette_colors = self.palette.colors()
            for c in data:
                if not c in palette_colors:
                    raise DataException("Unmapped color in given data")
            pixels = np.array(data, np.int32)
            self.pixels = pixels.reshape(TILE_SIZE, TILE_SIZE)
        else:
            self.pixels = np.zeros((TILE_SIZE, TILE_SIZE), np.int32)
        return

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._equal_with_remapping(self.pixels, other.pixels)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def flip_h(self):
        self.pixels = np.flip(self.pixels, axis=1)
        return self

    def flip_v(self):
        self.pixels = np.flip(self.pixels, axis=0)
        return self

    def set_palette(self, palette):
        minindex, maxindex = self._palette_range()
        if len(palette.colors()) > maxindex + 1:
            print("can't change palette (correspondance too small)")
            return
        self.palette = palette

    def get_pixel(self, i, j):
        if (i >= TILE_SIZE or j >= TILE_SIZE):
            print("error - out of index")
        return self.palette.get_color(self.pixels[i][j])

    def show(self):
        ret = Image.new(mode="RGBA", size=(TILE_SIZE, TILE_SIZE))
        for i in range(TILE_SIZE):
            for j in range(TILE_SIZE):
                ret.putpixel((i, j), self.get_pixel(i, j).get_as_rgba())
        ret.show()

    ###### méthodes privées ######
    def _equal_with_remapping(self, pixels1, pixels2):
        """retourne true si les deux tableaux d'indexes sont les mêmes"""
        def test_equality(tab1, tab2):
            """iterate on all values of table to test if they are equal with remapping"""
            correspondance_mapping_recto = {} # c1 -> c2
            correspondance_mapping_verso = {} # c2 -> c1 (double dict for quick comparison)
            def handle_remapping(c1, c2):
                """if c1 == c2 in remapping, returne true
                else if c1 and c2 are not mapped add their mapping, return true
                else return false"""
                if (c1 in correspondance_mapping_recto) and (c2 in correspondance_mapping_verso):
                    return correspondance_mapping_recto[c1] == correspondance_mapping_verso[c2]
                if (not c1 in correspondance_mapping_recto) and (not c2 in correspondance_mapping_verso):
                    correspondance_mapping_recto[c1] = c2
                    correspondance_mapping_verso[c2] = c1
                    return True
                return False
            for i in range(TILE_SIZE):
                for j in range(TILE_SIZE):
                    if not handle_remapping(tab1[i][j], tab2[i][j]):
                        return False
            return True

        if FLIP_EQUALITY:
            return test_equality(pixels1, pixels2) or\
                test_equality(pixels1, np.flip(pixels2, axis=0)) or\
                test_equality(pixels1, np.flip(pixels2, axis=1)) or\
                test_equality(pixels1, np.flip(np.flip(pixels2, axis=0), axis=1))
        return test_equality(pixels1, pixels2)


    def _palette_range(self):
        """return the minimum and maximum indexes used by the tile"""
        minindex, maxindex = TILE_SIZE * TILE_SIZE, 0
        for i in range(TILE_SIZE):
            for j in range(TILE_SIZE):
                pix = self.pixels[i][j]
                if pix < minindex:
                    minindex = pix
                if pix > maxindex:
                    maxindex = pix
        return minindex, maxindex
    ##############################




class Palette:
    # dictionnaire des couleurs disponibles : int -> Color
    dict_colors = None

    def __init__(self):
        self.dict_colors = {}
        return

    def add_color(self, color):
        """adds a new color and return its index
        (if already in palette, return the index)"""
        for k, c in self.dict_colors.items():
            if c == color:
                return k
        key = len(self.dict_colors)
        self.dict_colors[key] = color
        return key

    def get_color(self, index):
        if index in self.dict_colors:
            return self.dict_colors[index]
        return None

    def colors(self):
        """return the list of available colors (indexes)"""
        return list(self.dict_colors.keys())


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            selfcolors = list(self.dict_colors.values())
            othercolors = list(self.dict_colors.values())
            if len(selfcolors) == len(othercolors):
                for e in selfcolors:
                    if not e in othercolors:
                        return False
                return True
            return False
        else:
            return False




class Color:
    r = None
    g = None
    b = None
    trans = None

    def __init__(self, tuple_rgba):
        self.r, self.g, self.b, tmp = tuple_rgba
        self.trans = (tmp < 255)
        return

    def get_as_rgba(self):
        return (self.r, self.g, self.b, 0 if self.trans else 255)

    def __eq__(self, other):
        """impléments member equality"""
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
        pa.add_color(Color((i, 2*i, 3, 255)))
    ti1 = Tile(pa, pa.colors())
    ti2 = Tile(pa, pa.colors())
    ti2.flip_h().flip_v()
    print(ti1 == ti2)
    print(ti1.get_pixel(3, 5).get_as_rgba())
    ti1.show()
    print("Done")
    return

if __name__ == "__main__":
    test()