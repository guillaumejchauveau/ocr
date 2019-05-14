from PIL import Image

import utils.graphics

img = utils.graphics.RawImage(Image.open('text3.jpg'))
img.binarize()
img.erode()
img.image.save('tmp/image.bmp')
