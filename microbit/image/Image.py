class Image:
    """Dummy image class for autocompletion"""

class Image:
    def __init__(self, *args, width: int = None, height: int = None, buffer: bytearray = None):
        """ Base image class
        Image() - Create a blank 5x5 image

        Image(string) - Create an image by parsing the string, a single character returns that glyph

        Image(width, height) - Create a blank image of given size

        Image(width, height, buffer) - Create an image from the given buffer

        Parameters:
        -----------
        string : A string which represents the image or a single character (str)

        width : The width of the image (int) (optional)

        height : The height of the image (int) (optional)

        buffer : A bytearray which represents the image (bytearray) (optionnal)

        Raises:
        -------
        TypeError if a parameters has an invalid type

        IndexError if the size is invalid
        """
        # Create empty image
        self.__pixels = {}
        self._readonly = False
        # Check args
        args_length = len(args)
        # 1 argument
        if args_length == 1:
            string = args[0]
            # Check if glyph
            if len(string) == 1:
                string = Image._ASCII[string if string in Image._ASCII else '?']
            # Create the image
            self.__convertString(string)
        # 0, 2 or 3 arguments
        elif args_length in [0, 2, 3]:
            # 0 argument
            if args_length == 0:
                width = 5 if width == None else width
                height = 5 if height == None else height
            # 2 arguments
            else:
                width = args[0]
                height = args[1]
                # Check if width and height are positive integer
                if not isinstance(width, int) or not isinstance(height, int):
                    raise TypeError('size must be an integer')
                elif width < 0 or height < 0:
                    raise IndexError('size must be positive')

            # 3 arguments
            if args_length == 3:
                buffer = args[2]
                # Check if buffer exists and is valid
                if not isinstance(buffer, bytearray) or (isinstance(buffer, bytearray) and len(buffer) != width*height):
                    raise TypeError('image data is incorrect size or type')

            # Create the image
            self.__width = width
            self.__height = height
            for y in range(height):
                for x in range(width):
                    if buffer != None:
                        self.set_pixel(x, y, buffer[x+y*5])
                    else:
                        self.set_pixel(x, y, 0)

        # Invalid arguments
        else:
            raise IndexError('Image() takes 0 to 3 arguments')

    def width(self) -> int:
        """Gets the number of columns in an image
        
        Returns:
        --------
        width : The width of the image (int)"""
        return self.__width

    def height(self) -> int:
        """Gets the number of rows in an image
                
        Returns:
        --------
        height : The height of the image (int)
        """
        return self.__height

    def set_pixel(self, x: int, y: int, value: int):
        """Sets the brightness of a pixel at the given position. Cannot be used on inbuilt images.
        
        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)
        
        value : The brightness (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the x or y are outside the image
        
        ValueError if the brightness is not between 0 and 9
        """
        if self._readonly:
            raise AttributeError('the image cannot be modified')
        if not self.__inImage(x, y):
            raise ValueError('invalid index')
        if not isinstance(value, int):
            raise TypeError('%f brightness is not an integer' % value)
        if value < 0 or 9 < value:
            raise ValueError('brightness out of bounds')
        self.__pixels[(x, y)] = value

    def get_pixel(self, x: int, y: int) -> int:
        """Returns the brightness of the pixel located at x,y
        
        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        Notes:
        ------
        Returns 0 if x or y is outside the image
        """
        if not self.__inImage(x, y):
            return 0
        else:
            return int(self.__pixels[(x, y)])

    def shift_left(self, n: int):
        """Returns a new image created by shifting the image left by n columns
        
        Parameters:
        -----------
        n : The number of shifting (int)

        Returns:
        --------
        image : The shifted image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(n, int):
            raise TypeError(f'invalid type : {type(n)} is not a int')
        image = Image(width=self.__width, height=self.__height)
        image.blit(self, n, 0, self.__width, self.__height)
        return image

    def shift_right(self, n: int):
        """Returns a new image created by shifting the image right by n columns

        Parameters:
        -----------
        n : The number of shifting (int)

        Returns:
        --------
        image : The shifted image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        return self.shift_left(-n)

    def shift_up(self, n: int):
        """Returns a new image created by shifting the image up by n rows
        
        Parameters:
        -----------
        n : The number of shifting (int)

        Returns:
        --------
        image : The shifted image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        image = Image(width=self.__width, height=self.__height)
        image.blit(self, 0, n, self.__width, self.__height)
        return image

    def shift_down(self, n: int):
        """Returns a new image created by shifting the image down by n rows
        
        Parameters:
        -----------
        n : The number of shifting (int)

        Returns:
        --------
        image : The shifted image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        return self.shift_up(-n)

    def crop(self, x: int, y: int, w: int, h: int):
        """Return a new image by cropping the picture to a width of w and a height of h, starting with the pixel at column x and row y.
        
        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)

        w : The width (int)

        h : The height (int)

        Returns:
        --------
        image : The cropped image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        image = Image(width=w, height=h)
        image.blit(self, x, y, w, h)
        return image

    def copy(self):
        """ Return a copy of the image 
        
        Returns:
        --------
        image : The copy of the image (Image)
        """
        image = Image(width=self.__width, height=self.__height)
        for [x, y] in self.__pixels:
            image.set_pixel(x, y, self.__pixels[(x, y)])
        return image

    def invert(self):
        """Return a new image by inverting the brightness of the pixels in the source image.
        
        Returns:
        --------
        image : The image with inverted brightness (Image)
        """
        image = Image(width=self.__width, height=self.__height)
        for [x, y] in self.__pixels:
            image.set_pixel(x, y, 9-self.get_pixel(x, y))
        return image

    def fill(self, value: int):
        """Set the brightness of all the pixels in the image to the value, which has to be between 0 (dark) and 9 (bright). Cannot be used on inbuilt images.
        
        Parameters:
        -----------
        value : The brightness used to fill the image (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the value is not between 0 and 9

        Exception if the image is readonly
        """
        if not isinstance(value, int):
            raise TypeError(f'invalid type : {type(value)} is not a int')
        if 0 <= value and value < 10:
            raise ValueError(f'{value} is not between 0 and 9')
        if self._readonly:
            raise Exception('could not fill a readonly image')
        for [x, y] in self.__pixels:
            self.set_pixel(x, y, value)

    def blit(self, src: Image, x: int, y: int, w: int, h: int, xdest: int = 0, ydest:int = 0):
        """Copy the rectangle defined by x, y, w, h from the image src into this image at xdest, ydest. Areas in the source rectangle, but outside the source image are treated as having a value of 0.

        Parameters:
        -----------
        src : The source image (Image)

        x : The x position (int)

        y : The y position (int)

        w : The width (int)

        h : The height (int)

        xdest : The x destination position (optional - default: 0) (int)

        ydest : The y destination position (optional - default: 0) (int)
        """
        # Check the source image
        if not isinstance(src, Image):
            raise TypeError('src must be a Image')
        # Check the parameters
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError('sources coords must be integer')
        if not isinstance(xdest, int) or not isinstance(ydest, int):
            raise TypeError('destinations coords must be integer')
        if not isinstance(w, int) or not isinstance(h, int):
            raise TypeError('size must be integer')
        # Get the destination coord starting by xdest 
        for dx in range(max(0, xdest), min(xdest+w, self.__width)):
            for dy in range(max(0, ydest), min(ydest+h, self.__height)):
                # Get the source coord
                sx = dx - (xdest - x)
                sy = dy - (ydest - y)
                # Copy the value to the dest image
                value = src.get_pixel(sx, sy)
                self.set_pixel(dx, dy, value)

    def __inImage(self, x: int, y: int) -> bool:
        """ Check if the position is in the image

        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)

        Returns:
        --------
        inside : True if the position is inside, False otherwise

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(x, int):
            raise TypeError(f'invalid type : {type(x)} is not a int')
        if not isinstance(y, int):
            raise TypeError(f'invalid type : {type(y)} is not a int')
        return 0 <= x and x < self.__width and 0 <= y and y < self.__height

    def __convertString(self, string: str):
        """ Read the string and set the pixels at the requested brightness
        
        Parameters:
        -----------
        string : The string (str)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the string is invalid
        """
        if not isinstance(string, str):
            raise TypeError(f'invalid type : {type(string)} is not a str')
        lines = string.replace('\n', ':').split(':')
        # Get the length and the width
        self.__width = 0
        for line in lines:
            self.__width = max(self.__width, len(line))
        self.__height = len(lines)
        # Create the image
        for y, line in enumerate(lines):
            for x in range(self.__width):
                # Check if space or unfinished line
                if len(line) <= x or line[x] == ' ':
                    number = 0
                # Check if the char is a number
                elif not line[x].isdigit():
                    raise ValueError('%s has a invalid character %s' % (line, line[x]))
                # Check if the number is valid
                else:
                    number = int(line[x])
                # Add the number
                self.set_pixel(x, y, number)

    def __sum(self, other, add):
        """ Add or sub the image with another image 

        Parameters:
        -----------
        other : The other image (Image)

        add : Add if True, sub otherwise (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the images have different size
        """
        # Check add type
        if not isinstance(add, bool):
            raise TypeError('add must be a boolean')
        # Check type
        if not isinstance(other, Image):
            raise TypeError('unsupported operand type(s) for %s: ‘Image’ and ‘%s’' % ('+' if add else '-', type(other)))
        # Check size
        if self.__width != other.width() or self.__height != other.height():
            raise ValueError('images must be the same size')
        # Create the new image
        image = Image(width=self.__width, height=self.__height)
        for y in range(self.__height):
            for x in range(self.__width):
                if add:
                    value = min(9, self.get_pixel(x, y) + other.get_pixel(x, y))
                else:
                    value = max(0, self.get_pixel(x, y) - other.get_pixel(x, y))
                image.set_pixel(x, y, value)
        return image

    def __dim(self, value, mul):
        """ Multiply every position brigthness by a multiplier

        Parameters:
        -----------
        value : The value of the multiplier (float)

        mul : Multiply if True, divise otherwise (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the images have different size

        ValueError if the brightness multiplier is negative
        """
        # Check mul type
        if not isinstance(mul, bool):
            raise TypeError('mul must be a boolean')
        # Check type
        if not isinstance(value, (int, float)):
            raise TypeError('unsupported operand type(s) for %s: ‘Image’ and ‘%s’' % ('*' if mul else '/', type(value)))
        # Check value value
        if value < 0:
            raise ValueError('brightness multiplier must not be negative')
        # Create the new image
        image = Image(width=self.__width, height=self.__height)
        for y in range(self.__height):
            for x in range(self.__width):
                value = round(self.get_pixel(x, y) * value)
                value = max(0, min(9, value))
                image.set_pixel(x, y, value)
        return image

    def __repr__(self):
        string = "Image(\n      '"
        for y in range(self.__height):
            for x in range(self.__width):
                string += str(self.__pixels[(x, y)])
            string += "'\n      '"
        return string[:-7] + ")"

    def __str__(self):
        string = "Image('"
        for y in range(self.__height):
            for x in range(self.__width):
                string += str(self.__pixels[(x, y)])
            string += ":'"
        return string[:-2] + "')"
    
    def __sub__(self, other):
        return self.__sum(other, False)

    def __add__(self, other):
        return self.__sum(other, True)

    def __mul__(self, other):
        return self.__dim(other, True)

    def __truediv__(self, other):
        return self.__dim(1/other, False)

    @staticmethod
    def _constImage(string):
        """ Create an readonly image from a string
        
        Parameters:
        -----------
        string : The string (str)

        Returns:
        --------
        image : The constant image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the string is invalid
        """
        image = Image(string)
        image._readonly = True
        return image

    _ASCII = {}

    # For autocompletion
    HEART = Image()
    HEART_SMALL = Image()
    HAPPY = Image()
    SMILE = Image()
    SAD = Image()
    CONFUSED = Image()
    ANGRY = Image()
    ASLEEP = Image()
    SURPRISED = Image()
    SILLY = Image()
    FABULOUS = Image()
    MEH = Image()

    YES = Image()
    NO = Image()

    CLOCK12 = Image()
    CLOCK11 = Image()
    CLOCK10 = Image()
    CLOCK9 = Image()
    CLOCK8 = Image()
    CLOCK7 = Image()
    CLOCK6 = Image()
    CLOCK5 = Image()
    CLOCK4 = Image()
    CLOCK3 = Image()
    CLOCK2 = Image()
    CLOCK1 = Image()
    ALL_CLOCKS = [CLOCK1, CLOCK2, CLOCK3, CLOCK4, CLOCK5, CLOCK6, CLOCK7, CLOCK8, CLOCK9, CLOCK10, CLOCK11, CLOCK12]

    ARROW_N = Image()
    ARROW_NE = Image()
    ARROW_E = Image()
    ARROW_SE = Image()
    ARROW_S = Image()
    ARROW_SW = Image()
    ARROW_W = Image()
    ARROW_NW = Image()
    ALL_ARROWS = [ARROW_N, ARROW_NE, ARROW_E, ARROW_SE, ARROW_S, ARROW_SW, ARROW_W, ARROW_NW]

    TRIANGLE = Image()
    TRIANGLE_LEFT = Image()
    CHESSBOARD = Image()
    DIAMOND = Image()
    DIAMOND_SMALL = Image()
    SQUARE = Image()
    SQUARE_SMALL = Image()

    RABBIT = Image()
    COW = Image()

    MUSIC_CROTCHET = Image()
    MUSIC_QUAVER = Image()
    MUSIC_QUAVERS = Image()

    PITCHFORK = Image()

    XMAS = Image()

    PACMAN = Image()
    TARGET = Image()
    TSHIRT = Image()
    ROLLERSKATE = Image()
    DUCK = Image()
    HOUSE = Image()
    TORTOISE = Image()
    BUTTERFLY = Image()
    STICKFIGURE = Image()
    GHOST = Image()
    SWORD = Image()
    GIRAFFE = Image()
    SKULL = Image()
    UMBRELLA = Image()
    SNAKE = Image()

