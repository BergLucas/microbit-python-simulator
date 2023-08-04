from .utils import rgb
from tkinter import Canvas, Widget
from typing import Union


class ButtonWidget(Canvas):
    def __init__(self, master: Widget, size: int, buttonKey: Union[str, None] = None):
        """Create a ButtonWidget object

        Parameters:
        -----------
        master : The parent widget (Widget)

        size : The size of the button (int)

        buttonKey : The keyboard key associated to the button (optional - default: None) (Union[str, None])

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if size <= 0
        """
        if not isinstance(master, Widget):
            raise TypeError(f"invalid type : {type(master)} is not a Widget")
        if not isinstance(size, int):
            raise TypeError(f"invalid type : {type(size)} is not a int")
        if not isinstance(buttonKey, (type(None), str)):
            raise TypeError(f"invalid type : {type(buttonKey)} is not None or a str")
        if size <= 0:
            raise ValueError(f"invalid size : size can not be negative")
        Canvas.__init__(
            self,
            master,
            width=size,
            height=size,
            bg=rgb(150, 150, 150),
            highlightthickness=0,
        )
        self.reset()
        # Create round
        self.__round = self.create_oval(
            size // 4, size // 4, 3 * size // 4, 3 * size // 4, fill="black"
        )
        self.tag_bind(self.__round, "<Button-1>", lambda e: self.press())
        if buttonKey is not None:
            self.bind_all(f"<KeyPress-{buttonKey}>", lambda e: self.press())
        self.tag_bind(self.__round, "<ButtonRelease-1>", lambda e: self.release())
        if buttonKey is not None:
            self.bind_all(f"<KeyRelease-{buttonKey}>", lambda e: self.release())

    def press(self):
        """Press the button"""
        self.__is_pressed = True
        self.__was_pressed = True
        self.__get_presses += 1
        self.itemconfig(self.__round, fill=rgb(30, 30, 30))

    def release(self):
        """Release the button"""
        self.__is_pressed = False
        self.itemconfig(self.__round, fill="black")

    def reset(self):
        """Reset the state of the button"""
        self.__is_pressed = False
        self.__was_pressed = False
        self.__get_presses = 0

    def is_pressed(self) -> bool:
        """Check if the button is pressed

        Returns:
        --------
        pressed : True if the button is being pressed, False otherwise
        """
        return self.__is_pressed

    def was_pressed(self) -> bool:
        """Check if the button was pressed

        Returns:
        --------
        pressed : True if the button has been pressed since this was last called, False otherwise
        """
        pressed = self.__was_pressed
        self.__was_pressed = False
        return pressed

    def get_presses(self) -> int:
        """Returns the number of times the button has been pressed since this method was last called, then resets the count

        Returns:
        --------
        presses : The number of presses (int)
        """
        presses = self.__get_presses
        self.__get_presses = 0
        return presses
