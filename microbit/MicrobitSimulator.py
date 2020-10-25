import time
from .utils import rgb
from .Settings import *
from .button.MCBButtonRenderer import MCBButtonRenderer
from .display.MCBDisplayRenderer import MCBDisplayRenderer
from .accelerometer.MCBAccelerometerRenderer import MCBAccelerometerRenderer
from tkinter import Tk, Frame, Canvas

class MicrobitSimulator(Tk):
    def __init__(self, width: int = 700, height: int = 500):
        """ Create a MicrobitSimulator window
        
        Parameters:
        -----------
        width : The width of the window (optional - default: 700) (int)

        height : The height of the window (optional - default: 500) (int)
        """
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
        self.__display = MCBDisplayRenderer(self.__background, int(size))
        self.__display.place(relx=(1-x_space)/2, rely=(1-y_space)/2)
        # Setup buttons
        self.__buttons = {}
        buttons_size = width*0.15
        rely = (1-buttons_size/height)/2
        # Setup button a
        button_a = MCBButtonRenderer(self.__background, int(buttons_size), BUTTON_A)
        button_a.place(relx=0.05, rely=rely)
        self.__buttons['A'] = button_a
        # Setup button b
        button_b = MCBButtonRenderer(self.__background, int(buttons_size), BUTTON_B)
        button_b.place(relx=0.80, rely=rely)
        self.__buttons['B'] = button_b
        # Setup accelerometer
        self.geometry(f'{900}x{height}')
        self.__accelerometer = MCBAccelerometerRenderer(self, 200, int(height))
        self.__accelerometer.place(x=700, y=0)

    def quit(self):
        """ Quit the MicrobitSimulator window """
        # Stop the threads
        self.__display.shutdown()
        super().quit()

    def getDisplay(self) -> MCBDisplayRenderer:
        """ Get the display object of the MicrobitSimulator 
        
        Returns:
        --------
        display : The display of the MicrobitSimulator (MCBDisplayRenderer)
        """
        return self.__display

    def getAccelerometer(self) -> MCBAccelerometerRenderer:
        """ Get the accelerometer object of the MicrobitSimulator 
        
        Returns:
        --------
        accelerometer : The accelerometer of the MicrobitSimulator (MCBDisplayRenderer)
        """
        return self.__accelerometer

    def getButton(self, name: str) -> MCBButtonRenderer:
        """ Get the requested button object of the MicrobitSimulator 
        
        Parameters:
        -----------
        name : The name of the requested button (str)

        Returns:
        --------
        button : The accelerometer of the MicrobitSimulator (MCBButtonRenderer)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the name is invalid
        """
        if not isinstance(name, str):
            raise TypeError(f'invalid type : {type(name)} is not a str')
        if name not in self.__buttons:
            raise ValueError(f'The button {name} does not exist')
        return self.__buttons[name]

    def panic(self, error_code: int):
        """ Display an error code on the display
        
        Parameters:
        -----------
        error_code : The code of the error (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the error code is not between 0 and 255
        """
        if not isinstance(error_code, int):
            raise TypeError(f'invalid type : {type(error_code)} is not a int')
        if error_code < 0 or 255 < error_code:
            raise ValueError('the error code must be between 0 and 255')
        self.__display.scroll(error_code, monospace=True, loop=True)

    def reset(self):
        """ Reset the MicrobitSimulator """
        self.__start = time.time()
        self.__display.clear()
        for button_id in self.__buttons:
            self.__buttons[button_id].reset()

    def sleep(self, milliseconds: int):
        """ Wait a number of milliseconds
        
        Parameters:
        -----------
        milliseconds : The number of milliseconds (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the time is negative
        """
        if not isinstance(milliseconds, int):
            raise TypeError(f'invalid type : {type(milliseconds)} is not a int')
        if milliseconds < 0:
            raise ValueError('the milliseconds can not be negative')
        time.sleep(milliseconds/1000)

    def running_time(self) -> int:
        """ Return the running time of the MicrobitSimulator in milliseconds 
        
        Returns:
        --------
        run_time : The running time of the MicrobitSimulator in milliseconds (int)
        """
        return time.time() - self.__start

    def temperature(self) -> int:
        """ Return the temperature
        
        Returns:
        --------
        temperature : The temperature (int)
        """
        return self.__temperature