# Built-In Image
Image.HEART = Image._constImage('09090:99999:99999:09990:00900')
Image.HEART_SMALL = Image._constImage('00000:09090:09990:00900:00000')
Image.HAPPY = Image._constImage('00000:09090:00000:90009:09990')
Image.SMILE = Image._constImage('00000:00000:00000:90009:09990')
Image.SAD = Image._constImage('00000:09090:00000:09990:90009')
Image.CONFUSED = Image._constImage('00000:09090:00000:09090:90909')
Image.ANGRY = Image._constImage('90009:09090:00000:99999:90909')
Image.ASLEEP = Image._constImage('00000:99099:00000:09990:00000')
Image.SURPRISED = Image._constImage('09090:00000:00900:09090:00900')
Image.SILLY = Image._constImage('90009:00000:99999:00099:00099')
Image.FABULOUS = Image._constImage('99999:99099:00000:09090:09990')
Image.MEH = Image._constImage('99099:00000:00090:00900:09000')

Image.YES = Image._constImage('00000:00009:00090:90900:09000')
Image.NO = Image._constImage('90009:09090:00900:09090:90009')

Image.CLOCK12 = Image._constImage('00900:00900:00900:00000:00000')
Image.CLOCK11 = Image._constImage('09000:09900:00900:00000:00000')
Image.CLOCK10 = Image._constImage('00000:99000:09900:00000:00000')
Image.CLOCK9 = Image._constImage('00000:00000:99900:00000:00000')
Image.CLOCK8 = Image._constImage('00000:00000:09900:99000:00000')
Image.CLOCK7 = Image._constImage('00000:00000:00900:09900:09000')
Image.CLOCK6 = Image._constImage('00000:00000:00900:00900:00900')
Image.CLOCK5 = Image._constImage('00000:00000:00900:00990:00090')
Image.CLOCK4 = Image._constImage('00000:00000:00990:00099:00000')
Image.CLOCK3 = Image._constImage('00000:00000:00999:00000:00000')
Image.CLOCK2 = Image._constImage('00000:00099:00990:00000:00000')
Image.CLOCK1 = Image._constImage('00090:00990:00900:00000:00000')
Image.ALL_CLOCKS = [
    Image.CLOCK1,
    Image.CLOCK2,
    Image.CLOCK3,
    Image.CLOCK4,
    Image.CLOCK5,
    Image.CLOCK6,
    Image.CLOCK7,
    Image.CLOCK8,
    Image.CLOCK9,
    Image.CLOCK10,
    Image.CLOCK11,
    Image.CLOCK12
]

