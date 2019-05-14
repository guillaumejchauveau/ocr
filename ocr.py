import time

import argparse
import logging
from PIL import Image

import analysis.graphics.text
import analysis.recognition
import lbls
import utils.graphics

logger = logging.getLogger()
logger.setLevel(10)
handler = logging.StreamHandler()
logger.addHandler(handler)

parser = argparse.ArgumentParser()
parser.add_argument('path', help='The path of the image')
path = parser.parse_args().path

logger.info('Processing ' + path)

start_time = time.process_time()

img = utils.graphics.RawImage(Image.open(path))
img.binarize()
img.erode()

cf_m = analysis.recognition.CharacterClassifierManager(lbls.lbls)
cf = cf_m.get_classifier()

tld = analysis.graphics.text.TextLineDiscovery(img, lambda value: value == 0)
with open('output.txt', 'w') as output_file:
    for tl in tld:
        if tl.height < 28:
            continue

        tl.resolve_characters(img, lambda value: value == 0)
        tl.resolve_text_content(cf)
        output_file.write(tl.text_content + '\n')

logger.info(path + ' processed in ' + str(time.process_time() - start_time) + ' seconds.')
