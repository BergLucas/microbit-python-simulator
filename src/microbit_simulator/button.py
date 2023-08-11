from tkinter import Canvas, Misc
from typing import Literal, Optional

from microbit_protocol.commands.microbit import MicrobitButtonIsPressedCommand
from microbit_protocol.exceptions import CommunicationClosedError
from microbit_protocol.peer import MicrobitPeer

from microbit_simulator.utils import rgb

BUTTON_A = "a"
BUTTON_B = "b"


class MicrobitButton(Canvas):
    """A button widget for the micro:bit."""

    def __init__(
        self,
        master: Misc,
        size: int,
        instance: Literal["button_a", "button_b"],
        button_key: str,
    ) -> None:
        """Initialises self to a MicrobitButton.

        Args:
            master (Misc): The parent widget.
            size (int): The size of the button. Must be positive.
            instance (Literal["button_a", "button_b"]): The button instance.
            button_key (str): The button key.
        """
        assert size > 0

        Canvas.__init__(
            self,
            master,
            width=size,
            height=size,
            bg=rgb(150, 150, 150),
            highlightthickness=0,
        )

        self.__is_pressed = False
        self.__instance: Literal["button_a", "button_b"] = instance
        self.__peer: Optional[MicrobitPeer] = None

        self.__round = self.create_oval(
            size // 4, size // 4, 3 * size // 4, 3 * size // 4, fill="black"
        )

        self.tag_bind(self.__round, "<Button-1>", lambda _: self.press())
        self.tag_bind(self.__round, "<ButtonRelease-1>", lambda _: self.release())

        self.bind_all(f"<KeyPress-{button_key}>", lambda _: self.press())
        self.bind_all(f"<KeyRelease-{button_key}>", lambda _: self.release())

    @property
    def peer(self) -> Optional[MicrobitPeer]:
        """Return the microbit peer.

        Returns:
            Optional[MicrobitPeer]: The microbit peer.
        """
        return self.__peer

    @peer.setter
    def peer(self, value: Optional[MicrobitPeer]) -> None:
        """Set the microbit peer.

        Args:
            value (Optional[MicrobitPeer]): The microbit peer.
        """
        self.__sync_is_pressed()
        self.__peer = value

    def press(self) -> None:
        """Press the button."""
        was_pressed = self.__is_pressed

        self.__is_pressed = True
        self.itemconfig(self.__round, fill=rgb(30, 30, 30))

        if not was_pressed:
            self.__sync_is_pressed()

    def release(self) -> None:
        """Release the button."""
        was_pressed = self.__is_pressed

        self.__is_pressed = False
        self.itemconfig(self.__round, fill="black")

        if was_pressed:
            self.__sync_is_pressed()

    def is_pressed(self) -> bool:
        """Returns whether the button is pressed.

        Returns:
            bool: Whether the button is pressed.
        """
        return self.__is_pressed

    def __sync_is_pressed(self) -> None:
        """Sync the button's is_pressed state."""
        if self.__peer is not None:
            try:
                self.__peer.send_command(
                    MicrobitButtonIsPressedCommand(
                        instance=self.__instance,
                        is_pressed=self.__is_pressed,
                    )
                )
            except CommunicationClosedError:
                self.__peer = None
