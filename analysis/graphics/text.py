import logging

import analysis.graphics
import utils.graphics.text
from utils.graphics import PixelMatrix

logger = logging.getLogger(__name__)


class TextLineDiscovery:
    def __init__(self, pixel_matrix: PixelMatrix, is_point: callable(int)):
        """Creates a TextLineDiscovery object.

        This object will detect all vertically isolated regions of PixelMatrix wich contains points.

        :param pixel_matrix: The matrix used to search lines.
        :type pixel_matrix: PixelMatrix
        :param is_point: A function that determines if a given pixel is considered to be a point.
        :type is_point: callable(int)
        """
        self.__pixel_matrix = pixel_matrix
        self.__is_point = is_point

        self.__fetch_cursor_y = 0
        self.__current_text_line = None

    def fetch(self) -> utils.graphics.text.TextLine:
        """Vertically iterates over the pixel matrix to find the beginning and the end of a new text line.

        :return The new text line.
        :rtype utils.graphics.text.TextLine
        """
        text_line_y = -1
        text_line_height = 1

        # Goes on the cursor position of the last fetch.
        while self.__fetch_cursor_y < self.__pixel_matrix.height:
            cursor_x = 0
            point_found = False

            while cursor_x < self.__pixel_matrix.width:
                if self.__is_point(self.__pixel_matrix[cursor_x, self.__fetch_cursor_y]):
                    point_found = True
                    break

                cursor_x += 1

            self.__fetch_cursor_y += 1

            if point_found:
                # If new line detected.
                if not text_line_y + 1:
                    text_line_y = self.__fetch_cursor_y
                else:  # If line height measurement is in progress.
                    text_line_height += 1
            elif text_line_y + 1:  # End of text line reached
                self.__current_text_line = utils.graphics.text.TextLine(text_line_y, text_line_height)
                return self.__current_text_line

    def __iter__(self):
        """Iterating over this object will execute `TextLineDiscovery.fetch()` until all text lines have been
        fetched."""
        return self

    def __next__(self) -> utils.graphics.text.TextLine:
        """See `TextLineDiscovery.__iter__()`"""
        if self.fetch():
            return self.__current_text_line

        raise StopIteration


class CharacterDiscovery:
    def __init__(self, pixel_matrix: PixelMatrix, is_point: callable(int)):
        """

        :param pixel_matrix: The matrix used to search characters.
        :type pixel_matrix: PixelMatrix
        :param is_point: A function that determines if a given pixel is considered to be a point.
        :type is_point: callable(int)
        """
        self.__pixel_matrix = pixel_matrix
        self.__is_point = is_point

        self.__shapes_map = {}
        self.__chars_shapes = []

        self.__fetch_chars_shapes_index = 0
        self.__current_char = None

        self.__find_shapes()

    def __find_shapes(self):
        sd = analysis.graphics.ShapeDiscovery(self.__pixel_matrix, self.__is_point, 1)
        for shape in sd:
            for x in range(shape.position_x, shape.position_x + shape.width):
                if not self.__shapes_map.get(x):
                    self.__shapes_map[x] = []

                    self.__shapes_map[x].append(shape)

        last_x = -1
        current_char_shapes = set()
        for x in sorted(self.__shapes_map):
            if last_x != -1 and x != last_x + 1:
                self.__chars_shapes.append(current_char_shapes)
                current_char_shapes = set()

            for shape in self.__shapes_map[x]:
                current_char_shapes.add(shape)

            last_x = x

        self.__chars_shapes.append(current_char_shapes)

    def fetch(self) -> utils.graphics.text.Character:
        """

        :return The new character.
        :rtype utils.graphics.text.Character
        """
        while self.__fetch_chars_shapes_index < len(self.__chars_shapes):
            char_shapes = list(self.__chars_shapes[self.__fetch_chars_shapes_index])
            char_pos = char_shapes[0].position_x, char_shapes[0].position_y
            char_entire_shape = utils.graphics.Shape(char_pos[0], char_pos[1])

            for char_shape in char_shapes:
                for point in char_shape:
                    char_entire_shape.add_point(point)

            self.__fetch_chars_shapes_index += 1

            self.__current_char = utils.graphics.text.Character(char_entire_shape)
            return self.__current_char

    def __iter__(self):
        """Iterating over this object will execute `CharacterDiscovery.fetch()` until all characters have been
        fetched."""
        return self

    def __next__(self) -> utils.graphics.text.Character:
        """See `CharacterDiscovery.__iter__()`"""
        if self.fetch():
            return self.__current_char

        raise StopIteration
