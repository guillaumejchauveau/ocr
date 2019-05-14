import logging

import analysis.recognition
import lbls

logger = logging.getLogger()
logger.setLevel(10)
handler = logging.StreamHandler()
logger.addHandler(handler)

cf_m = analysis.recognition.CharacterClassifierManager(lbls.lbls)
cf = cf_m.get_classifier()
