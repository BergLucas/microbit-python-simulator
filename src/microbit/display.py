from typing import Iterable, Union, overload

from microbit_client.image import Image

from microbit._internal import display as __display


def get_pixel(x: int, y: int) -> int:
    """Return the brightness of the LED at column x and row y as an integer.

    The brightness must be between 0 (off) and 9 (bright).

    Args:
        x (int): The x position of the pixel, from 0 (left) to 4 (right)
        y (int): The y position of the pixel, from 0 (top) to 4 (bottom)

    Raises:
        ValueError: if x or y is out of the screen

    Returns:
        int: The brightness of the pixel, from 0 (dark) to 9 (bright)
    """
    return __display.get_pixel(x, y)


def set_pixel(x: int, y: int, value: int) -> None:
    """Set the brightness of the LED at column x and row y to value.

    The brightness has to be an integer between 0 and 9.

    Args:
        x (int): The x position of the pixel, from 0 (left) to 4 (right)
        y (int): The y position of the pixel, from 0 (top) to 4 (bottom)
        value (int): The brightness of the pixel, from 0 (dark) to 9 (bright)

    Raises:
        ValueError: if the brightness is out of range
        ValueError: if x or y is out of the screen
    """
    __display.set_pixel(x, y, value)


def clear() -> None:
    """Set the brightness of all LEDs to 0 (off)."""
    __display.clear()


@overload
def show(image: Image) -> None:
    """Display the `image`.

    Args:
        image (Image): The image to display
    """


@overload
def show(
    image: Union[str, float, int, Iterable[Image]],
    delay: int = 400,
    *,
    wait: bool = True,
    loop: bool = False,
    clear: bool = False
) -> None:
    """If `image` is a string, float or integer, display letters/digits in sequence.

    Otherwise, if `image` is an iterable sequence of images, display these images
    in sequence. Each letter, digit or image is shown with `delay` milliseconds
    between them.

    If `wait` is `True`, this function will block until the animation is finished,
    otherwise the animation will happen in the background.

    If `loop` is `True`, the animation will repeat forever.

    If `clear` is `True`, the display will be cleared after the iterable has finished.

    Note that the `wait`, `loop` and `clear` arguments must be specified
    using their keyword.

    Args:
        image (Union[str, float, int, Iterable[Image]]): The image or images to display.
        delay (int, optional): The delay between images in milliseconds.
            Defaults to 400.
        wait (bool, optional): Whether to wait until the animation is finished.
            Defaults to True.
        loop (bool, optional): Whether to loop the animation. Defaults to False.
        clear (bool, optional): Whether to clear the display after the animation.
            Defaults to False.

    Raises:
        ValueError: if `delay` is negative
    """


def show(
    image: Union[Image, str, float, int, Iterable[Image]],
    delay: int = 400,
    *,
    wait: bool = True,
    loop: bool = False,
    clear: bool = False
) -> None:
    """Display the `image`.

    Args:
        image (Union[Image, str, float, int, Iterable[Image]]): The image or images
            to display
        delay (int, optional): The delay between images in milliseconds.
            Defaults to 400.
        wait (bool, optional): Whether to wait until the animation is finished.
            Defaults to True.
        loop (bool, optional): Whether to loop the animation. Defaults to False.
        clear (bool, optional): Whether to clear the display after the animation.
            Defaults to False.

    Raises:
        ValueError: if `delay` is negative
    """
    __display.show(image, delay, wait=wait, loop=loop, clear=clear)


def scroll(
    text: Union[str, int, float],
    delay: int = 150,
    *,
    wait: bool = True,
    loop: bool = False,
    monospace: bool = False
) -> None:
    """Scrolls `text` horizontally on the display.

    If `text` is an integer or float it is first converted to a string using `str()`.

    The `delay` parameter controls how fast the text is scrolling.

    If `wait` is `True`, this function will block until the animation is finished,
    otherwise the animation will happen in the background.

    If `loop` is `True`, the animation will repeat forever.

    If `monospace` is `True`, the characters will all take up 5 pixel-columns in width,
    otherwise there will be exactly 1 blank pixel-column between each character
    as they scroll.

    Note that the `wait`, `loop` and `monospace` arguments must be specified
    using their keyword.

    Args:
        text (Union[str, int, float]): The text to scroll
        delay (int, optional): The delay between images in milliseconds.
            Defaults to 150.
        wait (bool, optional): Whether to wait until the animation is finished.
            Defaults to True.
        loop (bool, optional): Whether to loop the animation. Defaults to False.
        monospace (bool, optional): Whether to use monospace font. Defaults to False.

    Raises:
        ValueError: if `delay` is negative
    """
    __display.scroll(text, delay, wait=wait, loop=loop, monospace=monospace)


def on() -> None:
    """Turns on the display."""
    __display.on()


def off() -> None:
    """Turns off the display.

    It allows you to re-use the GPIO pins associated with the display
    for other purposes.
    """
    __display.off()


def is_on() -> bool:
    """Returns `True` if the display is `on`, otherwise returns `False`.

    Returns:
        bool: Whether the display is on
    """
    return __display.is_on()


def read_light_level() -> int:
    """Use the display's LEDs in reverse-bias mode to sense the amount of light.

    Returns an integer between 0 and 255 representing the light level,
    with larger meaning more light.

    Returns:
        int: The light level, between 0 and 255
    """
    return __display.read_light_level()
