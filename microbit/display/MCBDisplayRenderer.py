from .MCBDisplay import MCBDisplay
from ..utils import rgb
from tkinter import Frame, Canvas

class MCBDisplayRenderer(Frame, MCBDisplay):
    def __init__(self, master, size):
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
                led = Led(self, led_width*size, led_height*size)
                led.place(relx=(space_width+led_width)*lx, rely=(space_height+led_height)*ly, relwidth=led_width, relheight=led_height)
                self.__leds[(lx,ly)] = led
        # Create the abstract pixels
        MCBDisplay.__init__(self)

    def set_pixel(self, x, y, value):
        MCBDisplay.set_pixel(self, x, y, value)
        if self._inDisplay(x, y):
            self.__leds[(x, y)].changeBrightness(value)

class Led(Frame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, bg='')
        holder = Canvas(self, bg=rgb(100, 100, 100), highlightthickness=0)
        holder.place(relx=0.1, rely=0, relwidth=0.8, relheight=1)
        self.__light = Canvas(self, bg=rgb(198, 198, 198), highlightthickness=0)
        self.__light.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

    def changeBrightness(self, brightness):
        if brightness < 0 or 9 < brightness:
            raise ValueError('brightness must be between 0 and 9')
        self.__light.config(bg=rgb(198+brightness*6, (9-brightness)*22, (9-brightness)*22))