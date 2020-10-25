from .Button import Button
class MCBButton(Button):
    def __init__(self):
        """Physical button on the Microbit board"""
        self.reset()

    def reset(self):
        """ Reset the state of the button """
        self.__is_pressed = False
        self.__was_pressed = False
        self.__get_presses = 0

    def press(self):
        """ Press the button """
        self.__is_pressed = True
        self.__was_pressed = True
        self.__get_presses += 1
    
    def release(self):
        """ Release the button """
        self.__is_pressed = False

    def is_pressed(self) -> bool:
        """ Check if the button is pressed

        Returns:
        --------
        pressed : True if the button is being pressed, False otherwise
        """
        return self.__is_pressed

    def was_pressed(self) -> bool:
        """ Check if the button was pressed

        Returns:
        --------
        pressed : True if the button has been pressed since this was last called, False otherwise
        """
        pressed = self.__was_pressed
        self.__was_pressed = False
        return pressed
    
    def get_presses(self) -> int:
        """ Returns the number of times the button has been pressed since this method was last called, then resets the count
        
        Returns:
        --------
        presses : The number of presses (int)
        """
        presses = self.__get_presses
        self.__get_presses = 0
        return presses