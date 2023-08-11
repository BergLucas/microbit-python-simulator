from tkinter import Canvas, Frame, Misc
from typing import Optional

from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.commands.microbit.display import (
    DISPLAY_MAX_X,
    DISPLAY_MAX_Y,
    DISPLAY_MIN_X,
    DISPLAY_MIN_Y,
    LED_MAX_VALUE,
    LED_MIN_VALUE,
    MAX_LIGHT_LEVEL,
    MIN_LIGHT_LEVEL,
    MicrobitDisplayOffCommand,
    MicrobitDisplayOnCommand,
    MicrobitDisplayReadLightLevelCommand,
    MicrobitDisplaySetPixelCommand,
    MicrobitDisplayShowCommand,
)
from microbit_protocol.exceptions import CommunicationClosedError
from microbit_protocol.peer import MicrobitPeer

from microbit_simulator.utils import rgb


class MicrobitLed(Frame):
    """This type represents a led on the microbit."""

    def __init__(self, master: Misc, width: int, height: int) -> None:
        """Initialises self to a Led.

        Args:
            master (Misc): The parent widget.
            width (int): The width of the led. Must be positive.
            height (int): The height of the led. Must be positive.
        """
        assert width > 0
        assert height > 0

        super().__init__(master, width=width, height=height, bg="")

        self.__brightness = 0
        self.__is_on = True

        holder = Canvas(self, bg=rgb(100, 100, 100), highlightthickness=0)
        holder.place(relx=0.1, rely=0, relwidth=0.8, relheight=1)

        self.__light = Canvas(self, bg=rgb(198, 198, 198), highlightthickness=0)
        self.__light.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

    def __config_light(self, brightness: int) -> None:
        """Configures the light of the led.

        Args:
            brightness (int): The brightness of the led. Must be between 0 and 9.
        """
        assert LED_MIN_VALUE <= brightness and brightness <= LED_MAX_VALUE

        self.__light.config(
            bg=rgb(
                r=198 + brightness * 6,
                g=(9 - brightness) * 22,
                b=(9 - brightness) * 22,
            )
        )

    @property
    def is_on(self) -> bool:
        """Returns whether the led is on.

        Returns:
            bool: Whether the led is on.
        """
        return self.__is_on

    def on(self) -> None:
        """Turns the led on."""
        self.__is_on = True
        self.__config_light(self.__brightness)

    def off(self) -> None:
        """Turns the led off."""
        self.__is_on = False
        self.__config_light(0)

    @property
    def brightness(self) -> int:
        """Returns the brightness of the led.

        Returns:
            int: The brightness of the led.
        """
        return self.__brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        """Sets the brightness of the led.

        Args:
            value (int): The brightness of the led. Must be between 0 and 9.
        """
        assert LED_MIN_VALUE <= value and value <= LED_MAX_VALUE

        self.__brightness = value
        self.__config_light(value)


