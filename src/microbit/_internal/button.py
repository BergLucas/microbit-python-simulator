from microbit_protocol.commands.microbit import MicrobitButtonIsPressedCommand
from microbit_protocol.commands import MicrobitCommand
from typing import Protocol


class Button(Protocol):
    """Represents a button.

    .. note::
        This class is not actually available to the user, it is only used by the two button instances, which are provided already initialized.
    """

    def is_pressed(self) -> bool:
        """Returns `True` if the specified button button is currently being held down, and `False` otherwise.

        Returns:
            bool: `True` if the button is being pressed, `False` otherwise.
        """
        ...

    def was_pressed(self) -> bool:
        """Returns `True` or `False` to indicate if the button was pressed (went from up to down) since the device started or the last time this method was called.

        Calling this method will clear the press state so that the button must be pressed again before this method will return `True` again.

        Returns:
            bool: `True` if the button has been pressed since this method was last called, `False` otherwise.
        """
        ...

    def get_presses(self) -> int:
        """Returns the running total of button presses, and resets this total to zero before returning.

        Returns:
            int: The number of times the button has been pressed since this method was last called, then resets the count.
        """
        ...


class MicrobitButton(Button):
    def __init__(self) -> None:
        self.__is_pressed = False
        self.__was_pressed = False
        self.__get_presses = 0

    def execute(self, command: MicrobitCommand) -> None:
        if isinstance(command, MicrobitButtonIsPressedCommand):
            if not self.__is_pressed and command.is_pressed:
                self.__was_pressed = True
                self.__get_presses += 1
            self.__is_pressed = command.is_pressed

        raise ValueError(f"Unknown command: {command}")

    def is_pressed(self) -> bool:
        return self.__is_pressed

    def was_pressed(self) -> bool:
        pressed = self.__was_pressed
        self.__was_pressed = False
        return pressed

    def get_presses(self) -> int:
        presses = self.__get_presses
        self.__get_presses = 0
        return presses
