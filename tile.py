# class object tile

from PIL import Image


class Tile:
    def __init__(self, palette):
        self.palette = palette
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
    return

if __name__ == "__main__":
    test()