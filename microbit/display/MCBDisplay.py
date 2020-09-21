from collections.abc import Iterable
from threading import Thread
from time import sleep
from .Display import Display
from ..image.Image import Image
class MCBDisplay(Display):
    def __init__(self):
        # Display properties
        self.__on = True
        self.__light_level = 0
        self.__pixels = {}
        self.__run = True
        # Reset pixels
        self.clear()

    def _inDisplay(self, x, y):
        return type(x) == int and type(y) == int and 0 <= x and x < 5 and 0 <= y and y < 5

    def get_pixel(self, x, y):
        """Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright)."""
        if not self._inDisplay(x, y):
            return 0
        else:
            return int(self.__pixels[(x, y)])

    def set_pixel(self, x, y, value):
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9."""
        if type(value) != int:
            raise TypeError('%f brightness is not an integer' % value)
        if value < 0 or 9 < value:
            raise IndexError('%d brightness is not between 0 and 9' % value)
        if self._inDisplay(x, y):
            self.__pixels[(x, y)] = value

    def clear(self):
        """Set the brightness of all LEDs to 0 (off)."""
        for x in range(5):
            for y in range(5):
                self.set_pixel(x, y, 0)

    def show(self, value, delay=400, *, wait=True, loop=False, clear=False):
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
        # Check if value is an image
        if isinstance(value, Image):
            for x in range(5):
                for y in range(5):
                    self.set_pixel(x, y, value.get_pixel(x, y))
        else:
            # Check if value is string or float or integer:
            if isinstance(value, (str, int, float)):
                string = str(value)
                value = []
                for char in string:
                    value.append(Image(char))
            elif not isinstance(value, Iterable):
                raise TypeError('value must be an Iterable')

            # Check if wait and loop
            animation = self.async_show_animation(value, delay, loop)
            if wait:
                while self.__run and animation.isAlive():
                    animation.join(delay/1000)
            # Check if clear
            if clear:
                self.clear()

    def scroll(self, value, delay=150, *, wait=True, loop=False, monospace=False):
        """Scrolls value horizontally on the display. If value is an integer or float it is first converted to a string using str(). The delay parameter controls how fast the text is scrolling.
        If wait is True, this function will block until the animation is finished, otherwise the animation will happen in the background.
        If loop is True, the animation will repeat forever.
        If monospace is True, the characters will all take up 5 pixel-columns in width, otherwise there will be exactly 1 blank pixel-column between each character as they scroll.
        Note that the wait, loop and monospace arguments must be specified using their keyword."""
        # Check if value is string or float or integer:
        if isinstance(value, (str, int, float)):
            string = str(value)
            value = []
            for char in string:
                value.append(Image(char))
        elif not isinstance(value, Iterable):
            raise TypeError('value must be an Iterable')
        # Check if wait and loop
        animation = self.async_scroll_animation(value, delay, loop, monospace)
        if wait:
            while self.__run and animation.isAlive():
                animation.join(delay/1000)

    def on(self):
        """Turn on the display."""
        self.__on = True
    
    def off(self):
        """Turn off the display."""
        self.__on = False

    def is_on(self):
        """Returns True if the display is on, otherwise returns False."""
        return self.__on

    def read_light_level(self):
        """Use the display’s LEDs in reverse-bias mode to sense the amount of light falling on the display. Returns an integer between 0 and 255 representing the light level, with larger meaning more light."""
        return self.__light_level

    def set_light_level(self, value):
        if value < 0 or 255 < value:
            raise IndexError('%d light level is not between 0 and 255' % value)
        self.__light_level = value
    
    def shutdown(self):
        self.__run = False

    def async_show_animation(self, image_list, delay, loop):
        animation = Thread(target=self.show_animation, args=(image_list, delay, loop), daemon=True)
        animation.start()
        return animation

    def async_scroll_animation(self, image_list, delay, loop, monospace):
        animation = Thread(target=self.scroll_animation, args=(image_list, delay, loop, monospace), daemon=True)
        animation.start()
        return animation

    def show_animation(self, image_list, delay, loop):
        one_time = True
        while (loop or one_time) and self.__run:
            for image in image_list:
                if not self.__run:
                    break
                self.show(image)
                sleep(delay/1000)
            one_time = False
    
    def scroll_animation(self, image_list, delay, loop, monospace):
        # Create one big image
        width = 5
        new_image = Image()
        # Add an offset if monospace
        offset = 1 if monospace else 0
        # Iterate over the image list
        for image in image_list:
            # Remove void if monospace
            if monospace:
                image = self.__remove_void(image)
            img_width = image.width()
            old_image = new_image
            # Create a new image of updated size
            new_image = Image(width=width+img_width+offset, height=5)
            # Copy the old image in the new image
            new_image.blit(old_image, 0, 0, width, 5, 0, 0)
            # Copy the image from the list
            new_image.blit(image, 0, 0, img_width, 5, width-1+offset, 0)
            width += img_width+offset
        # Start the loop
        one_time = True
        while (loop or one_time) and self.__run:
            image = new_image
            width = image.width()
            while (width > 0) and self.__run:
                self.show(image)
                image = image.shift_left(1)
                sleep(delay/1000)
                width -= 1
            one_time = False

    def __remove_void(self, image):
        min_x = None
        max_x = None
        for x in range(image.width()):
            for y in range(image.height()):
                value = image.get_pixel(x, y)
                if value != 0:
                    if min_x == None:
                        min_x = x
                        max_x = x
                    max_x = max(x, max_x)
                    min_x = min(x, min_x)
        # Check if the image is empty
        if min_x == None:
            return Image('')
        else:
            return image.crop(min_x, 0, max_x+1-min_x, image.height())