Image.ARROW_N = Image._constImage('00900:09990:90909:00900:00900')
Image.ARROW_NE = Image._constImage('00999:00099:00909:09000:90000')
Image.ARROW_E = Image._constImage('00900:00090:99999:00090:00900')
Image.ARROW_SE = Image._constImage('90000:09000:00909:00099:00999')
Image.ARROW_S = Image._constImage('00900:00900:90909:09990:00900')
Image.ARROW_SW = Image._constImage('00009:00090:90900:99000:99900')
Image.ARROW_W = Image._constImage('00900:09000:99999:09000:00900')
Image.ARROW_NW = Image._constImage('99900:99000:90900:00090:00009')
Image.ALL_ARROWS = [
    Image.ARROW_N,
    Image.ARROW_NE,
    Image.ARROW_E,
    Image.ARROW_SE,
    Image.ARROW_S,
    Image.ARROW_SW,
    Image.ARROW_W,
    Image.ARROW_NW
]

Image.TRIANGLE = Image._constImage('99999:00900:09090:99999:00000')
Image.TRIANGLE_LEFT = Image._constImage('90000:99000:90900:90090:99999')
Image.CHESSBOARD = Image._constImage('09090:90909:09090:90909:09090')
Image.DIAMOND = Image._constImage('00900:09090:90009:09090:00900')
Image.DIAMOND_SMALL = Image._constImage('00000:00900:09090:00900:00000')
Image.SQUARE = Image._constImage('99999:90009:90009:90009:99999')
Image.SQUARE_SMALL = Image._constImage('00000:09990:09090:09990:00000')

