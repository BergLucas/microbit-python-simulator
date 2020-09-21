import time
from .utils import rgb
from .button.MCBButtonRenderer import MCBButtonRenderer
from .display.MCBDisplayRenderer import MCBDisplayRenderer
from .accelerometer.MCBAccelerometerRenderer import MCBAccelerometerRenderer
from tkinter import Tk, Frame, Canvas

class MicrobitSimulator(Tk):
    def __init__(self, width=700, height=500):
        Tk.__init__(self)
        self.geometry(f'{width}x{height}')
        self.title('Microbit Simulator')
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.resizable(0, 0)
        # General properties
        self.__start = time.time()
        self.__temperature = 0
        # Create background
        self.__background = Canvas(self, bg=rgb(25, 25 , 25), highlightthickness=0)
        self.__background.place(x=0, y=0, width=width, height=height)
        # Create display
        x_space = 0.4
        size = width*x_space
        y_space = size/height
        self.__display = MCBDisplayRenderer(self.__background, size)
        self.__display.place(relx=(1-x_space)/2, rely=(1-y_space)/2)
        # Setup buttons
        self.__buttons = {}
        buttons_size = width*0.15
        rely = (1-buttons_size/height)/2
        # Setup button a
        button_a = MCBButtonRenderer(self.__background, buttons_size)
        button_a.place(relx=0.05, rely=rely)
        self.__buttons['A'] = button_a
        # Setup button b
        button_b = MCBButtonRenderer(self.__background, buttons_size)
        button_b.place(relx=0.80, rely=rely)
        self.__buttons['B'] = button_b
        # Setup accelerometer
        self.geometry(f'{900}x{height}')
        self.__accelerometer = MCBAccelerometerRenderer(self, 200, height)
        self.__accelerometer.place(x=700, y=0)

    def quit(self):
        # Stop the threads
        self.__display.shutdown()
        super().quit()

    def getDisplay(self):
        return self.__display

    def getAccelerometer(self):
        return self.__accelerometer

    def getButton(self, name):
        return self.__buttons[name]

    def panic(self, error_code):
        self.__display.scroll(error_code, monospace=True, loop=True)

    def reset(self):
        self.__start = time.time()
        self.__display.clear()
        for button_id in self.__buttons:
            self.__buttons[button_id].reset()

    def sleep(self, milliseconds):
        time.sleep(milliseconds/1000)

    def running_time(self):
        return time.time() - self.__start

    def temperature(self):
        return self.__temperature