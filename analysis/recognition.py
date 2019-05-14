import math
import time

import logging
import os.path
import pickle
from PIL import Image

import dataset
from utils import Matrix
from utils.graphics import PixelMatrix

logger = logging.getLogger(__name__)


class MatricePoids(Matrix):
    def __init__(self):
        super().__init__(28, 28, 0)
        self.sample_count = None


class CharacterFormatter:
    def __init__(self, char_pixel_matrix):
        self.__char_pixel_matrix = char_pixel_matrix

    def __call__(self):
        char_pixel_matrix = self.__char_pixel_matrix
        formatted_char_content_size = (22 * char_pixel_matrix.image.size[0] //
                                       char_pixel_matrix.image.size[1], 22)

        formatted_char_content = PixelMatrix(char_pixel_matrix.image.resize(formatted_char_content_size))
        formatted_char_width = formatted_char_content_size[0] if formatted_char_content_size[0] > 28 else 28
        formatted_char = PixelMatrix(Image.new('L', (formatted_char_width, 28), 255))

        content_offset = (0 if formatted_char_content_size[0] > 28 else (28 - formatted_char_content_size[0]) // 2, 2)

        for j in range(formatted_char_content_size[1]):
            for i in range(formatted_char_content_size[0]):
                formatted_char[i + content_offset[0], j + content_offset[1]] = formatted_char_content[i, j]

        # Crop the image if it is too large.
        if formatted_char_content_size[0] > 28:
            overlap = formatted_char_content_size[0] - 28
            box = (overlap // 2 + overlap % 2, 0, overlap // 2 + overlap % 2 + 28, 28)
            formatted_char = PixelMatrix(formatted_char.image.crop(box))

        return formatted_char


class CharacterClassifier:
    def __init__(self, lst_lbl, donnee_ent={}):
        """ donnee_ent = dictionnaire des donnee d'entrainement"""
        self.matricesPoids = {}
        self.donnee_ent = donnee_ent
        for lbl in lst_lbl:
            self.matricesPoids[lbl] = MatricePoids()

    def train_char(self, label):
        matricePoids = self.matricesPoids[label]
        matricePoids.sample_count = len(self.donnee_ent[label])

        for index, value in enumerate(matricePoids):
            for image in self.donnee_ent[label]:
                pixel = image[index]
                if pixel <= 127:
                    matricePoids[index] += 1
                else:
                    matricePoids[index] -= 1

    def train_liste(self):
        liste_lbl = []
        for lbl in self.matricesPoids.keys():
            logger.info('Processing label "' + lbl + '"')
            self.train_char(lbl)
            liste_lbl.append(lbl)

    def prediction(self, model, img):
        """calcule du score pour un modele
            img = matrice de l'image
            model = matrice du model"""
        score = 0

        threshold = - math.ceil(model.sample_count * 0.95)

        for index, poids in enumerate(model):
            if img[index] == 0:
                score += poids
            elif poids > threshold:
                score -= poids
        return score

    def predire(self, img):
        """calcul les scores de l'image pour tous les modeles et tri le resultat"""
        liste_taux = []

        for lbl, matricePoids in self.matricesPoids.items():
            score = self.prediction(matricePoids, img)
            liste_taux.append((score, lbl))

        liste_taux.sort(key=lambda tup: tup[0], reverse=True)
        return liste_taux


class CharacterClassifierManager:
    def __init__(self, lbls):
        self.__lbls = lbls
        self.__db_path = 'database'
        self.__mode = 1  # 0: MNIST 1: Font
        self.__classifier = None

    def get_classifier(self) -> CharacterClassifier:
        if self.__classifier:
            return self.__classifier

        self.__classifier = CharacterClassifier(self.__lbls)

        if os.path.isfile(self.__db_path):
            logger.info('Loading database...')
            with open(self.__db_path, 'rb') as file:
                self.__classifier.matricesPoids = pickle.load(file)
            logger.info('Done.')
        else:
            start_time = time.process_time()

            logger.info('Creating database')
            logger.info('Loading dataset...')

            if self.__mode:
                ds = dataset.load_ttf('dataset/OpenSans-Bold.ttf', self.__lbls)
            else:
                ds = dataset.load_mnist('dataset/train_img_mnist',
                                        'dataset/lbl_mnist',
                                        dict((i + 1, self.__lbls[i]) for i in range(len(self.__lbls))))

            ds = dataset.list_to_dict(ds)
            self.__classifier.donnee_ent = ds
            logger.info('Done. (' + str(time.process_time() - start_time) + ' seconds)')
            self.__classifier.train_liste()

            with open(self.__db_path, 'wb') as file:
                pickle.dump(self.__classifier.matricesPoids, file)

            logger.info('Database created in ' + str(time.process_time() - start_time) + ' seconds.')

        return self.__classifier
