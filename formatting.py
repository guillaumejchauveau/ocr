from PIL import Image

import analysis.recognition
import utils.graphics

file = '1-0'
img = utils.graphics.PixelMatrix(Image.open('tmp/' + file + '.bmp').convert('1'))
formatter = analysis.recognition.CharacterFormatter(img)
formatter().image.save('tmp/' + file + '_f.bmp')
