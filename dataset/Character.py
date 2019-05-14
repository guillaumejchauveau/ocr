class Character:
    def __init__(self, pixel_matrix, label: str = None):
        self.__pixel_matrix = pixel_matrix
        self.__label = label

    @property
    def label(self):
        return self.__label

    @property
    def pixels(self):
        return self.__pixel_matrix

    @label.setter
    def label(self, label):
        self.__label = label
