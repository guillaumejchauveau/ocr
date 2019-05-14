from PIL import Image, ImageMorph, ImageOps

import utils


class PixelMatrix(utils.Matrix):
    def __init__(self, image: Image):
        """Creates a PixelMatrix object.

        It's a simple wrapper for PIL's PixelAccess objects.

        :param image: The image to work on.
        :type image: Image
        """
        super().__init__(matrix=[[]])

        self._set_image(image)

    @property
    def image(self) -> Image:
        """Accessor to the PIL Image object.

        :return The Image object containing the pixels.
        :rtype Image
        """
        return self.__image

    def _set_image(self, img: Image):
        """Sets the image of the instance and updates the work matrix.
        :param img: The image to assign.
        :type img: Image
        """
        self.__image = img
        self.__matrix = self.image.load()

    def copy(self):
        """Creates a copy of the PixelMatrix.

        :return A copy of the instance and it's Image.
        :rtype PixelMatrix
        """
        return self.__class__(self.image.copy())

    def convert(self, mode):
        """Creates a copy with a different image mode.

        :param mode: The requested mode.
        :return A copy of the instance with the new converted Image.
        :rtype PixelMatrix
        """
        return self.__class__(self.image.convert(mode))

    def __getitem__(self, position: (int, int) or int):
        """Maps evaluation of self[position] to the matrix.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        :return The color at position.
        """
        position = self._position(position)

        return self.__matrix[position]

    def __setitem__(self, position: (int, int) or int, value: int or tuple):
        """Maps assignment of self[position] to the matrix.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        :param value: The color to assign.
        :type value: int or tuple
        """
        position = self._position(position)

        self.__matrix[position] = value

    def __delitem__(self, position: (int, int) or int):
        """Maps deletion of self[position] to the matrix.

        :param position: X and Y coordinates.
        :type position: (int, int) or int
        """
        position = self._position(position)

        self.__matrix[position] = None

    @property
    def width(self) -> int:
        """
        :return The width of the matrix.
        :rtype int
        """
        return self.image.size[0]

    @property
    def height(self) -> int:
        """
        :return The height of the matrix.
        :rtype int
        """
        return self.image.size[1]

    def __neg__(self):
        """Invert the instance's image."""
        return self.__class__(ImageOps.invert(self.image))

    def __add__(self, other: int or tuple or utils.Matrix):
        """
        Creates a new matrix with each values of the instance plus an external value or the values of another Matrix.

        :param other: Either a color or a Matrix of colors.
        :type other: int or list or tuple or utils.Matrix
        """
        copy = self.copy()

        if isinstance(other, utils.Matrix):
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    copy_value = list(value)

                    for channel, other_channel_value in enumerate(other[index]):
                        copy_value[channel] += other_channel_value

                    copy_value = tuple(copy_value)
                else:
                    copy_value = value + other[index]

                copy[index] = copy_value
        else:
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    copy_value = list(value)

                    for channel, other_channel_value in enumerate(other):
                        copy_value[channel] += other_channel_value

                    copy_value = tuple(copy_value)
                else:
                    copy_value = value + other[index]

                copy[index] = copy_value

        return copy

    def __sub__(self, other: int or list or tuple or utils.Matrix):
        """
        Creates a new matrix with each values of the instance minus an external value or the values of another Matrix.

        :param other: Either a color or a Matrix of colors.
        :type other: int or list or tuple or utils.Matrix
        """
        copy = self.copy()

        if isinstance(other, utils.Matrix):
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    for channel, channel_value in enumerate(value):
                        copy[index][channel] = channel_value - other[index][channel]
                else:
                    copy[index] = value - other[index]
        else:
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    for channel, channel_value in enumerate(value):
                        copy[index][channel] = channel_value - other[channel]
                else:
                    copy[index] = value - other

        return copy

    def __iadd__(self, other: int or list or tuple or utils.Matrix):
        """
        Increments the instance's values with an external value or the values of another Matrix.

        :param other: Either an int or a Matrix of ints.
        :type other: int or list or tuple or utils.Matrix
        """
        if isinstance(other, utils.Matrix):
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    for channel, channel_value in enumerate(value):
                        self[index][channel] += other[index][channel]
                else:
                    self[index] += other[index]
        else:
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    for channel, channel_value in enumerate(value):
                        self[index][channel] += other[channel]
                else:
                    self[index] += other

        return self

    def __isub__(self, other: int or list or tuple or utils.Matrix):
        """
        Decrements the instance's values with an external value or the values of another Matrix.

        :param other: Either an int or a Matrix of ints.
        :type other: int or list or tuple or utils.Matrix
        """
        if isinstance(other, utils.Matrix):
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    for channel, channel_value in enumerate(value):
                        self[index][channel] -= other[index][channel]
                else:
                    self[index] -= other[index]
        else:
            for index, value in enumerate(self):
                if type(value) == list or type(value) == tuple:
                    for channel, channel_value in enumerate(value):
                        self[index][channel] -= other[channel]
                else:
                    self[index] -= other

        return self

    def slice(self, box: (int, int, int, int)):
        """Extracts a piece of the pixel matrix.

        :param box: Defines the rectangle to slice with four lines: left, top, right (excluded) and bottom (excluded).
        :type box: (int, int, int, int)
        :return A new PixelMatrix object.
        :rtype PixelMatrix
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

        return PixelMatrix(self.image.crop(box))


class RawImage(PixelMatrix):
    def __init__(self, img: Image):
        """Creates a RawImage object.

        A RawImage is an image wich has been transformed to be used in analysis.

        :param img: The raw image to transform.
        :type img: Image
        """
        super().__init__(img)

        self.__original = img

    def binarize(self):
        """Transforms the color image in a monochromatic image."""
        self._set_image(ImageOps.grayscale(self.image))
        threshold = sum(self.image.getextrema()) / 2

        for index, value in enumerate(self):
            self[index] = 0 if value <= threshold else 255

    def erode(self):
        """Erodes the image."""
        erosion = ImageMorph.MorphOp(op_name='erosion4')
        self._set_image(ImageOps.crop(erosion.apply(self.image)[1], 1))


class Shape:
    def __init__(self, position_x: int, position_y: int):
        """Creates a Shape object.

        A shape is a set of Points.
        """
        self.__width = 1
        self.__height = 1
        self.__position_x = position_x
        self.__position_y = position_y

        self.__points = []

    def __getitem__(self, index: int) -> utils.Point:
        """Maps evaluation of self[index] to the shape's points.

        :param index: The index of the point.
        :type index: int
        :return The Point.
        :rtype Point
        """
        return self.__points[index]

    def __iter__(self):
        """
        :return An iterator over the shape's points.
        """
        return iter(self.__points)

    def __len__(self):
        """
        :return The number of Points of the shape (its surface).
        """
        return len(self.__points)

    @property
    def width(self) -> int:
        """
        :return The width of the shape's bounding-box.
        :rtype int
        """
        return self.__width

    @property
    def height(self) -> int:
        """
        :return The height of the shape's bounding-box.
        :rtype int
        """
        return self.__height

    @property
    def position_x(self) -> int:
        """
        :return X position of the top-left corner of the shape's bounding-box.
        :rtype int
        """
        return self.__position_x

    @property
    def position_y(self) -> int:
        """
        :return Y position of the top-left corner of the shape's bounding-box.
        :rtype int
        """
        return self.__position_y

    def add_point(self, point: utils.Point):
        """Adds a point to the shape and update the shape's bounding-box's position and size accordingly.

        :param point: The Point to add.
        :type point: Point
        """
        h_offset = point.x - self.position_x

        if h_offset < 0:
            self.__position_x = point.x
            self.__width -= h_offset
        if h_offset >= self.width:
            self.__width = h_offset + 1

        v_offset = point.y - self.position_y

        if v_offset < 0:
            self.__position_y = point.y
            self.__height -= v_offset
        if v_offset >= self.height:
            self.__height = v_offset + 1

        self.__points.append(point)

    def to_pixel_matrix(self) -> PixelMatrix:
        """Creates a PixelMatrix based on the shape's points.

        :return The PixelMatrix.
        :rtype PixelMatrix
        """
        image = Image.new('1', (self.width, self.height), 255)
        pixel_matrix = PixelMatrix(image)

        for point in self:
            pixel_matrix[point.x - self.position_x, point.y - self.position_y] = 0

        return pixel_matrix
