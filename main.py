# main app file

# main application arguments :
# -i : input | the image input (must be a png, dimentions must be multiple of 8)
# -o : output | the file where the tilset should be saved
# -m : tilemap-output | generate a tilemap of the input picture with indexes from the generated tileset

import argparse
from PIL import Image
# from tile import Tile
from tile import MetaTile

#TODO tile creation from image
def generate_tiles_from_image(image):
    """generate a tileset from an image"""
    # slice image in multiple 8 by 8 squares
    width, height = image.size
    assert width%8 == 0
    assert height%8 == 0
    for i in range(width//8):
        for j in range(height//8):
            slice = image.crop(i*8, j*8, (i+1)*8, (j+1)*8)
            #TODO create tile
            t = MetaTile(slice)
    return


def test():
    """test function"""
    # im = Image.open("test_logo.png")
    im = Image.open("test.png")
    im = im.convert("RGBA")
    print("testing")
    generate_tiles_from_image(im)
    print("done")


def main():
    """main function"""
    parser = argparse.ArgumentParser(description="Generate tilsets from pictures")
    parser.add_argument("-i", "--input", help="input file (must be png)")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-m", "--tilemap-output", help="generate a tilemap")
    args = parser.parse_args()

    return


if __name__ == "__main__":
    test()
    main()