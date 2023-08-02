from typing import Union, Iterable
from ..image.Image import Image


class Display:
    def get_pixel(self, x: int, y: int):
        """Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright)."""
        pass

    def set_pixel(self, x: int, y: int, value: int):
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9."""
        pass

    def clear(self):
        """Set the brightness of all LEDs to 0 (off)."""
        pass

    def show(
        self,
        value: Union[Image, int, str, Iterable],
        delay: int = 400,
        *,
        wait: bool = True,
        loop: bool = False,
        clear: bool = False
    ):
        """shows the image. Use either:
            show(image)
            shows the image on the display.
            or
            show(value, <>delay, <>*, <>wait, <>loop, <>clear), where fields marked with <> are optional
            If value is a string, float or integer, display letters/digits in sequence. Otherwise, if value is an iterable sequence of images, display these images in sequence. Each letter, digit or image is shown with delay milliseconds between them.
        If wait is True, this function will block until the animation is finished, otherwise the animation will happen in the background.
        If loop is True, the animation will repeat forever.
        If clear is True, the display will be cleared after the iterable has finished.
        Note that the wait, loop and clear arguments must be specified using their keyword."""
        pass

    def scroll(
        self,
        value: Union[Image, int, str, Iterable],
        delay: int = 150,
        *,
        wait: bool = True,
        loop: bool = False,
        monospace: bool = False
    ):
        """Scrolls value horizontally on the display. If value is an integer or float it is first converted to a string using str(). The delay parameter controls how fast the text is scrolling.
        If wait is True, this function will block until the animation is finished, otherwise the animation will happen in the background.
        If loop is True, the animation will repeat forever.
        If monospace is True, the characters will all take up 5 pixel-columns in width, otherwise there will be exactly 1 blank pixel-column between each character as they scroll.
        Note that the wait, loop and monospace arguments must be specified using their keyword."""
        pass

    def on(self):
        """Turn on the display."""
        pass

    def off(self):
        """Turn off the display."""
        pass

    def is_on(self) -> bool:
        """Returns True if the display is on, otherwise returns False."""
        pass

    def read_light_level(self) -> int:
        """Use the display’s LEDs in reverse-bias mode to sense the amount of light falling on the display. Returns an integer between 0 and 255 representing the light level, with larger meaning more light."""
        pass
