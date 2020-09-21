from .Button import Button
class MCBButton(Button):
    """Physical button on the Microbit board"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.__is_pressed = False
        self.__was_pressed = False
        self.__get_presses = 0

    def press(self):
        self.__is_pressed = True
        self.__was_pressed = True
        self.__get_presses += 1
    
    def release(self):
        self.__is_pressed = False

    def is_pressed(self):
        """Returns True if the button is being pressed"""
        return self.__is_pressed

    def was_pressed(self):
        """Returns True if the button has been pressed since this was last called"""
        pressed = self.__was_pressed
        self.__was_pressed = False
        return pressed
    
    def get_presses(self):
        """Returns the number of times the button has been pressed since this method was last called, then resets the count"""
        presses = self.__get_presses
        self.__get_presses = 0
        return presses