Image.RABBIT = Image._constImage('90900:90900:99990:99090:99990')
Image.COW = Image._constImage('90009:90009:99999:09990:00900')

Image.MUSIC_CROTCHET = Image._constImage('00900:00900:00900:99900:99900')
Image.MUSIC_QUAVER = Image._constImage('00900:00990:00909:99900:99900')
Image.MUSIC_QUAVERS = Image._constImage('09999:09009:09009:99099:99099')

Image.PITCHFORK = Image._constImage('90909:90909:99999:00900:00900')

Image.XMAS = Image._constImage('00900:09990:00900:09990:99999')

Image.PACMAN = Image._constImage('09999:99090:99900:99990:09999')
Image.TARGET = Image._constImage('00900:09990:99099:09990:00900')
Image.TSHIRT = Image._constImage('99099:99999:09990:09990:09990')
Image.ROLLERSKATE = Image._constImage('00099:00099:99999:99999:09090')
Image.DUCK = Image._constImage('09900:99900:09999:09990:00000')
Image.HOUSE = Image._constImage('00900:09990:99999:09990:09090')
Image.TORTOISE = Image._constImage('00000:09990:99999:09090:00000')
Image.BUTTERFLY = Image._constImage('99099:99999:00900:99999:99099')
Image.STICKFIGURE = Image._constImage('00900:99999:00900:09090:90009')
Image.GHOST = Image._constImage('09990:90909:99999:99999:90909')
Image.SWORD = Image._constImage('00900:00900:00900:09990:00900')
Image.GIRAFFE = Image._constImage('99000:09000:09000:09990:09090')
Image.SKULL = Image._constImage('09990:90909:99999:09990:09990')
Image.UMBRELLA = Image._constImage('09990:99999:00900:90900:99900')
Image.SNAKE = Image._constImage('99000:99099:09090:09990:00000')

