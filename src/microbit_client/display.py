from threading import Thread
from time import sleep
from typing import Iterable, Union

from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.commands.microbit.display import (
    DISPLAY_MAX_X,
    DISPLAY_MAX_Y,
    DISPLAY_MIN_X,
    DISPLAY_MIN_Y,
    LED_MAX_VALUE,
    LED_MIN_VALUE,
    MicrobitDisplayClearCommand,
    MicrobitDisplayOffCommand,
    MicrobitDisplayOnCommand,
    MicrobitDisplayReadLightLevelCommand,
    MicrobitDisplaySetPixelCommand,
    MicrobitDisplayShowCommand,
)
from microbit_protocol.peer import MicrobitPeer

from microbit_client.image import Image


class Display:
    """Represents a micro:bit's display client."""

    def __init__(self, peer: MicrobitPeer) -> None:
        """Initialises `self` to a new Display instance.

        Args:
            peer (MicrobitPeer): The peer to communicate with.
        """
        self.__peer = peer
        self.__light_level = 0
        self.on()
        self.clear()

        def listener(command: MicrobitCommand) -> None:
            if isinstance(command, MicrobitDisplayReadLightLevelCommand):
                self.__light_level = command.light_level

        peer.add_listener(listener)

    def get_pixel(self, x: int, y: int) -> int:
        """Gets the brightness of the LED at the given position.

        Args:
            x (int): The x position of the LED.
            y (int): The y position of the LED.

        Returns:
            int: The brightness of the LED.
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"

        if (
            x < DISPLAY_MIN_X
            or DISPLAY_MAX_X < x
            or y < DISPLAY_MIN_Y
            or DISPLAY_MAX_Y < y
        ):
            raise ValueError(f"invalid position {x}, {y}")

        return self.__pixels[y][x]

    def set_pixel(self, x: int, y: int, value: int) -> None:
        """Sets the brightness of the LED at the given position.

        Args:
            x (int): The x position of the LED.
            y (int): The y position of the LED.
            value (int): The brightness of the LED.

        Raises:
            ValueError: If `value` is not between 0 and 9 inclusive.
            ValueError: If `x` or `y` are not between 0 and 4 inclusive.
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"
        assert isinstance(
            value, int
        ), f"value must be an int, not {type(value).__name__}"

        if value < LED_MIN_VALUE or LED_MAX_VALUE < value:
            raise ValueError("brightness out of bounds")

        if (
            x < DISPLAY_MIN_X
            or DISPLAY_MAX_X < x
            or y < DISPLAY_MIN_Y
            or DISPLAY_MAX_Y < y
        ):
            raise ValueError(f"invalid position {x}, {y}")

        self.__pixels[y][x] = value

        self.__peer.send_command(MicrobitDisplaySetPixelCommand(x=x, y=y, value=value))

    def clear(self) -> None:
        """Set the brightness of all LEDs to 0 (off)."""
        self.__pixels = [[0 for _ in range(5)] for _ in range(5)]
        self.__peer.send_command(MicrobitDisplayClearCommand())

    def show(  # noqa: PLR0913
        self,
        image: Union[Image, str, float, int, Iterable[Image]],
        delay: int = 400,
        *,
        wait: bool = True,
        loop: bool = False,
        clear: bool = False,
    ) -> None:
        """Displays an image on the micro:bit's display.

        Args:
            image (Union[Image, str, float, int, Iterable[Image]]): The image
                to display.
            delay (int, optional): The delay between each frame in milliseconds.
                Defaults to 400.
            wait (bool, optional): Whether to wait for the animation to finish.
                Defaults to True.
            loop (bool, optional): Whether to loop the animation.
                Defaults to False.
            clear (bool, optional): Whether to clear the display after the animation.
                Defaults to False.

        Raises:
            ValueError: If `delay` is negative.
        """
        if isinstance(image, Image):
            self.__send_image(image)
            return

        assert isinstance(image, (str, float, int, Iterable)), (
            "image must be a str, float, int or Iterable[Image],"
            f"got {type(image).__name__}"
        )
        assert isinstance(
            delay, int
        ), f"delay must be an int, not {type(delay).__name__}"
        assert isinstance(wait, bool), f"wait must be a bool, not {type(wait).__name__}"
        assert isinstance(loop, bool), f"loop must be a bool, not {type(loop).__name__}"
        assert isinstance(
            clear, bool
        ), f"clear must be a bool, not {type(clear).__name__}"

        if delay < 0:
            raise ValueError("delay must be positive")

        if isinstance(image, (int, float)):
            image = str(image)

        images: Iterable[Image]
        if isinstance(image, str):
            images = [Image(letter) for letter in image]
        else:
            images = image

        def target() -> None:
            self.__send_images(images, delay)
            while loop:
                self.__send_images(images, delay)

            if clear:
                self.clear()

        if wait:
            target()
        else:
            Thread(target=target, daemon=True).start()

    def scroll(  # noqa: PLR0913
        self,
        text: Union[str, int, float],
        delay: int = 150,
        *,
        wait: bool = True,
        loop: bool = False,
        monospace: bool = False,
    ) -> None:
        """Scrolls text across the micro:bit's display.

        Args:
            text (Union[str, int, float]): The text to scroll.
            delay (int, optional): The delay between each frame in milliseconds.
                Defaults to 150.
            wait (bool, optional): Whether to wait for the animation to finish.
                Defaults to True.
            loop (bool, optional): Whether to loop the animation.
                Defaults to False.
            monospace (bool, optional): Whether to use monospace font.
                Defaults to False.

        Raises:
            ValueError: If `delay` is negative.
        """
        assert isinstance(
            text, (str, int, float)
        ), f"text must be a str, int or float, not {type(text).__name__}"
        assert isinstance(
            delay, int
        ), f"delay must be an int, not {type(delay).__name__}"
        assert isinstance(wait, bool), f"wait must be a bool, not {type(wait).__name__}"
        assert isinstance(loop, bool), f"loop must be a bool, not {type(loop).__name__}"
        assert isinstance(
            monospace, bool
        ), f"monospace must be a bool, not {type(monospace).__name__}"

        if delay < 0:
            raise ValueError("delay must be positive")

        if isinstance(text, (int, float)):
            text = str(text)

        if monospace:
            image = self.__get_scroll_image_monospace(text)
        else:
            image = self.__get_scroll_image(text)

        def target() -> None:
            self.__scroll_image(image, delay)
            while loop:
                self.__scroll_image(image, delay)

        if wait:
            target()
        else:
            Thread(target=target, daemon=True).start()

    def on(self) -> None:
        """Turns the display on."""
        self.__is_on = True
        self.__peer.send_command(MicrobitDisplayOnCommand())

    def off(self) -> None:
        """Turns the display off."""
        self.__is_on = False
        self.__peer.send_command(MicrobitDisplayOffCommand())

    def is_on(self) -> bool:
        """Returns whether the display is on.

        Returns:
            bool: Whether the display is on.
        """
        return self.__is_on

    def read_light_level(self) -> int:
        """Reads the light level from the display.

        Returns:
            int: The light level.
        """
        return self.__light_level

    def __scroll_image(self, image: Image, delay: int) -> None:
        """Scrolls an image across the display.

        Args:
            image (Image): The image to scroll.
            delay (int): The delay between each frame in milliseconds.
        """
        for i in range(image.width() + 1):
            self.__send_image(image.crop(i, 0, 5, 5))
            sleep(delay / 1000)

    def __send_images(self, images: Iterable[Image], delay: int) -> None:
        """Sends images to the display.

        Args:
            images (Iterable[Image]): The images to send.
            delay (int): The delay between each frame in milliseconds.
        """
        for image in images:
            self.__send_image(image)
            sleep(delay / 1000)

    def __send_image(self, image: Image) -> None:
        """Sends an image to the display.

        Args:
            image (Image): The image to send.
        """
        self.__peer.send_command(
            MicrobitDisplayShowCommand(
                image=[
                    [image.get_pixel(x, y) for x in range(image.width())]
                    for y in range(image.height())
                ]
            )
        )

    @classmethod
    def __get_scroll_image_monospace(cls, text: str) -> Image:
        """Gets an image of the text in monospace to scroll.

        Args:
            text (str): The text to scroll.

        Returns:
            Image: The image of the text.
        """
        scroll_image = Image(4 + 5 * len(text), 5)

        for i, char in enumerate(text):
            scroll_image.blit(Image(char), 0, 0, 5, 5, 4 + 5 * i, 0)

        return scroll_image

    @classmethod
    def __get_scroll_image(cls, text: str) -> Image:
        """Gets an image of the text to scroll.

        Args:
            text (str): The text to scroll.

        Returns:
            Image: The image of the text.
        """
        images: list[Image] = []
        images_width = 0

        for char in text:
            if char == " ":
                image = Image(3, 5)
            else:
                image = cls.__remove_image_void(Image(char))

            images.append(image)
            images_width += image.width()

        scroll_image = Image(4 + images_width + len(images) - 1, 5)

        current_width = 4
        for image in images:
            scroll_image.blit(image, 0, 0, image.width(), 5, current_width, 0)
            current_width += image.width() + 1

        return scroll_image

    @classmethod
    def __remove_image_void(cls, image: Image) -> Image:
        """Removes the void pixels from an image.

        Args:
            image (Image): The image to remove the void pixels from.

        Returns:
            Image: The image without the void pixels.
        """
        start = 0
        while start < image.width() and cls.__is_column_void(image, start):
            start += 1

        end = image.width() - 1
        while start < end and cls.__is_column_void(image, end):
            end -= 1

        width = end - start + 1

        return image.crop(start, 0, width, image.height())

    @classmethod
    def __is_column_void(cls, image: Image, column: int) -> bool:
        """Returns whether a column is void.

        Args:
            image (Image): The image to check.
            column (int): The column to check.

        Returns:
            bool: Whether the column is void.
        """
        for y in range(image.height()):
            if image.get_pixel(column, y) != 0:
                return False
        return True
