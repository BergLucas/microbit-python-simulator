from microbit_protocol.commands.microbit.display import (
    MicrobitDisplaySetPixelCommand,
    MicrobitDisplayClearCommand,
    MicrobitDisplayShowCommand,
    MicrobitDisplayOnCommand,
    MicrobitDisplayOffCommand,
    MicrobitDisplayReadLightLevelCommand,
)
from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.peer import MicrobitPeer
from microbit._internal.image import Image
from typing import Union, Iterable, overload
from threading import Thread
from time import sleep

class Display:
    def __init__(self, peer: MicrobitPeer) -> None:
        self.__peer = peer
        self.__light_level = 0
        self.on()
        self.clear()

    def get_pixel(self, x: int, y: int) -> int:
        """Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright).

        Args:
            x (int): The x position of the pixel, from 0 (left) to 4 (right)
            y (int): The y position of the pixel, from 0 (top) to 4 (bottom)

        Raises:
            ValueError: if x or y is out of the screen

        Returns:
            int: The brightness of the pixel, from 0 (dark) to 9 (bright)
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"

        try:
            return self.__pixels[y][x]
        except IndexError:
            raise ValueError(f"invalid position {x}, {y}")

    def set_pixel(self, x: int, y: int, value: int) -> None:
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9.

        Args:
            x (int): The x position of the pixel, from 0 (left) to 4 (right)
            y (int): The y position of the pixel, from 0 (top) to 4 (bottom)
            value (int): The brightness of the pixel, from 0 (dark) to 9 (bright)

        Raises:
            ValueError: if the brightness is out of range
            ValueError: if x or y is out of the screen
        """
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"
        assert isinstance(
            value, int
        ), f"value must be an int, not {type(value).__name__}"

        if value < 0 or 9 < value:
            raise ValueError("brightness out of bounds")

        try:
            self.__pixels[y][x] = value
        except IndexError:
            raise ValueError("invalid position {x}, {y}")

        self.__peer.send_command(MicrobitDisplaySetPixelCommand(x=x, y=y, value=value))

    def clear(self) -> None:
        """Set the brightness of all LEDs to 0 (off)."""
        self.__pixels = [[0 for _ in range(5)] for _ in range(5)]
        self.__peer.send_command(MicrobitDisplayClearCommand())

    @overload
    def show(self, image: Image) -> None:
        """Display the `image`.

        Args:
            image (Image): The image to display
        """

    @overload
    def show(self, image: Union[str, float, int, Iterable[Image]], delay: int = 400, *, wait: bool = True, loop: bool = False, clear: bool = False) -> None:
        """If `image` is a string, float or integer, display letters/digits in sequence.
        Otherwise, if `image` is an iterable sequence of images, display these images in sequence.
        Each letter, digit or image is shown with `delay` milliseconds between them.

        If `wait` is `True`, this function will block until the animation is finished, otherwise the animation will happen in the background.

        If `loop` is `True`, the animation will repeat forever.

        If `clear` is `True`, the display will be cleared after the iterable has finished.

        Note that the `wait`, `loop` and `clear` arguments must be specified using their keyword.

        Args:
            image (Union[str, float, int, Iterable[Image]]): The image or images to display
            delay (int, optional): The delay between images in milliseconds. Defaults to 400.
            wait (bool, optional): Whether to wait until the animation is finished. Defaults to True.
            loop (bool, optional): Whether to loop the animation. Defaults to False.
            clear (bool, optional): Whether to clear the display after the animation. Defaults to False.

        Raises:
            ValueError: if `delay` is negative
        """

    def show(self, image: Union[Image, str, float, int, Iterable[Image]], delay: int = 400, *, wait: bool = True, loop: bool = False, clear: bool = False) -> None:
        """Display the `image`.
        
        Args:
            image (Union[Image, str, float, int, Iterable[Image]]): The image or images to display
            delay (int, optional): The delay between images in milliseconds. Defaults to 400.
            wait (bool, optional): Whether to wait until the animation is finished. Defaults to True.
            loop (bool, optional): Whether to loop the animation. Defaults to False.
            clear (bool, optional): Whether to clear the display after the animation. Defaults to False.

        Raises:
            ValueError: if `delay` is negative
        """
        if isinstance(image, Image):
            self.__send_image(image)
            return

        assert isinstance(image, (str, float, int, Iterable)), f"image must be a str, float, int or Iterable[Image], got {type(image).__name__}"
        assert isinstance(delay, int), f"delay must be an int, not {type(delay).__name__}"
        assert isinstance(wait, bool), f"wait must be a bool, not {type(wait).__name__}"
        assert isinstance(loop, bool), f"loop must be a bool, not {type(loop).__name__}"
        assert isinstance(clear, bool), f"clear must be a bool, not {type(clear).__name__}"

        if delay < 0:
            raise ValueError("delay must be positive")

        if isinstance(image, (int, float)):
            image = str(image)

        if isinstance(image, str):
            images = [Image(letter) for letter in image]
        else:
            images = image

        def target() -> None:
            self.__send_images(images, delay)
            while loop:
                self.__send_images(images, delay)

        if wait:
            target()
        else:
            Thread(target=target, daemon=True).start()

        if clear:
            self.clear()

    def scroll(self, text: Union[str, int, float], delay: int = 150, *, wait: bool = True, loop: bool = False, monospace: bool = False) -> None:
        """Scrolls `text` horizontally on the display. If `text` is an integer or float it is first converted to a string using `str()`.
        The `delay` parameter controls how fast the text is scrolling.

        If `wait` is `True`, this function will block until the animation is finished, otherwise the animation will happen in the background.

        If `loop` is `True`, the animation will repeat forever.

        If `monospace` is `True`, the characters will all take up 5 pixel-columns in width, otherwise there will be exactly 1 blank pixel-column between each character as they scroll.

        Note that the `wait`, `loop` and `monospace` arguments must be specified using their keyword.

        Args:
            text (Union[str, int, float]): The text to scroll
            delay (int, optional): The delay between images in milliseconds. Defaults to 150.
            wait (bool, optional): Whether to wait until the animation is finished. Defaults to True.
            loop (bool, optional): Whether to loop the animation. Defaults to False.
            monospace (bool, optional): Whether to use monospace font. Defaults to False.

        Raises:
            ValueError: if `delay` is negative
        """
        assert isinstance(text, (str, int, float)), f"text must be a str, int or float, not {type(text).__name__}"
        assert isinstance(delay, int), f"delay must be an int, not {type(delay).__name__}"
        assert isinstance(wait, bool), f"wait must be a bool, not {type(wait).__name__}"
        assert isinstance(loop, bool), f"loop must be a bool, not {type(loop).__name__}"
        assert isinstance(monospace, bool), f"monospace must be a bool, not {type(monospace).__name__}"

        if delay < 0:
            raise ValueError("delay must be positive")

        if isinstance(text, (int, float)):
            text = str(text)

        image = Image(4 + 5*len(text), 5)

        for i, char in enumerate(text):
            image.blit(Image(char), 0, 0, 5, 5, 4 + 5*i, 0)

        def target() -> None:
            self.__scroll_image(image, delay)
            while loop:
                self.__scroll_image(image, delay)

        if wait:
            target()
        else:
            Thread(target=target, daemon=True).start()

    def on(self) -> None:
        """Use on() to turn on the display."""
        self.__is_on = True
        self.__peer.send_command(MicrobitDisplayOnCommand())

    def off(self) -> None:
        """Use off() to turn off the display (thus allowing you to re-use the GPIO pins associated with the display for other purposes)."""
        self.__is_on = False
        self.__peer.send_command(MicrobitDisplayOffCommand())

    def is_on(self) -> bool:
        """Returns `True` if the display is `on`, otherwise returns `False`.
        
        Returns:
            bool: Whether the display is on
        """
        return self.__is_on

    def read_light_level(self) -> int:
        """Use the display's LEDs in reverse-bias mode to sense the amount of light falling on the display.
        Returns an integer between 0 and 255 representing the light level, with larger meaning more light.

        Returns:
            int: The light level, between 0 and 255
        """
        return self.__light_level

    def execute(self, command: MicrobitCommand) -> None:
        """Execute a command.

        Args:
            command (MicrobitCommand): The command to execute
        
        Raises:
            ValueError: if the command is not recognised
        """
        if isinstance(command, MicrobitDisplayReadLightLevelCommand):
            self.__light_level = command.light_level
        else:
            raise ValueError(f"Unknown command: {command}")

    def __scroll_image(self, image: Image, delay: int) -> None:
        """Scroll the image horizontally.

        Args:
            image (Image): The image to scroll
            delay (int): The delay between images in milliseconds
        """
        for i in range(image.width() + 1):
            self.__send_image(image.crop(i, 0, 5, 5))
            sleep(delay/1000)

    def __send_images(self, images: Iterable[Image], delay: int) -> None:
        """Send the images with a delay between them.

        Args:
            images (Iterable[Image]): The images to send
            delay (int): The delay between images in milliseconds
        """
        for image in images:
            self.__send_image(image)
            sleep(delay/1000)

    def __send_image(self, image: Image) -> None:
        """Send the image.

        Args:
            image (Image): The image to send
        """
        self.__peer.send_command(
            MicrobitDisplayShowCommand(
                image=[
                    [image.get_pixel(x, y) for x in range(image.width())]
                    for y in range(image.height())
                ]
            )
        )
