import struct
from PIL import Image, ImageDraw, ImageFont

from dataset.Character import Character
from utils.graphics import PixelMatrix


def load_mnist(imagespath: str, labelspath: str, labelsdict: dict = {}):
    characters = []

    # Load images file
    with open(imagespath, "rb") as file:
        magic = struct.unpack('>I', file.read(4))[0]
        nbr = struct.unpack('>I', file.read(4))[0]
        size = struct.unpack('>II', file.read(8))

        for i in range(nbr):
            img = Image.new("L", size)
            pixels = PixelMatrix(img)
            for x in range(size[0]):
                for y in range(size[1]):
                    pixels[x, y] = 255 - struct.unpack('B', file.read(1))[0]
            characters.append(Character(pixels))

    # Load labels file
    with open(labelspath, "rb") as file:
        magic = struct.unpack('>I', file.read(4))[0]
        lbl_nbr = struct.unpack('>I', file.read(4))[0]

        if lbl_nbr != nbr:
            raise AssertionError("Size of labels file is not egal to size of images file")

        for i in range(lbl_nbr):
            label = struct.unpack('B', file.read(1))[0]
            if label in labelsdict:
                characters[i].label = labelsdict[label]
            else:
                characters[i].label = label

    return characters


def load_ttf(ttfpath: str, lbls):
    font = ImageFont.truetype(ttfpath, 30)
    characters = []

    for lbl in lbls:
        image = Image.new("1", (28, 28), 255)

        draw = ImageDraw.Draw(image)
        t_size = font.getsize(lbl)
        draw.text((14 - t_size[0] / 2 + 1, 14 - t_size[1] / 2 - 6), lbl, font=font)

        characters.append(Character(PixelMatrix(image), lbl))

    return characters


def list_to_dict(array):
    d = {}

    for char in array:
        label = char.label

        if label not in d:
            d[label] = []
        d[char.label].append(char.pixels)

    return d
