import collections
import logging

import utils
import utils.graphics

logger = logging.getLogger(__name__)


class ShapeDiscovery:
    def __init__(self, pixel_matrix: utils.Matrix, is_point: callable(int), mode: int = 0):
        """Creates a ShapeDiscovery object.

        The ShapeDiscovery object while create Shape objects with all the points of each shapes in a matrix. See
        ShapeDiscovery.fetch() for more information.

        :param pixel_matrix: The matrix used to search shapes.
        :type pixel_matrix: utils.Matrix
        :param is_point: A function that determines if a given pixel is considered to be a point.
        :type is_point: callable(int)
        :param mode: Defines if a row is horizontal (0) or vertical (1) (default horizontal).
        :type mode: int
        """
        self.__pixel_matrix = pixel_matrix
        self.__is_point = is_point
        self.__row_mode = mode

        self.__fetch_cursor_x = 0
        self.__fetch_cursor_y = 0

        self.__current_shape = None
        self.__row_scan_queue = collections.deque()
        self.__previous_point_queued = {-1: False, 1: False}

    def fetch(self) -> utils.graphics.Shape:
        """Iterates over the pixel matrix to find a shape's point and processes it to find all the shape's points.

        The next call will process the next found shape. The ShapeDiscovery object can be iterated to execute `fetch(
        )` until all shapes have been found.

        Point processing
        ----------------

        When a point has to be processed, it is added to the scan queue (`ShapeDiscovery.__row_scan_queue()`).
        The queue starts with the first detected point and will be processed by `ShapeDiscovery.scan_row()` until it is
        empty. A row is a set of the horizontally or vertically adjacent shape points of a point (depending of
        `ShapeDiscovery.__row_mode`, see `ShapeDiscovery.__init__() for more info`). See `ShapeDiscovery.scan_row()`
        for more information on the row scan.

        :return A Shape with all the detected Points.
        :rtype utils.graphics.Shape
        """
        # Resets data from previous fetch.
        self.__current_shape = None
        self.__row_scan_queue.clear()

        # Goes on the cursor position of the last fetch.
        while self.__fetch_cursor_y < self.__pixel_matrix.height:
            while self.__fetch_cursor_x < self.__pixel_matrix.width:
                # Checks if pixel is part of a shape.
                if self.__is_point(self.__pixel_matrix[self.__fetch_cursor_x, self.__fetch_cursor_y]):
                    start_point = utils.Point(self.__fetch_cursor_x, self.__fetch_cursor_y)

                    # Initialises shape.
                    self.__current_shape = utils.graphics.Shape(start_point.x, start_point.y)

                    # Queues the shape pixel for row scan.
                    self.__row_scan_queue.append(start_point)

                    # Processes row scan queue.
                    while len(self.__row_scan_queue):
                        start_point = self.__row_scan_queue.popleft()
                        self.scan_row(start_point)

                    return self.__current_shape

                self.__fetch_cursor_x += 1

            self.__fetch_cursor_x = 0
            self.__fetch_cursor_y += 1

    def scan_row(self, start_point: utils.Point):
        """Finds all adjacent shape points of a point and send them to `ShapeDiscovery.__process_row_point`.

        :param start_point: The start point.
        :type start_point: utils.Point
        """
        # logger.debug('sp: ' + str(start_point))

        self.__previous_point_queued = {-1: False, 1: False}

        self.__process_row_point(start_point)
        cursor_offset_dim = self.__row_mode

        for cursor_offset in [-1, 1]:  # Previous, next points.
            cursor_pos = [start_point.x, start_point.y]

            while True:
                cursor_pos[cursor_offset_dim] += cursor_offset

                # Catches IndexError exception in case of matrix edge encounter.
                try:
                    point = utils.Point(cursor_pos[0], cursor_pos[1])

                    if self.__is_point(self.__pixel_matrix[cursor_pos[0], cursor_pos[1]]):
                        self.__process_row_point(point)
                    else:
                        self.__queue_adjacent_point_side_rows(point)

                        break
                except IndexError:
                    break

    def __process_row_point(self, point: utils.Point):
        """
        Adds a row point to its shape and removes it from the original matrix to prevent reprocessing. Queues its
        previous row and next row adjacent shape points.

        :param point: The point to process.
        :type point: utils.Point
        """
        # logger.debug('p: ' + str(point))

        # Removes point from matrix
        self.__pixel_matrix[point.x, point.y] = 255
        # Adds pixel to shape
        self.__current_shape.add_point(point)

        # Removes point from queue if present (edge closed).
        for queued_point_index, queued_point in enumerate(self.__row_scan_queue):
            if queued_point == point:
                # logger.debug('rqp: ' + str(queued_point))

                del self.__row_scan_queue[queued_point_index]
                break

        self.__queue_adjacent_point_side_rows(point)

    def __queue_adjacent_point_side_rows(self, point: utils.Point):
        """Queues the previous and next row's adjacent point.

        :param point:
        :type point: utils.Point
        """
        cursor_offset_dim = abs(self.__row_mode - 1)

        for cursor_offset in [-1, 1]:
            cursor_pos = [point.x, point.y]
            cursor_pos[cursor_offset_dim] += cursor_offset

            # Checks if the row exists.
            if 0 <= cursor_pos[cursor_offset_dim] < \
                    (self.__pixel_matrix.width if self.__row_mode else self.__pixel_matrix.height):
                if self.__is_point(self.__pixel_matrix[cursor_pos[0], cursor_pos[1]]):
                    # Queues it only if the previous on the same line haven't already been queued to prevent row
                    # duplicate.
                    if not self.__previous_point_queued[cursor_offset]:
                        self.__row_scan_queue.append(utils.Point(cursor_pos[0], cursor_pos[1]))
                        self.__previous_point_queued[cursor_offset] = True

                        # logger.debug('qp: ' + str(self.__row_scan_queue[-1]))
                else:
                    self.__previous_point_queued[cursor_offset] = False

    def __iter__(self):
        """Iterating over this object will execute `ShapeDiscovery.fetch()` until all shapes have been fetched."""
        return self

    def __next__(self) -> utils.graphics.Shape:
        """See `ShapeDiscovery.__iter__()`"""
        if self.fetch():
            return self.__current_shape

        raise StopIteration
