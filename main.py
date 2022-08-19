# main app file

# main application arguments :
# -i : input | the image input (must be a png, dimentions must be multiple of 8)
# -o : output | the file where the tilset should be saved
# -m : tilemap-output | generate a tilemap of the input picture with indexes from the generated tileset

import argparse
from PIL import Image

#TODO tile creation from image
def generate_tiles_from_image(image):
    return


def test():
    im = Image.open("test_logo.png")
    im = im.convert("RGBA")
    print("testing")


def main():
    parser = argparse.ArgumentParser(description="Generate tilsets from pictures")
    parser.add_argument("-i", "--input", help="input file (must be png)")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-m", "--tilemap-output", help="generate a tilemap")
    args = parser.parse_args()

    return


if __name__ == "__main__":
    main()