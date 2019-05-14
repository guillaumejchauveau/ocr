class Point:
    def __init__(self, x: int, y: int):
        """Creates a Point object.

        Just a point in a matrix.

        :param x: X position of the point.
        :param y: Y position of the point.
        :type x: int
        :type y: int
        """
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        """
        :return X position of the point.
        :rtype int
        """
        return self.__x

    @property
    def y(self) -> int:
        """
        :return Y position of the pixel.
        :rtype int
        """
        return self.__y

    def __eq__(self, other):
        """Compares 2 points' position.

        :param other: The point to compare the instance to.
        :type other: Point
        """
        return self.x == other.x and self.y == other.y

    def __str__(self):
        """Creates a convenient string representation for print.

        :return A string containing the coordinates of the point.
        :rtype str
        """
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


class Matrix:
    def __init__(self, width: int = None, height: int = None, initial_value=None, matrix: list = None):
        """Creates a Matrix object.

        :param width: The width of the matrix.
        :type width: int
        :param height: The height of the matrix.
        :type height: int
        :param initial_value: The value used to fill the matrix.
        :param matrix: If specified, width and height are unnecessary.
        :type matrix: list
        :raise ValueError: Raised if width or height have been forgotten.
        """
        if matrix:
            self.__matrix = matrix

            self.__width = len(self.__matrix[0])
            self.__height = len(self.__matrix)
        else:
            if width is None or height is None:
                raise ValueError('Width or height undefined.')

            self.__width = width
            self.__height = height

            self.__matrix = []

            for x in range(self.width):
                self.__matrix.append([initial_value] * self.height)

        self.__iter_x_cursor = 0
        self.__iter_y_cursor = 0

    def _position(self, input_pos: (int, int) or int) -> (int, int):
        """Converts a user-given position to an usable one.

        Position can be either a tuple of x and y or an int.

        :param input_pos: User position
        :type input_pos: (int, int) or int
        :return Accessible index based on user position.
        :rtype (int, int)
        :raise IndexError: Raised if the user position is not recognized.
        """
        if type(input_pos) == tuple:
            return input_pos

        if type(input_pos) == int:
            return input_pos % self.width, input_pos // self.width

        raise IndexError

    @property
    def _matrix(self) -> list:
        """Magic accessor to the actual matrix.

        :rtype list
        """
        return self.__matrix

    def __getitem__(self, position: (int, int) or int):
        """Maps evaluation of `self[position]` to the matrix.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        :return The value at position.
        """
        x, y = self._position(position)

        return self.__matrix[y][x]

    def __setitem__(self, position: (int, int) or int, value):
        """Maps assignment of `self[position]` to the matrix.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        :param value: The value to assign.
        """
        x, y = self._position(position)

        self.__matrix[y][x] = value

    def __delitem__(self, position: (int, int) or int):
        """Maps deletion of `self[position]` to the matrix.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        """
        x, y = self._position(position)

        self.__matrix[y][x] = None

    @property
    def width(self) -> int:
        """
        :return The width of the matrix.
        :rtype int
        """
        return self.__width

    @property
    def height(self) -> int:
        """
        :return The height of the matrix.
        :rtype int
        """
        return self.__height

    def __len__(self):
        """
        :return The surface of the matrix.
        """
        return self.width * self.height

    def __iter__(self):
        """Iterating over this object will give access to each of the values of the matrix."""
        self.__iter_x_cursor = 0
        self.__iter_y_cursor = 0

        return self

    def __next__(self):
        """See `self.__iter__`."""
        if self.__iter_x_cursor >= self.width:
            self.__iter_x_cursor = 0
            self.__iter_y_cursor += 1

        if self.__iter_y_cursor >= self.height:
            raise StopIteration

        self.__iter_x_cursor += 1

        return self[self.__iter_x_cursor - 1, self.__iter_y_cursor]

    def __lt__(self, other):
        """
        'Lower than' comparison between each values of the instance and an external value or the values of another
        Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            result = self.__class__(self.width, self.height)

            for index, value in enumerate(self):
                result[index] = value < other[index]

            return result
        else:
            for value in self:
                if value >= other:
                    return False

        return True

    def __le__(self, other):
        """
        'Lower than or equals' comparison between each values of the instance and an external value or the values of
        another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            result = self.__class__(self.width, self.height)

            for index, value in enumerate(self):
                result[index] = value <= other[index]

            return result
        else:
            for value in self:
                if value > other:
                    return False

        return True

    def __eq__(self, other):
        """
        'Equals' comparison between each values of the instance and an external value or the values of another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            result = self.__class__(self.width, self.height)

            for index, value in enumerate(self):
                result[index] = value == other[index]

            return result
        else:
            for value in self:
                if value != other:
                    return False

        return True

    def __ne__(self, other):
        """
        'Not equal' comparison between each values of the instance and an external value or the values of another
        Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            result = self.__class__(self.width, self.height)

            for index, value in enumerate(self):
                result[index] = value != other[index]

            return result
        else:
            for value in self:
                if value == other:
                    return False

        return True

    def __gt__(self, other):
        """
        'Greater than' comparison between each values of the instance and an external value or the values of another
        Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            result = self.__class__(self.width, self.height)

            for index, value in enumerate(self):
                result[index] = value > other[index]

            return result
        else:
            for value in self:
                if value <= other:
                    return False

        return True

    def __ge__(self, other):
        """
        'Greater than or equals' comparison between each values of the instance and an external value or the values of
        another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            result = self.__class__(self.width, self.height)

            for index, value in enumerate(self):
                result[index] = value >= other[index]

            return result
        else:
            for value in self:
                if value < other:
                    return False

        return True

    def __add__(self, other):
        """
        Creates a new matrix with each values of the instance plus an external value or the values of another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        copy = self.__class__(self.width, self.height)

        if isinstance(other, self.__class__):
            for index, value in enumerate(self):
                copy[index] = value + other[index]
        else:
            for index, value in enumerate(self):
                copy[index] = value + other

        return copy

    def __sub__(self, other):
        """
        Creates a new matrix with each values of the instance minus an external value or the values of another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        copy = self.__class__(self.width, self.height)

        if isinstance(other, self.__class__):
            for index, value in enumerate(self):
                copy[index] = value - other[index]
        else:
            for index, value in enumerate(self):
                copy[index] = value - other

        return copy

    def __iadd__(self, other):
        """
        Increments the instance's values with an external value or the values of another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            for index, value in enumerate(self):
                self[index] += other[index]
        else:
            for index, value in enumerate(self):
                self[index] += other

        return self

    def __isub__(self, other):
        """
        Decrements the instance's values with an external value or the values of another Matrix.

        :param other: Either a value or a Matrix of values.
        """
        if isinstance(other, self.__class__):
            for index, value in enumerate(self):
                self[index] -= other[index]
        else:
            for index, value in enumerate(self):
                self[index] -= other

        return self

    def slice(self, box: (int, int, int, int)):
        """Extracts a piece of the matrix.

        :param box: Defines the rectangle to slice with four lines: left, top, right (excluded) and bottom (excluded).
        :type box: (int, int, int, int)
        :return A new Matrix object.
        :rtype Matrix
        """
        box = list(box)

        for index, axis_value in enumerate(box):
            if axis_value < 0:
                box[index] = 0

            # If odd then it's a vertical axis.
            if index % 2:
                if axis_value > self.height:
                    box[index] = self.height
            else:
                if axis_value > self.width:
                    box[index] = self.width

        width = box[2] - box[0]
        height = box[3] - box[1]

        matrix_slice = self.__class__(width, height)

        for y_cursor in range(box[1], box[3]):
            for x_cursor in range(box[0], box[2]):
                matrix_slice[x_cursor, y_cursor] = self[x_cursor, y_cursor]

        return matrix_slice

    def neighbors(self, position: (int, int) or int, connectivity: int = 1, horizontal: bool = True,
            vertical: bool = True):
        """Slice the matrix with a given element's neighbors.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        :param connectivity: The number of neighbors around the pixel to slice.
        :type connectivity: int
        :param horizontal: Determines if the horizontal neighbors have to be taken.
        :type horizontal: bool
        :param vertical: Determines if the vertical neighbors have to be taken.
        :type vertical: bool
        :return The matrix of neighbors.
        :rtype Matrix
        """
        position = self._position(position)

        box = [
            *position,
            *position
        ]

        if horizontal:
            box[0] -= connectivity
            box[2] += (connectivity + 1)
        else:
            box[2] += 1
        if vertical:
            box[1] -= connectivity
            box[3] += (connectivity + 1)
        else:
            box[3] += 1

        return self.slice(box)
