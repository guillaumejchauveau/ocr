import analysis.graphics.text
import analysis.recognition
from utils.graphics import PixelMatrix, Shape


class Character:
    def __init__(self, shape: Shape):
        """Creates a Character object.

        :param shape: The Shape of the Character.
        :type shape: Shape
        """
        self.__shape = shape
        self.__char = None

    @property
    def shape(self) -> Shape:
        """
        :return The Shape of the Character.
        :rtype Shape
        """
        return self.__shape

    @property
    def char(self) -> str:
        """
        :return The resolved char.
        :rtype str
        """
        return self.__char

    def resolve_char(self, classifier: analysis.recognition.CharacterClassifier):
        """Calls the CharacterClassifier to identify the shape.

        :param classifier: The classifier to use for identification.
        :type classifier: analysis.recognition.CharacterClassifier
        """
        formatter = analysis.recognition.CharacterFormatter(self.shape.to_pixel_matrix())
        self.__char = classifier.predire(formatter())[0][1]


class TextLine:
    def __init__(self, y: int, height: int):
        """Creates a TextLine object. A TextLine is a horizontal region in a PixelMatrix.

        :param y: The vertical position of the top pixels of the text line.
        :type y: int
        :param height: The height of the text line.
        :type height: int
        """
        self.__y = y
        self.__height = height
        self.__characters = []
        self.__average_characters_width = None
        self.__text_content = None

    @property
    def y(self) -> int:
        """
        :return The vertical position of the top pixels of the text line.
        :rtype int
        """
        return self.__y

    @property
    def height(self) -> int:
        """
        :return The height of the text line.
        :rtype int"""
        return self.__height

    @property
    def characters(self) -> list:
        """
        :return The Characters discovered in the TextLine.
        :rtype list
        """
        return self.__characters

    @property
    def text_content(self) -> str:
        """
        :return The resolved text content.
        :rtype str
        """
        return self.__text_content

    def extract_pixel_matrix(self, pixel_matrix: PixelMatrix) -> PixelMatrix:
        """Extracts the region corresponding to the TextLine of a PixelMatrix.

        :param pixel_matrix: The PixelMatrix to extract the region from.
        :type pixel_matrix: PixelMatrix

        :rtype PixelMatrix
        """
        return pixel_matrix.slice((0, self.y, pixel_matrix.width, self.y + self.height))

    def resolve_characters(self, pixel_matrix: PixelMatrix, is_point: callable(int)):
        """Discovers the Characters inside the TextLine.

        :param pixel_matrix: The PixelMatrix containing the TextLine.
        :type pixel_matrix: PixelMatrix
        :param is_point: A function that determines if a given pixel is considered to be a point.
        :type is_point: callable(int)
        """
        self.__average_characters_width = 0
        cd = analysis.graphics.text.CharacterDiscovery(self.extract_pixel_matrix(pixel_matrix), is_point)

        for index, char in enumerate(cd):
            self.__characters.append(char)
            self.__average_characters_width += char.shape.width

        self.__average_characters_width /= len(self.characters)

    def resolve_text_content(self, classifier: analysis.recognition.CharacterClassifier):
        """Calls each characters' `resolve_char` method to reconstruct the text content of the line.
        Detects presence of spaces.

        :param classifier: The classifier to use for character identification.
        :type classifier: analysis.recognition.CharacterClassifier
        """
        self.__text_content = ''
        previous_x = -1
        for character in self.characters:
            if previous_x != -1 and (character.shape.position_x - previous_x) > self.__average_characters_width:
                self.__text_content += ' '

            character.resolve_char(classifier)
            self.__text_content += character.char

            previous_x = character.shape.position_x + character.shape.width