# ASCII Image (supported 32-126)
Image._ASCII = {
    ' ' : '00000:00000:00000:00000:00000',
    '!' : '09000:09000:09000:00000:09000',
    '"' : '09090:09090:00000:00000:00000',
    '#' : '09000:09000:09000:00000:09000',
    '$' : '09990:99009:09990:90099:09990',
    '%' : '99009:90090:00900:09009:90099',
    '&' : '09900:90090:09900:90090:09909',
    "'" : '09000:09000:00000:00000:00000',
    '(' : '00900:09000:09000:09000:00900',
    ')' : '09000:00900:00900:00900:09000',
    '*' : '00000:09090:00900:09090:00000',
    '+' : '00000:00900:09990:00900:00000',
    ',' : '00000:00000:00000:00900:09000',
    '-' : '00000:00000:09990:00000:00000',
    '.' : '00000:00000:00000:00900:09000',
    '/' : '00009:00090:00900:09000:90000',
    '0' : '09900:90090:90090:90090:09900',
    '1' : '00900:09900:00900:00900:09990',
    '2' : '99900:00090:09900:90000:99990',
    '3' : '99990:00090:00900:90090:09900',
    '4' : '00990:09090:90090:99999:00090',
    '5' : '99999:90000:99990:00009:99990',
    '6' : '00090:00900:09990:90009:09990',
    '7' : '99999:00090:00900:09000:90000',
    '8' : '09990:90009:09990:90009:09990',
    '9' : '09990:90009:09990:00900:09000',
    ':' : '00000:09000:00000:09000:00000',
    ';' : '00000:00900:00000:00900:09000',
    '<' : '00090:00900:09000:00900:00090',
    '=' : '00000:09990:00000:09990:00000',
    '>' : '09000:00900:00090:00900:09000',
    '?' : '09990:90009:00990:00000:00900',
    '@' : '09990:90009:90909:90099:09900',
    'A' : '09900:90090:99990:90090:90090',
    'B' : '99900:90090:99900:90090:99900',
    'C' : '09990:90000:90000:90000:09990',
    'D' : '99900:90090:90090:90090:99900',
    'E' : '99990:90000:99900:90000:99990',
    'F' : '99990:90000:99900:90000:90000',
    'G' : '09990:90000:90099:90009:09990',
    'I' : '99900:09000:09000:09000:99900',
    'J' : '99999:00090:00090:90090:09900',
    'K' : '90090:90900:99000:90900:90090',
    'L' : '90000:90000:90000:90000:99990',
    'M' : '90009:99099:90909:90009:90009',
    'N' : '90009:99009:90909:90099:90009',
    'O' : '09900:90090:90090:90090:09900',
    'P' : '99900:90090:99900:90000:90000',
    'Q' : '09900:90090:90090:09900:00990',
    'R' : '99900:90090:99900:90090:90009',
    'S' : '09990:90000:09900:00090:99900',
    'T' : '99999:00900:00900:00900:00900',
    'U' : '90090:90090:90090:90090:09900',
    'V' : '90009:90009:90009:09090:00900',
    'W' : '90009:90009:90909:99099:90009',
    'X' : '90090:90090:09900:90090:90090',
    'Y' : '90009:09090:00900:00900:00900',
    'Z' : '99990:00900:09000:90000:99990',
    '[' : '09990:09000:09000:09000:09990',
    '\\' : '90000:09000:00900:00090:00009',
    ']' : '09990:00090:00090:00090:09990',
    '^' : '00900:09090:00000:00000:00000',
    '_' : '00000:00000:00000:00000:99999',
    '`' : '09000:00900:00000:00000:00000',
    'a' : '00000:09990:90090:90090:09999',
    'b' : '90000:90000:99900:90090:99900',
    'c' : '00000:09990:90000:90000:09990',
    'd' : '00090:00090:09990:90090:09990',
    'e' : '09900:90090:99900:90000:09990',
    'f' : '00990:09000:99900:09000:09000',
    'g' : '09990:90090:09990:00090:09900',
    'h' : '90000:90000:99900:90090:90090',
    'i' : '09000:00000:09000:09000:09000',
    'j' : '00090:00000:00090:00090:09900',
    'k' : '90000:90900:99000:90900:90090',
    'l' : '09000:09000:09000:09000:00990',
    'm' : '00000:99099:90909:90009:90009',
    'n' : '00000:99900:90090:90090:90090',
    'o' : '00000:09900:90090:90090:09900',
    'p' : '00000:99900:90090:99900:90000',
    'q' : '00000:09990:90090:09990:00090',
    'r' : '00000:09990:90000:90000:90000',
    's' : '00000:00990:09000:00900:99000',
    't' : '09000:09000:09990:09000:00999',
    'u' : '00000:90090:90090:90090:09999',
    'v' : '00000:90009:90009:09090:00900',
    'w' : '00000:90009:90009:90909:99099',
    'x' : '00000:90090:09900:09900:90090',
    'y' : '00000:90009:09090:00900:99000',
    'z' : '00000:99990:00900:09000:99990',
    '{' : '00990:00900:09900:00900:00990',
    '|' : '09000:09000:09000:09000:09000',
    '}' : '99000:09000:09900:09000:99000',
    '~' : '00000:00000:09900:00099:00000'
}