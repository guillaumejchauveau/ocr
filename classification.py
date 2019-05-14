import math

import logging
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import analysis.recognition
import lbls
from utils import Matrix
from utils.graphics import PixelMatrix

logger = logging.getLogger()
logger.setLevel(10)
handler = logging.StreamHandler()
logger.addHandler(handler)

cf_m = analysis.recognition.CharacterClassifierManager(lbls.lbls)
cf = cf_m.get_classifier()

img = PixelMatrix(Image.open('tmp/1-0_f.bmp').convert('1'))

liste_taux = cf.predire(img)
for taux in liste_taux:
    print(taux)

# [DEBUG] Image de correpondance des points

for i in range(3):
    matriceCorrespondances = Matrix(28, 28)
    taux, lettre = liste_taux[i]

    matricePoids = cf.matricesPoids[lettre]
    threshold = - math.ceil(matricePoids.sample_count * 0.95)
    for index, poids in enumerate(matricePoids):
        if img[index] == 0:
            matriceCorrespondances[index] = poids
        elif poids > threshold:
            matriceCorrespondances[index] = -poids
        else:
            matriceCorrespondances[index] = 0

    matriceCorrespondances_np = np.array(matriceCorrespondances._matrix)
    fig, ax = plt.subplots()

    ax.imshow(matriceCorrespondances_np, cmap='seismic', interpolation='nearest')
    fig.colorbar(ax.pcolor(matriceCorrespondances_np), ax=ax, cmap='seismic')
    fig.savefig('tmp/pix_cor' + str(i) + '.jpg')
