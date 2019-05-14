import logging
import matplotlib.pyplot as plt
import numpy as np

import analysis.recognition
import lbls

logger = logging.getLogger()
logger.setLevel(10)
handler = logging.StreamHandler()
logger.addHandler(handler)

cf_m = analysis.recognition.CharacterClassifierManager(lbls.lbls)
cf = cf_m.get_classifier()

for l in lbls.lbls:
    a = np.array(cf.matricesPoids[l]._matrix)
    fig, ax = plt.subplots()
    ax.imshow(a, cmap='seismic', interpolation='nearest')
    fig.colorbar(ax.pcolor(a), ax=ax, cmap='seismic')
    fig.savefig('tmp/models/' + l + '.jpg')
