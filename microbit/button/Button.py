class Button:
    """Physical button on the Microbit board"""

    def is_pressed(self):
        """Returns True if the button is being pressed"""
        pass

    def was_pressed(self):
        """Returns True if the button has been pressed since this was last called"""
        pass
    
    def get_presses(self):
        """Returns the number of times the button has been pressed since this method was last called, then resets the count"""
        pass