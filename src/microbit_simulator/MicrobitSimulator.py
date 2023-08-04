from microbit_protocol.commands.microbit import (
    MicrobitResetCommand,
    MicrobitTemperatureCommand,
)
from microbit_protocol.peer import MicrobitPeer, MicrobitWebsocketPeer
from microbit_protocol.commands import MicrobitCommand
from microbit_simulator.accelerometer import AccelerometerWidget
from microbit_simulator.display import MicrobitDisplay
from microbit_simulator.button import MicrobitButton, BUTTON_A, BUTTON_B
from microbit_simulator.utils import rgb
from tkinter import Tk, Misc, Canvas
from typing import Optional, Literal
from threading import Thread


class MicrobitSimulator(Tk):
    def __init__(self, width: int = 900, height: int = 500) -> None:
        """Initialises self to a MicrobitSimulator.

        Args:
            width (int, optional): The width of the window. Defaults to 900.
            height (int, optional): The height of the window. Defaults to 500.
        """
        Tk.__init__(self)

        self.geometry(f"{width}x{height}")
        self.title("Microbit Simulator")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.resizable(False, False)

        self.__temperature = 0
        self.__peer: Optional[MicrobitPeer] = None

        self.__background = self.__place_background(self, height, width)
        self.__display = self.__place_display(self.__background, 0, height, 700)
        self.__button_a = self.__place_button(
            self.__background, 0.15, 0.05, height, 700, "button_a", BUTTON_A
        )
        self.__button_b = self.__place_button(
            self.__background, 0.15, 0.80, height, 700, "button_b", BUTTON_B
        )
        self.__accelerometer = self.__place_accelerometer(
            self.__background, 700, height, 200
        )

    def open(self) -> None:
        def target():
            peer = MicrobitWebsocketPeer.wait_for_connection("localhost", 8765)
            self.peer = peer
            self.__display.peer = peer
            self.__button_a.peer = peer
            self.__button_b.peer = peer
            peer.listen()

        Thread(target=target, daemon=True).start()

    def quit(self) -> None:
        """Quit the MicrobitSimulator window"""
        self.__display.peer = None
        super().quit()

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
        if self.__peer is not None:
            self.__peer.remove_listener(self.__execute)

        if value is not None:
            value.add_listener(self.__execute)

        self.__peer = value
        self.__sync_temperature()

    @property
    def display(self) -> MicrobitDisplay:
        """Returns the display of the MicrobitSimulator.

        Returns:
            MicrobitDisplay: The display of the MicrobitSimulator.
        """
        return self.__display

    @property
    def button_a(self) -> MicrobitButton:
        """Returns the A button of the MicrobitSimulator.

        Returns:
            ButtonWidget: The A button of the MicrobitSimulator.
        """
        return self.__button_a

    @property
    def button_b(self) -> MicrobitButton:
        """Returns the B button of the MicrobitSimulator.

        Returns:
            ButtonWidget: The B button of the MicrobitSimulator.
        """
        return self.__button_b

    @property
    def temperature(self) -> int:
        """Returns the temperature of the MicrobitSimulator.

        Returns:
            int: The temperature of the MicrobitSimulator.
        """
        return self.__temperature

    @temperature.setter
    def temperature(self, value: int) -> None:
        """Sets the temperature of the MicrobitSimulator.

        Args:
            value (int): The new temperature of the MicrobitSimulator.
        """
        self.__temperature = value
        self.__sync_temperature()

    @staticmethod
    def __place_background(master: Misc, height: int, width: int) -> Canvas:
        """Places the background in the center of the window.

        Args:
            master (Misc): The parent widget.
            height (int): The height of the window.
            width (int): The width of the window.

        Returns:
            Canvas: The background of the MicrobitSimulator.
        """
        background = Canvas(master, bg=rgb(25, 25, 25), highlightthickness=0)
        background.place(x=0, y=0, width=width, height=height)

        master.update_idletasks()

        return background

    @staticmethod
    def __place_display(
        master: Misc, relx: float, height: int, width: int
    ) -> MicrobitDisplay:
        """Places the display in the center of the window.

        Args:
            master (Misc): The parent widget.
            relx (float): The relative x position of the display.
            height (int): The height of the window.
            width (int): The width of the window.

        Returns:
            MicrobitDisplay: The display of the MicrobitSimulator.
        """
        x_space = 0.4
        size = width * x_space
        y_space = size / height
        width_ratio = width / master.winfo_width()

        display = MicrobitDisplay(master, int(size))
        display.place(
            relx=relx + width_ratio * (1 - x_space) / 2,
            rely=(1 - y_space) / 2,
        )

        master.update_idletasks()

        return display

    @staticmethod
    def __place_button(
        master: Misc,
        rwidth: float,
        relx: float,
        height: int,
        width: int,
        instance: Literal["button_a", "button_b"],
        button_key: str,
    ) -> MicrobitButton:
        """Places the button at the given relx position in the window.

        Args:
            master (Misc): The parent widget.
            rwidth (float): The relative width of the button.
            relx (float): The relative x position of the button.
            height (int): The height of the window.
            width (int): The width of the window.
            instance (Literal["button_a", "button_b"]): The instance of the button.
            button_key (str): The key of the button.

        Returns:
            ButtonWidget: The button of the MicrobitSimulator.
        """
        buttons_size = width * 0.15
        rely = (1 - buttons_size / height) / 2
        width_ratio = width / master.winfo_width()

        button = MicrobitButton(master, int(rwidth * width), instance, button_key)
        button.place(relx=relx * width_ratio, rely=rely)

        master.update_idletasks()

        return button

    @staticmethod
    def __place_accelerometer(
        master: Misc, x: int, height: int, width: int
    ) -> AccelerometerWidget:
        """Places the accelerometer in the center of the window.

        Args:
            master (Misc): The parent widget.
            x (int): The x position of the accelerometer.
            height (int): The height of the window.
            width (int): The width of the window.

        Returns:
            AccelerometerWidget: The accelerometer of the MicrobitSimulator.
        """
        accelerometer = AccelerometerWidget(master, width, height)
        accelerometer.place(x=x, y=0)

        master.update_idletasks()

        return accelerometer

    def __execute(self, command: MicrobitCommand) -> None:
        """Execute the given command.

        Args:
            command (MicrobitCommand): The command to execute.
        """
        if isinstance(command, MicrobitResetCommand):
            self.__reset()

    def __reset(self) -> None:
        """Reset the MicrobitSimulator."""
        if self.__peer is not None:
            self.__peer.stop()
            self.__peer.close()

            self.peer = None
            self.__display.peer = None
            self.__button_a.peer = None
            self.__button_b.peer = None

    def __sync_temperature(self) -> None:
        """Sync the microbit's temperature value."""
        if self.__peer is not None:
            self.__peer.send_command(
                MicrobitTemperatureCommand(temperature=self.__temperature)
            )