class MicrobitDisplay(Frame):
    """A display widget that represents the display of a microbit."""

    def __init__(self, master: Misc, size: int):
        """Initialises self to a DisplayWidget.

        Args:
            master (Misc): The parent widget.
            size (int): The size of the display. Must be positive.
        """
        assert size > 0

        Frame.__init__(self, master, width=size, height=size, bg=rgb(25, 25, 25))

        led_rwidth = 0.07
        led_rheight = 0.15
        space_rwidth = (1 - led_rwidth * 5) / 4
        space_rheight = (1 - led_rheight * 5) / 4

        self.__leds: list[list[MicrobitLed]] = [
            [
                self.__place_led(
                    led_rwidth=led_rwidth,
                    led_rheight=led_rheight,
                    relx=(space_rwidth + led_rwidth) * lx,
                    rely=(space_rheight + led_rheight) * ly,
                    size=size,
                )
                for ly in range(5)
            ]
            for lx in range(5)
        ]

        self.__is_on = True
        self.__light_level = 0
        self.__peer: Optional[MicrobitPeer] = None

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
        self.__sync_light_level()

    def get_pixel(self, x: int, y: int) -> int:
        """Return the brightness of the LED at column x and row y.

        Args:
            x (int): The x position of the led. Must be between 0 and 4.
            y (int): The y position of the led. Must be between 0 and 4.

        Returns:
            int: The brightness of the led.
        """
        return self.__leds[x][y].brightness

    def is_on(self) -> bool:
        """Return whether the display is on.

        Returns:
            bool: Whether the display is on.
        """
        return self.__is_on

    def set_light_level(self, value: int) -> None:
        """Set the light level of the display.

        Args:
            value (int): The light level of the display. Must be between 0 and 255.
        """
        assert MIN_LIGHT_LEVEL <= value and value <= MAX_LIGHT_LEVEL

        self.__light_level = value
        self.__sync_light_level()

    def read_light_level(self) -> int:
        """Return the current light level of the display.

        Returns:
            int: The current light level of the display.
        """
        return self.__light_level

    def __place_led(  # noqa: PLR0913
        self,
        led_rwidth: float,
        led_rheight: float,
        relx: float,
        rely: float,
        size: float,
    ) -> MicrobitLed:
        """Place a led on the display.

        Args:
            led_rwidth (float): The relative width of the led. Must be positive.
            led_rheight (float): The relative height of the led. Must be positive.
            relx (float): The x position of the led. Must be positive.
            rely (float): The y position of the led. Must be positive.
            size (float): The size of the display. Must be positive.

        Returns:
            MicrobitLed: The led.
        """
        assert led_rwidth > 0
        assert led_rheight > 0
        assert relx >= 0
        assert rely >= 0
        assert size > 0

        led = MicrobitLed(self, int(led_rwidth * size), int(led_rheight * size))

        led.place(
            relx=relx,
            rely=rely,
            relwidth=led_rwidth,
            relheight=led_rheight,
        )

        return led

    def __execute(self, command: MicrobitCommand) -> None:
        """Execute the command.

        Args:
            command (MicrobitCommand): The command to execute.
        """
        if isinstance(command, MicrobitDisplayOnCommand):
            self.__on()
        if isinstance(command, MicrobitDisplayOffCommand):
            self.__off()
        if isinstance(command, MicrobitDisplaySetPixelCommand):
            self.__set_pixel(command.x, command.y, command.value)
        if isinstance(command, MicrobitDisplayShowCommand):
            self.__show(command.image)

    def __set_pixel(self, x: int, y: int, value: int) -> None:
        """Set the brightness of the LED at column x and row y to value.

        The brightness has to be between 0 (off) and 9 (bright).

        Args:
            x (int): The x position of the led. Must be between 0 and 4.
            y (int): The y position of the led. Must be between 0 and 4.
            value (int): The brightness of the led. Must be between 0 and 9.
        """
        assert DISPLAY_MIN_X <= x and x <= DISPLAY_MAX_X
        assert DISPLAY_MIN_Y <= y and y <= DISPLAY_MAX_Y
        assert LED_MIN_VALUE <= value and value <= LED_MAX_VALUE

        self.__leds[x][y].brightness = value

    def __show(self, image: list[list[int]]) -> None:
        """Display the image.

        Args:
            image (list[list[int]]): The image to display.
                Must be a maximum 5x5 matrix of integers between 0 and 9.
        """
        for y, row in enumerate(image):
            for x, value in enumerate(row):
                self.__set_pixel(x, y, value)

    def __on(self) -> None:
        """Turn on the display."""
        self.__is_on = True
        for row in self.__leds:
            for led in row:
                led.on()

    def __off(self) -> None:
        """Turn off the display."""
        self.__is_on = False
        for row in self.__leds:
            for led in row:
                led.off()

    def __sync_light_level(self) -> None:
        """Sync the display's light_level value."""
        if self.__peer is not None:
            try:
                self.__peer.send_command(
                    MicrobitDisplayReadLightLevelCommand(light_level=self.__light_level)
                )
            except CommunicationClosedError:
                self.__peer = None
