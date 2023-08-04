from __future__ import annotations
from typing import overload, Union, Callable
from functools import cache
import re


class Image:
    """
    The `Image` class is used to create images that can be displayed easily on the device's LED matrix.

    Given an image object it's possible to display it via the `display` API:

    ```python
    display.show(Image.HAPPY)
    ```
    """

    @overload
    def __init__(self) -> None:
        """Create a blank 5x5 image."""

    @overload
    def __init__(self, string: str) -> None:
        """Create an image by parsing the string, a single character returns that glyph.

        The `string` argument has to consist of digits 0-9 arranged into lines, describing the image, for example:

        ```python
        image = Image("90009:"
                      "09090:"
                      "00900:"
                      "09090:"
                      "90009")
        ```

        will create a 5x5 image of an X. The end of a line is indicated by a colon. It's also possible to use a newline (n) to indicate the end of a line like this:

        ```python
        image = Image("90009\\n"
                      "09090\\n"
                      "00900\\n"
                      "09090\\n"
                      "90009")
        ```

        Args:
            string (str): The string to parse

        Raises:
            ValueError: if an unexpected character is found in the string
        """

    @overload
    def __init__(self, width: int, height: int) -> None:
        """Create a blank image of given size.

        Args:
            width (int): The width of the image
            height (int): The height of the image

        Raises:
            ValueError: if width or height is not between 0 and 9
        """

    @overload
    def __init__(
        self, width: int, height: int, buffer: Union[bytes, bytearray]
    ) -> None:
        """Create an image from the given buffer.

        This form creates an empty image with `width` columns and `height` rows.
        `buffer` is an array of `width x height` integers in range 0-9 to initialize the image:

        ```python
        Image(2, 2, b'\\x08\\x08\\x08\\x08')
        ```

        or:

        ```python
        Image(2, 2, bytearray([9,9,9,9]))
        ```

        Will create a 2 x 2 pixel image at full brightness.

        .. note::
            Keyword arguments cannot be passed

        Args:
            width (int): The width of the image
            height (int): The height of the image
            buffer (Union[bytes, bytearray]): The buffer to use

        Raises:
            ValueError: if the buffer is the wrong size
            ValueError: if the width or height is not between 0 and 9
        """

    def __init__(self, *args, **kwargs) -> None:
        """Initialises `self` to a new `Image`.

        Args:
            *args: The arguments
            **kwargs: The keyword arguments
        """
        assert not kwargs, "Image() does not take keyword arguments"
        assert (
            0 <= len(args) and len(args) <= 3
        ), f"Image() expected at most 3 arguments, got {len(args)}"

        if len(args) == 1:
            string = args[0]
            assert isinstance(
                string, str
            ), f"string must be a str, not {type(string).__name__}"
            self.__init_from_string(string)
            return

        if len(args) == 0:
            width = 5
            height = 5
        else:
            width = args[0]
            height = args[1]
            assert isinstance(
                width, int
            ), f"width must be an int, not {type(width).__name__}"
            assert isinstance(
                height, int
            ), f"height must be an int, not {type(width).__name__}"

        if len(args) < 3:
            self.__init_from_size(width, height)
        else:
            buffer = args[2]
            assert isinstance(
                buffer, (bytes, bytearray)
            ), f"buffer must be a bytes or bytearray, not {type(buffer).__name__}"
            self.__init_from_buffer(width, height, buffer)

    def __init_from_string(self, string: str) -> None:
        """Initialises `self` to a new `Image` from a string.

        Args:
            string (str): The string to parse

        Raises:
            ValueError: if an unexpected character is found in the string
        """
        if len(string) == 1:
            string = Image.__ASCII.get(string, Image.__ASCII["?"])

        lines: list[str] = re.split("[:\n]", string)

        width = max(len(line) for line in lines)
        height = len(lines)

        self.__init_from_size(width, height)

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == " ":
                    number = 0
                elif not char.isdigit():
                    raise ValueError(f"Unexpected character {char} in Image definition")
                else:
                    number = int(char)

                self.__pixels[y][x] = number

    def __init_from_size(self, width: int, height: int) -> None:
        """Initialises `self` to a new `Image` from the given size.

        Args:
            width (int): The width of the image
            height (int): The height of the image

        Raises:
            ValueError: if the width or height is not positive
        """
        if width < 0:
            raise ValueError(f"width must be positive, got {width}")
        if height < 0:
            raise ValueError(f"height must be positive, got {width}")

        self.__readonly = False
        self.__width = width
        self.__height = height
        self.__pixels = [[0 for _ in range(self.__width)] for _ in range(self.__height)]

    def __init_from_buffer(
        self, width: int, height: int, buffer: Union[bytes, bytearray]
    ) -> None:
        """Initialises `self` to a new `Image` from the given buffer.

        Args:
            width (int): The width of the image
            height (int): The height of the image
            buffer (Optional[Union[bytes, bytearray]]): The buffer to use

        Raises:
            ValueError: if the buffer is the wrong size
            ValueError: if the width or height is not positive
        """
        self.__init_from_size(width, height)

        if len(buffer) != width * height:
            raise ValueError(
                "Image data is incorrect size. Expected {} bytes, got {}".format(
                    width * height, len(buffer)
                )
            )

        for y in range(height):
            for x in range(width):
                value = buffer[x + y * width]

                if value < 0 or value > 9:
                    raise ValueError(f"Bytes value {value} out of range 0-9")

                self.__pixels[y][x] = value

    def width(self) -> int:
        """Return the number of columns in the image.

        Returns:
            int : The width of the image
        """
        return self.__width

    def height(self) -> int:
        """Return the numbers of rows in the image.

        Returns:
            int : The height of the image
        """
        return self.__height

    def set_pixel(self, x: int, y: int, value: int) -> None:
        """Set the brightness of the pixel at column `x` and row `y` to the `value`, which has to be between 0 (dark) and 9 (bright).

        This method will raise an exception when called on any of the built-in read-only images, like `Image.HEART`.

        Args:
            x (int): The x position of the pixel
            y (int): The y position of the pixel
            value (int): The brightness of the pixel, from 0 (dark) to 9 (bright)

        Raises:
            TypeError: if the image is read-only
            ValueError: if the brightness is out of range
            ValueError: if x or y is out of the image
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"
        assert isinstance(
            value, int
        ), f"value must be an int, not {type(value).__name__}"

        if self.__readonly:
            raise TypeError("Image cannot be modified (try copying first)")
        if value < 0 or 9 < value:
            raise ValueError("brightness out of bounds")

        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            raise ValueError(f"invalid position {x}, {y}")

        self.__pixels[y][x] = value

    def get_pixel(self, x: int, y: int) -> int:
        """Return the brightness of pixel at column `x` and row `y` as an integer between 0 and 9.

        Args:
            x (int): The x position of the pixel
            y (int): The y position of the pixel

        Raises:
            ValueError: if x or y is out of the image

        Returns:
            int: The brightness of the pixel, from 0 (dark) to 9 (bright)
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"

        if x < 0 or x >= self.__width or y < 0 or y >= self.__height:
            raise ValueError(f"invalid position {x}, {y}")

        return self.__pixels[y][x]

    def shift_left(self, n: int) -> Image:
        """Return a new image created by shifting the picture left by n columns.

        Args:
            n (int): The number of columns to shift

        Returns:
            Image : The shifted image
        """
        assert isinstance(n, int), f"n must be an int, not {type(n).__name__}"

        image = Image(self.__width, self.__height)
        image.blit(self, n, 0, self.__width, self.__height)
        return image

    def shift_right(self, n: int) -> Image:
        """Same as image.shift_left(-n).

        Args:
            n (int): The number of columns to shift

        Returns:
            Image : The shifted image
        """
        assert isinstance(n, int), f"n must be an int, not {type(n).__name__}"

        return self.shift_left(-n)

    def shift_up(self, n: int) -> Image:
        """Return a new image created by shifting the picture up by n rows.

        Args:
            n (int): The number of rows to shift

        Returns:
            Image : The shifted image
        """
        assert isinstance(n, int), f"n must be an int, not {type(n).__name__}"

        image = Image(self.__width, self.__height)
        image.blit(self, 0, n, self.__width, self.__height)
        return image

    def shift_down(self, n: int):
        """Same as image.shift_up(-n).

        Args:
            n (int): The number of rows to shift

        Returns:
            Image : The shifted image
        """
        assert isinstance(n, int), f"n must be an int, not {type(n).__name__}"

        return self.shift_up(-n)

    def crop(self, x: int, y: int, w: int, h: int) -> Image:
        """Return a new image by cropping the picture to a width of `w` and a height of `h`, starting with the pixel at column `x` and row `y`.

        Args:
            x (int): The x position of the pixel
            y (int): The y position of the pixel
            w (int): The width of the image
            h (int): The height of the image

        Returns:
            Image : The cropped image
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"

        image = Image(w, h)
        image.blit(self, x, y, w, h)
        return image

    def copy(self) -> Image:
        """Return an exact copy of the image.

        Returns:
            Image : The copied image
        """
        image = Image(self.__width, self.__height)
        for y in range(image.__height):
            for x in range(image.__width):
                image.__pixels[y][x] = self.__pixels[y][x]
        return image

    def invert(self) -> Image:
        """Return a new image by inverting the brightness of the pixels in the source image.

        Returns:
            Image : The inverted image
        """
        image = Image(self.__width, self.__height)
        for y in range(image.__height):
            for x in range(image.__width):
                image.__pixels[y][x] = 9 - self.__pixels[y][x]
        return image

    def fill(self, value: int):
        """Set the brightness of all the pixels in the image to the value, which has to be between 0 (dark) and 9 (bright).

        This method will raise an exception when called on any of the built-in read-only images, like Image.HEART.

        Args:
            value (int): The brightness of the pixel

        Raises:
            TypeError: if the image is read-only
            ValueError: if the brightness is out of range
        """
        assert isinstance(
            value, int
        ), f"value must be an int, not {type(value).__name__}"

        if self.__readonly:
            raise TypeError("Image cannot be modified (try copying first)")
        if value < 0 or 9 < value:
            raise ValueError("brightness out of bounds")

        for y in range(self.__height):
            for x in range(self.__width):
                self.__pixels[y][x] = value

    def blit(
        self, src: Image, x: int, y: int, w: int, h: int, xdest: int = 0, ydest: int = 0
    ) -> None:
        """Copy the rectangle defined by `x`, `y`, `w`, `h` from the image `src` into this image at `xdest`, `ydest`.

        Areas in the source rectangle, but outside the source image are treated as having a value of 0.

        shift_left(), shift_right(), shift_up(), shift_down() and crop() can are all implemented by using blit().
        For example, img.crop(x, y, w, h) can be implemented as:

        ```python
        def crop(self, x, y, w, h):
            res = Image(w, h)
            res.blit(self, x, y, w, h)
            return res
        ```

        Args:
            src (Image): The source image
            x (int): The x position of the source rectangle
            y (int): The y position of the source rectangle
            w (int): The width of the source rectangle
            h (int): The height of the source rectangle
            xdest (int, optional): The x position of the destination rectangle. Defaults to 0.
            ydest (int, optional): The y position of the destination rectangle. Defaults to 0.

        """
        assert isinstance(src, Image), f"src must be an Image, not {type(src).__name__}"
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"
        assert isinstance(w, int), f"w must be an int, not {type(w).__name__}"
        assert isinstance(h, int), f"h must be an int, not {type(h).__name__}"
        assert isinstance(
            xdest, int
        ), f"xdest must be an int, not {type(xdest).__name__}"
        assert isinstance(
            ydest, int
        ), f"ydest must be an int, not {type(ydest).__name__}"

        for dx in range(max(0, xdest), min(xdest + w, self.__width)):
            for dy in range(max(0, ydest), min(ydest + h, self.__height)):
                sx = dx - (xdest - x)
                sy = dy - (ydest - y)
                try:
                    value = src.__pixels[sy][sx]
                except IndexError:
                    value = 0
                self.__pixels[dy][dx] = value

    def __merge_with_image(
        self, image: Image, merge_function: Callable[[int, int], int]
    ) -> Image:
        """Merge self with another image into a new Image using a merge function.

        Args:
            image (Image): The image to merge with
            merge_function (Callable[[int, int], int]): The function `(pixel1, pixel2) -> result` to merge the pixels with

        Raises:
            ValueError: if the images are not the same size

        Returns:
            Image: The merged image
        """
        if self.__width != image.__width or self.__height != image.__height:
            raise ValueError("Images must be the same size")

        image = Image(self.__width, self.__height)
        for y in range(image.__height):
            for x in range(image.__width):
                image.__pixels[y][x] = merge_function(
                    self.__pixels[y][x], image.__pixels[y][x]
                )
        return image

    def __merge_with_number(
        self,
        value: Union[int, float],
        merge_function: Callable[[int, Union[int, float]], int],
    ) -> Image:
        """Merge self with a number into a new Image using a merge function.

        Args:
            value (Union[int, float]): The number to merge with
            merge_function (Callable[[int, Union[int, float]], int]): The function `(pixel, value) -> result` to merge the pixels with

        Raises:
            ValueError: if value is negative

        Returns:
            Image: The merged image
        """
        if value < 0:
            raise ValueError("brightness multiplier must not be negative")

        image = Image(self.__width, self.__height)
        for y in range(image.__height):
            for x in range(image.__width):
                image.__pixels[y][x] = merge_function(self.__pixels[y][x], value)
        return image

    def __repr__(self):
        return (
            "Image('"
            + str.join(
                ":",
                (
                    str.join(
                        "", (str(self.__pixels[y][x]) for x in range(self.__width))
                    )
                    for y in range(self.__height)
                ),
            )
            + ":')"
        )

    def __str__(self):
        return (
            "Image(\n    '"
            + str.join(
                ":'\n    '",
                (
                    str.join(
                        "", (str(self.__pixels[y][x]) for x in range(self.__width))
                    )
                    for y in range(self.__height)
                ),
            )
            + ":'\n)"
        )

    def __add__(self, image: Image) -> Image:
        assert isinstance(
            image, Image
        ), f"Unsupported operand type(s) for +: Image and {type(image).__name__}"

        return self.__merge_with_image(
            image,
            lambda pixel1, pixel2: min(9, pixel1 + pixel2),
        )

    def __sub__(self, image: Image) -> Image:
        assert isinstance(
            image, Image
        ), f"Unsupported operand type(s) for -: Image and {type(image).__name__}"

        return self.__merge_with_image(
            image,
            lambda pixel1, pixel2: max(0, pixel1 - pixel2),
        )

    def __mul__(self, value: Union[int, float]) -> Image:
        assert isinstance(
            value, (int, float)
        ), f"Unsupported operand type(s) for *: Image and {type(value).__name__}"

        return self.__merge_with_number(
            value,
            lambda pixel, value: min(9, round(pixel * value)),
        )

    def __truediv__(self, value: Union[int, float]) -> Image:
        assert isinstance(
            value, (int, float)
        ), f"Unsupported operand type(s) for /: Image and {type(value).__name__}"

        return self.__merge_with_number(
            value,
            lambda pixel, value: min(9, round(pixel / value)),
        )

    @classmethod
    def __constant_image(cls, string: str) -> Image:
        """Create a constant image from a string.

        Args:
            string (str): The string to create the image from

        Raises:
            ValueError: if an unexpected character is found in the string

        Returns:
            Image: The constant image
        """
        image = Image(string)
        image.__readonly = True
        return image

    # ASCII Image (supported 32-126)
    __ASCII = {
        " ": "00000:00000:00000:00000:00000",
        "!": "09000:09000:09000:00000:09000",
        '"': "09090:09090:00000:00000:00000",
        "#": "09000:09000:09000:00000:09000",
        "$": "09990:99009:09990:90099:09990",
        "%": "99009:90090:00900:09009:90099",
        "&": "09900:90090:09900:90090:09909",
        "'": "09000:09000:00000:00000:00000",
        "(": "00900:09000:09000:09000:00900",
        ")": "09000:00900:00900:00900:09000",
        "*": "00000:09090:00900:09090:00000",
        "+": "00000:00900:09990:00900:00000",
        ",": "00000:00000:00000:00900:09000",
        "-": "00000:00000:09990:00000:00000",
        ".": "00000:00000:00000:00900:00900",
        "/": "00009:00090:00900:09000:90000",
        "0": "09900:90090:90090:90090:09900",
        "1": "00900:09900:00900:00900:09990",
        "2": "99900:00090:09900:90000:99990",
        "3": "99990:00090:00900:90090:09900",
        "4": "00990:09090:90090:99999:00090",
        "5": "99999:90000:99990:00009:99990",
        "6": "00090:00900:09990:90009:09990",
        "7": "99999:00090:00900:09000:90000",
        "8": "09990:90009:09990:90009:09990",
        "9": "09990:90009:09990:00900:09000",
        ":": "00000:09000:00000:09000:00000",
        ";": "00000:00900:00000:00900:09000",
        "<": "00090:00900:09000:00900:00090",
        "=": "00000:09990:00000:09990:00000",
        ">": "09000:00900:00090:00900:09000",
        "?": "09990:90009:00990:00000:00900",
        "@": "09990:90009:90909:90099:09900",
        "A": "09900:90090:99990:90090:90090",
        "B": "99900:90090:99900:90090:99900",
        "C": "09990:90000:90000:90000:09990",
        "D": "99900:90090:90090:90090:99900",
        "E": "99990:90000:99900:90000:99990",
        "F": "99990:90000:99900:90000:90000",
        "G": "09990:90000:90099:90009:09990",
        "I": "99900:09000:09000:09000:99900",
        "J": "99999:00090:00090:90090:09900",
        "K": "90090:90900:99000:90900:90090",
        "L": "90000:90000:90000:90000:99990",
        "M": "90009:99099:90909:90009:90009",
        "N": "90009:99009:90909:90099:90009",
        "O": "09900:90090:90090:90090:09900",
        "P": "99900:90090:99900:90000:90000",
        "Q": "09900:90090:90090:09900:00990",
        "R": "99900:90090:99900:90090:90009",
        "S": "09990:90000:09900:00090:99900",
        "T": "99999:00900:00900:00900:00900",
        "U": "90090:90090:90090:90090:09900",
        "V": "90009:90009:90009:09090:00900",
        "W": "90009:90009:90909:99099:90009",
        "X": "90090:90090:09900:90090:90090",
        "Y": "90009:09090:00900:00900:00900",
        "Z": "99990:00900:09000:90000:99990",
        "[": "09990:09000:09000:09000:09990",
        "\\": "90000:09000:00900:00090:00009",
        "]": "09990:00090:00090:00090:09990",
        "^": "00900:09090:00000:00000:00000",
        "_": "00000:00000:00000:00000:99999",
        "`": "09000:00900:00000:00000:00000",
        "a": "00000:09990:90090:90090:09999",
        "b": "90000:90000:99900:90090:99900",
        "c": "00000:09990:90000:90000:09990",
        "d": "00090:00090:09990:90090:09990",
        "e": "09900:90090:99900:90000:09990",
        "f": "00990:09000:99900:09000:09000",
        "g": "09990:90090:09990:00090:09900",
        "h": "90000:90000:99900:90090:90090",
        "i": "09000:00000:09000:09000:09000",
        "j": "00090:00000:00090:00090:09900",
        "k": "90000:90900:99000:90900:90090",
        "l": "09000:09000:09000:09000:00990",
        "m": "00000:99099:90909:90009:90009",
        "n": "00000:99900:90090:90090:90090",
        "o": "00000:09900:90090:90090:09900",
        "p": "00000:99900:90090:99900:90000",
        "q": "00000:09990:90090:09990:00090",
        "r": "00000:09990:90000:90000:90000",
        "s": "00000:00990:09000:00900:99000",
        "t": "09000:09000:09990:09000:00999",
        "u": "00000:90090:90090:90090:09999",
        "v": "00000:90009:90009:09090:00900",
        "w": "00000:90009:90009:90909:99099",
        "x": "00000:90090:09900:09900:90090",
        "y": "00000:90009:09090:00900:99000",
        "z": "00000:99990:00900:09000:99990",
        "{": "00990:00900:09900:00900:00990",
        "|": "09000:09000:09000:09000:09000",
        "}": "99000:09000:09900:09000:99000",
        "~": "00000:00000:09900:00099:00000",
    }

    # Built-In Images
    @classmethod
    @property
    @cache
    def HEART(cls) -> Image:
        return cls.__constant_image("09090:99999:99999:09990:00900")

    @classmethod
    @property
    @cache
    def HEART_SMALL(cls) -> Image:
        return cls.__constant_image("00000:09090:09990:00900:00000")

    @classmethod
    @property
    @cache
    def HAPPY(cls) -> Image:
        return cls.__constant_image("00000:09090:00000:90009:09990")

    @classmethod
    @property
    @cache
    def SMILE(cls) -> Image:
        return cls.__constant_image("00000:00000:00000:90009:09990")

    @classmethod
    @property
    @cache
    def SAD(cls) -> Image:
        return cls.__constant_image("00000:09090:00000:09990:90009")

    @classmethod
    @property
    @cache
    def CONFUSED(cls) -> Image:
        return cls.__constant_image("00000:09090:00000:09090:90909")

    @classmethod
    @property
    @cache
    def ANGRY(cls) -> Image:
        return cls.__constant_image("90009:09090:00000:99999:90909")

    @classmethod
    @property
    @cache
    def ASLEEP(cls) -> Image:
        return cls.__constant_image("00000:99099:00000:09990:00000")

    @classmethod
    @property
    @cache
    def SURPRISED(cls) -> Image:
        return cls.__constant_image("09090:00000:00900:09090:00900")

    @classmethod
    @property
    @cache
    def SILLY(cls) -> Image:
        return cls.__constant_image("90009:00000:99999:00099:00099")

    @classmethod
    @property
    @cache
    def FABULOUS(cls) -> Image:
        return cls.__constant_image("99999:99099:00000:09090:09990")

    @classmethod
    @property
    @cache
    def MEH(cls) -> Image:
        return cls.__constant_image("99099:00000:00090:00900:09000")

    @classmethod
    @property
    @cache
    def YES(cls) -> Image:
        return cls.__constant_image("00000:00009:00090:90900:09000")

    @classmethod
    @property
    @cache
    def NO(cls) -> Image:
        return cls.__constant_image("90009:09090:00900:09090:90009")

    @classmethod
    @property
    @cache
    def CLOCK12(cls) -> Image:
        return cls.__constant_image("00900:00900:00900:00000:00000")

    @classmethod
    @property
    @cache
    def CLOCK11(cls) -> Image:
        return cls.__constant_image("09000:09900:00900:00000:00000")

    @classmethod
    @property
    @cache
    def CLOCK10(cls) -> Image:
        return cls.__constant_image("00000:99000:09900:00000:00000")

    @classmethod
    @property
    @cache
    def CLOCK9(cls) -> Image:
        return cls.__constant_image("00000:00000:99900:00000:00000")

    @classmethod
    @property
    @cache
    def CLOCK8(cls) -> Image:
        return cls.__constant_image("00000:00000:09900:99000:00000")

    @classmethod
    @property
    @cache
    def CLOCK7(cls) -> Image:
        return cls.__constant_image("00000:00000:00900:09900:09000")

    @classmethod
    @property
    @cache
    def CLOCK6(cls) -> Image:
        return cls.__constant_image("00000:00000:00900:00900:00900")

    @classmethod
    @property
    @cache
    def CLOCK5(cls) -> Image:
        return cls.__constant_image("00000:00000:00900:00990:00090")

    @classmethod
    @property
    @cache
    def CLOCK4(cls) -> Image:
        return cls.__constant_image("00000:00000:00990:00099:00000")

    @classmethod
    @property
    @cache
    def CLOCK3(cls) -> Image:
        return cls.__constant_image("00000:00000:00999:00000:00000")

    @classmethod
    @property
    @cache
    def CLOCK2(cls) -> Image:
        return cls.__constant_image("00000:00099:00990:00000:00000")

    @classmethod
    @property
    @cache
    def CLOCK1(cls) -> Image:
        return cls.__constant_image("00090:00990:00900:00000:00000")

    @classmethod
    @property
    @cache
    def ALL_CLOCKS(cls) -> tuple[Image, ...]:
        return (
            cls.CLOCK1,
            cls.CLOCK2,
            cls.CLOCK3,
            cls.CLOCK4,
            cls.CLOCK5,
            cls.CLOCK6,
            cls.CLOCK7,
            cls.CLOCK8,
            cls.CLOCK9,
            cls.CLOCK10,
            cls.CLOCK11,
            cls.CLOCK12,
        )

    @classmethod
    @property
    @cache
    def ARROW_N(cls) -> Image:
        return cls.__constant_image("00900:09990:90909:00900:00900")

    @classmethod
    @property
    @cache
    def ARROW_NE(cls) -> Image:
        return cls.__constant_image("00999:00099:00909:09000:90000")

    @classmethod
    @property
    @cache
    def ARROW_E(cls) -> Image:
        return cls.__constant_image("00900:00090:99999:00090:00900")

    @classmethod
    @property
    @cache
    def ARROW_SE(cls) -> Image:
        return cls.__constant_image("90000:09000:00909:00099:00999")

    @classmethod
    @property
    @cache
    def ARROW_S(cls) -> Image:
        return cls.__constant_image("00900:00900:90909:09990:00900")

    @classmethod
    @property
    @cache
    def ARROW_SW(cls) -> Image:
        return cls.__constant_image("00009:00090:90900:99000:99900")

    @classmethod
    @property
    @cache
    def ARROW_W(cls) -> Image:
        return cls.__constant_image("00900:09000:99999:09000:00900")

    @classmethod
    @property
    @cache
    def ARROW_NW(cls) -> Image:
        return cls.__constant_image("99900:99000:90900:00090:00009")

    @classmethod
    @property
    @cache
    def ALL_ARROWS(cls) -> tuple[Image, ...]:
        return (
            cls.ARROW_N,
            cls.ARROW_NE,
            cls.ARROW_E,
            cls.ARROW_SE,
            cls.ARROW_S,
            cls.ARROW_SW,
            cls.ARROW_W,
            cls.ARROW_NW,
        )

    @classmethod
    @property
    @cache
    def TRIANGLE(cls) -> Image:
        return cls.__constant_image("99999:00900:09090:99999:00000")

    @classmethod
    @property
    @cache
    def TRIANGLE_LEFT(cls) -> Image:
        return cls.__constant_image("90000:99000:90900:90090:99999")

    @classmethod
    @property
    @cache
    def CHESSBOARD(cls) -> Image:
        return cls.__constant_image("09090:90909:09090:90909:09090")

    @classmethod
    @property
    @cache
    def DIAMOND(cls) -> Image:
        return cls.__constant_image("00900:09090:90009:09090:00900")

    @classmethod
    @property
    @cache
    def DIAMOND_SMALL(cls) -> Image:
        return cls.__constant_image("00000:00900:09090:00900:00000")

    @classmethod
    @property
    @cache
    def SQUARE(cls) -> Image:
        return cls.__constant_image("99999:90009:90009:90009:99999")

    @classmethod
    @property
    @cache
    def SQUARE_SMALL(cls) -> Image:
        return cls.__constant_image("00000:09990:09090:09990:00000")

    @classmethod
    @property
    @cache
    def RABBIT(cls) -> Image:
        return cls.__constant_image("90900:90900:99990:99090:99990")

    @classmethod
    @property
    @cache
    def COW(cls) -> Image:
        return cls.__constant_image("90009:90009:99999:09990:00900")

    @classmethod
    @property
    @cache
    def MUSIC_CROTCHET(cls) -> Image:
        return cls.__constant_image("00900:00900:00900:99900:99900")

    @classmethod
    @property
    @cache
    def MUSIC_QUAVER(cls) -> Image:
        return cls.__constant_image("00900:00990:00909:99900:99900")

    @classmethod
    @property
    @cache
    def MUSIC_QUAVERS(cls) -> Image:
        return cls.__constant_image("09999:09009:09009:99099:99099")

    @classmethod
    @property
    @cache
    def PITCHFORK(cls) -> Image:
        return cls.__constant_image("90909:90909:99999:00900:00900")

    @classmethod
    @property
    @cache
    def XMAS(cls) -> Image:
        return cls.__constant_image("00900:09990:00900:09990:99999")

    @classmethod
    @property
    @cache
    def PACMAN(cls) -> Image:
        return cls.__constant_image("09999:99090:99900:99990:09999")

    @classmethod
    @property
    @cache
    def TARGET(cls) -> Image:
        return cls.__constant_image("00900:09990:99099:09990:00900")

    @classmethod
    @property
    @cache
    def TSHIRT(cls) -> Image:
        return cls.__constant_image("99099:99999:09990:09990:09990")

    @classmethod
    @property
    @cache
    def ROLLERSKATE(cls) -> Image:
        return cls.__constant_image("00099:00099:99999:99999:09090")

    @classmethod
    @property
    @cache
    def DUCK(cls) -> Image:
        return cls.__constant_image("09900:99900:09999:09990:00000")

    @classmethod
    @property
    @cache
    def HOUSE(cls) -> Image:
        return cls.__constant_image("00900:09990:99999:09990:09090")

    @classmethod
    @property
    @cache
    def TORTOISE(cls) -> Image:
        return cls.__constant_image("00000:09990:99999:09090:00000")

    @classmethod
    @property
    @cache
    def BUTTERFLY(cls) -> Image:
        return cls.__constant_image("99099:99999:00900:99999:99099")

    @classmethod
    @property
    @cache
    def STICKFIGURE(cls) -> Image:
        return cls.__constant_image("00900:99999:00900:09090:90009")

    @classmethod
    @property
    @cache
    def GHOST(cls) -> Image:
        return cls.__constant_image("09990:90909:99999:99999:90909")

    @classmethod
    @property
    @cache
    def SWORD(cls) -> Image:
        return cls.__constant_image("00900:00900:00900:09990:00900")

    @classmethod
    @property
    @cache
    def GIRAFFE(cls) -> Image:
        return cls.__constant_image("99000:09000:09000:09990:09090")

    @classmethod
    @property
    @cache
    def SKULL(cls) -> Image:
        return cls.__constant_image("09990:90909:99999:09990:09990")

    @classmethod
    @property
    @cache
    def UMBRELLA(cls) -> Image:
        return cls.__constant_image("09990:99999:00900:90900:99900")

    @classmethod
    @property
    @cache
    def SNAKE(cls) -> Image:
        return cls.__constant_image("99000:99099:09090:09990:00000")
