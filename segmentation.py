import logging
from PIL import Image

import analysis.graphics.text
import utils.graphics

logger = logging.getLogger()
logger.setLevel(10)
handler = logging.StreamHandler()
logger.addHandler(handler)

img = utils.graphics.PixelMatrix(Image.open('tmp/image.bmp').convert('1'))

tld = analysis.graphics.text.TextLineDiscovery(img, lambda value: value == 0)
for line_index, tl in enumerate(tld):
    if tl.height < 28:
        continue

    tl.resolve_characters(img, lambda value: value == 0)

    for char_index, character in enumerate(tl.characters):
        character.shape.to_pixel_matrix().image.save('tmp/' + str(line_index) + '-' + str(char_index) + '.bmp')
