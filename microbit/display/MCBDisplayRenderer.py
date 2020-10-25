from .MCBDisplay import MCBDisplay
from ..utils import rgb
from tkinter import Frame, Canvas, Widget

class MCBDisplayRenderer(Frame, MCBDisplay):
    def __init__(self, master: Widget, size: int):
        """ Create a MicrobitDisplayRenderer object 
        
        Parameters:
        -----------
        master : The parent widget (Widget)

        size : The size of requested display (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if size <= 0
        """
        if not isinstance(master, Widget):
            raise TypeError(f'invalid type : {type(master)} is not a Widget')
        if not isinstance(size, int):
            raise TypeError(f'invalid type : {type(size)} is not a int')
        if size <= 0:
            raise ValueError(f'invalid size : size can not be negative')
        Frame.__init__(self, master, width=size, height=size, bg='')
        # Init leds size
        led_width = 0.07
        led_height = 0.15
        space_width = (1-led_width*5)/4
        space_height = (1-led_height*5)/4
        # Create leds
        self.__leds = {}
        for lx in range(5):
            for ly in range(5):
                led = Led(self, int(led_width*size), int(led_height*size))
                led.place(relx=(space_width+led_width)*lx, rely=(space_height+led_height)*ly, relwidth=led_width, relheight=led_height)
                self.__leds[(lx,ly)] = led
        # Create the abstract pixels
        MCBDisplay.__init__(self)

    def set_pixel(self, x, y, value):
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9.
        
        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)
        
        value : The brightness (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        
        ValueError if the brightness is not between 0 and 9
        """
        MCBDisplay.set_pixel(self, x, y, value)
        if self._inDisplay(x, y):
            self.__leds[(x, y)].changeBrightness(value)

class Led(Frame):
    def __init__(self, master: Widget, width: int, height: int):
        """ Create a Led object
                
        Parameters:
        -----------
        master : The parent widget (Widget)

        height : The height of the led (int)

        width : The width of the led (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if height <= 0 or width <= 0
        """
        if not isinstance(master, Widget):
            raise TypeError(f'invalid type : {type(master)} is not a Widget')
        if not isinstance(width, int):
            raise TypeError(f'invalid type : {type(width)} is not a int')
        if not isinstance(height, int):
            raise TypeError(f'invalid type : {type(height)} is not a int')
        if height <= 0:
            raise ValueError(f'invalid height : height can not be negative')
        if width <= 0:
            raise ValueError(f'invalid width : width can not be negative')
        super().__init__(master, width=width, height=height, bg='')
        holder = Canvas(self, bg=rgb(100, 100, 100), highlightthickness=0)
        holder.place(relx=0.1, rely=0, relwidth=0.8, relheight=1)
        self.__light = Canvas(self, bg=rgb(198, 198, 198), highlightthickness=0)
        self.__light.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

    def changeBrightness(self, brightness: int):
        """ Change the brighness of the led
        
        Parameters:
        -----------
        brightness : The brightness level between 0 and 9 (int)
        
        Raises:
        -------
        TypeError if a parameter has an invalid type
        
        ValueError if brightness is not betweeen 0 and 9
        """
        if not isinstance(brightness, int):
            raise TypeError(f'invalid type : {type(brightness)} is not a int')
        if brightness < 0 or 9 < brightness:
            raise ValueError('brightness must be between 0 and 9')
        self.__light.config(bg=rgb(198+brightness*6, (9-brightness)*22, (9-brightness)*22))