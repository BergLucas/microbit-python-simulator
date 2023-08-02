from threading import Thread
from time import sleep
from typing import Type, Union, Iterable
from .Display import Display
from microbit._internal.microbit.image import Image


class MCBDisplay(Display):
    def __init__(self):
        """Create a MicrobitDisplay object"""
        # Display properties
        self.__on = True
        self.__light_level = 0
        self.__pixels = {}
        self.__run = True
        # Reset pixels
        self.clear()

    def _inDisplay(self, x: int, y: int) -> bool:
        """Check if the position is in the display

        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)

        Returns:
        --------
        inside : True if the position is inside the display, False otherwise

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(x, int):
            raise TypeError(f"invalid type : {type(x)} is not a int")
        if not isinstance(y, int):
            raise TypeError(f"invalid type : {type(y)} is not a int")
        return 0 <= x and x < 5 and 0 <= y and y < 5

    def get_pixel(self, x: int, y: int):
        """Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright).

        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        Notes:
        ------
        Returns 0 if x or y is outside the display
        """
        if not self._inDisplay(x, y):
            return 0
        else:
            return int(self.__pixels[(x, y)])

    def set_pixel(self, x: int, y: int, value: int):
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9.

        Parameters:
        -----------
        x : The x position (int)

        y : The y position (int)

        value : The brightness (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the brightness is not between 0 and 9
        """
        if not isinstance(value, int):
            raise TypeError("%f brightness is not an integer" % value)
        if value < 0 or 9 < value:
            raise ValueError("%d brightness is not between 0 and 9" % value)
        if self._inDisplay(x, y):
            self.__pixels[(x, y)] = value

    def clear(self):
        """Set the brightness of all LEDs to 0 (off)."""
        for x in range(5):
            for y in range(5):
                self.set_pixel(x, y, 0)

    def show(
        self,
        value: Union[Image, str, int, Iterable],
        delay: int = 400,
        *,
        wait: bool = True,
        loop: bool = False,
        clear: bool = False,
    ):
        """Show a sequence of image on the display.

        Parameters:
        -----------
        value : The value which will be displayed (Union[Image, str, int, Iterable])

        delay : How fast the text is scrolling in ms (int)

        wait : Block until the animation is finished if True, otherwise the animation will happen in the background (bool)

        loop : The animation will repeat forever if True (bool)

        clear : The display will be cleared after the iterable has finished if True (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the delay is negative

        Notes:
        ------
        The wait, loop and monospace arguments must be specified using their keyword
        """
        # Check if value is an image
        if isinstance(value, Image):
            self.__show_image(value)
            return
        # Check if value is string or float or integer:
        elif isinstance(value, (str, int, float)):
            string = str(value)
            value = []
            for char in string:
                value.append(Image(char))
        # Check if Iterable
        elif not isinstance(value, Iterable):
            raise TypeError("value must be an Iterable")
        # Check if wait and loop
        animation = self.async_show_animation(value, delay, loop)
        if wait:
            while self.__run and animation.isAlive():
                animation.join(delay / 1000)
        # Check if clear
        if clear:
            self.clear()

    def scroll(
        self,
        value: Union[Image, str, int, Iterable],
        delay: int = 150,
        *,
        wait: bool = True,
        loop: bool = False,
        monospace: bool = False,
    ):
        """Scrolls value horizontally on the display.

        Parameters:
        -----------
        value : The value which will be displayed (Union[Image, str, int, Iterable])

        delay : How fast the text is scrolling in ms (int)

        wait : Block until the animation is finished if True, otherwise the animation will happen in the background (bool)

        loop : The animation will repeat forever if True (bool)

        monospace : The characters will all take up 5 pixel-columns in width if True, otherwise there will be exactly 1 blank pixel-column between each character as they scroll (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the delay is negative

        Notes:
        ------
        The wait, loop and monospace arguments must be specified using their keyword
        """
        # Check if value is an image
        if isinstance(value, Image):
            value = [value]
        # Check if value is string or float or integer:
        elif isinstance(value, (str, int, float)):
            string = str(value)
            value = []
            for char in string:
                value.append(Image(char))
        elif not isinstance(value, Iterable):
            raise TypeError("value must be an Iterable")
        # Check if wait and loop
        animation = self.async_scroll_animation(value, delay, loop, monospace)
        if wait:
            while self.__run and animation.isAlive():
                animation.join(delay / 1000)

    def on(self):
        """Turn on the display."""
        self.__on = True

    def off(self):
        """Turn off the display."""
        self.__on = False

    def is_on(self) -> bool:
        """Check if the display is on

        Returns:
        --------
        on : True if the display is on, otherwise returns False."""
        return self.__on

    def read_light_level(self) -> int:
        """Returns the light level between 0 and 255

        Returns:
        --------
        light_level : The light level (int)
        """
        return self.__light_level

    def set_light_level(self, value: int):
        """Set the light level to a value

        Parameters:
        -----------
        value : The brightness (int)

        Raises:
        -------
        TypeError if the type of a parameter is invalid
        """
        if not isinstance(value, int):
            raise TypeError(f"invalid type : {type(value)} is not a int")
        if value < 0 or 255 < value:
            raise IndexError("%d light level is not between 0 and 255" % value)
        self.__light_level = value

    def shutdown(self):
        """Shutdown the display"""
        self.__run = False

    def async_show_animation(self, image_list: Iterable, delay: int, loop: bool):
        """Show an animation in background

        Parameters:
        -----------
        image_list : The iterable of image (Iterable[Image])

        delay : The delay after the image is shown (int)

        loop : Loop the animation if True, does not loop otherwise (bool)

        Returns:
        --------
        animation : The thread which does the animation (Thread)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the delay is negative
        """
        animation = Thread(
            target=self.show_animation, args=(image_list, delay, loop), daemon=True
        )
        animation.start()
        return animation

    def async_scroll_animation(
        self, image_list: Iterable, delay: int, loop: bool, monospace: bool
    ):
        """Scroll an animation in background

        Parameters:
        -----------
        image_list : The iterable of image (Iterable[Image])

        delay : The delay after the image is shown (int)

        loop : Loop the animation if True, does not loop otherwise (bool)

        monospace : Normalized space if True, not normalized otherwise (bool)

        Returns:
        --------
        animation : The thread which does the animation (Thread)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the delay is negative
        """
        animation = Thread(
            target=self.scroll_animation,
            args=(image_list, delay, loop, monospace),
            daemon=True,
        )
        animation.start()
        return animation

    def show_animation(self, image_list: Iterable, delay: int, loop: bool):
        """Show an animation

        Parameters:
        -----------
        image_list : The iterable of image (Iterable[Image])

        delay : The delay after the image is shown (int)

        loop : Loop the animation if True, does not loop otherwise (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the delay is negative
        """
        # Check types
        if not isinstance(image_list, Iterable):
            raise TypeError(f"invalid type : {type(image_list)} is not a Iterable")
        for image in image_list:
            if not isinstance(image, Image):
                raise TypeError(f"invalid type : {type(image)} is not an Image")
        if not isinstance(delay, int):
            raise TypeError(f"invalid type : {type(delay)} is not a int")
        if delay < 0:
            raise ValueError("the delay can not be negative")
        if not isinstance(loop, bool):
            raise TypeError(f"invalid type : {type(loop)} is not a bool")
        one_time = True
        while (loop or one_time) and self.__run:
            for image in image_list:
                if not self.__run:
                    break
                self.__show_image(image)
                sleep(delay / 1000)
            one_time = False

    def scroll_animation(
        self, image_list: Iterable, delay: int, loop: bool, monospace: bool
    ):
        """Scroll an animation

        Parameters:
        -----------
        image_list : The iterable of image (Iterable[Image])

        delay : The delay after the image is shown (int)

        loop : Loop the animation if True, does not loop otherwise (bool)

        monospace : Normalized space if True, not normalized otherwise (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the delay is negative
        """
        # Check types
        if not isinstance(image_list, Iterable):
            raise TypeError(f"invalid type : {type(image_list)} is not a Iterable")
        for image in image_list:
            if not isinstance(image, Image):
                raise TypeError(f"invalid type : {type(image)} is not an Image")
        if not isinstance(delay, int):
            raise TypeError(f"invalid type : {type(delay)} is not a int")
        if delay < 0:
            raise ValueError("the delay can not be negative")
        if not isinstance(loop, bool):
            raise TypeError(f"invalid type : {type(loop)} is not a bool")
        if not isinstance(monospace, bool):
            raise TypeError(f"invalid type : {type(monospace)} is not a bool")
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
            new_image = Image(width=width + img_width + offset, height=5)
            # Copy the old image in the new image
            new_image.blit(old_image, 0, 0, width, 5, 0, 0)
            # Copy the image from the list
            new_image.blit(image, 0, 0, img_width, 5, width - 1 + offset, 0)
            width += img_width + offset
        # Start the loop
        one_time = True
        while (loop or one_time) and self.__run:
            image = new_image
            width = image.width()
            while (width > 0) and self.__run:
                self.__show_image(image)
                image = image.shift_left(1)
                sleep(delay / 1000)
                width -= 1
            one_time = False

    def __show_image(self, image: Image):
        """Show an image

        Parameters:
        -----------
        image : The image to display (Image)
        """
        for x in range(5):
            for y in range(5):
                self.set_pixel(x, y, image.get_pixel(x, y))

    def __remove_void(self, image: Image) -> Image:
        """Resize an image to remove the void around it

        Parameters:
        -----------
        image : The requested image (Image)

        Returns:
        --------
        cropped_image : The cropped image (Image)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(image, Image):
            raise TypeError(f"invalid type : {type(image)} is not a Image")
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
            return Image("")
        else:
            return image.crop(min_x, 0, max_x + 1 - min_x, image.height())
