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
from microbit_client.image import Image
from typing import Union, Iterable
from threading import Thread
from time import sleep


class Display:
    def __init__(self, peer: MicrobitPeer) -> None:
        self.__peer = peer
        self.__light_level = 0
        self.on()
        self.clear()

        def listener(command: MicrobitCommand) -> None:
            if isinstance(command, MicrobitDisplayReadLightLevelCommand):
                self.__light_level = command.light_level

        peer.add_listener(listener)

    def get_pixel(self, x: int, y: int) -> int:
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"

        if x < 0 or 4 < x or y < 0 or 4 < y:
            raise ValueError(f"invalid position {x}, {y}")

        return self.__pixels[y][x]

    def set_pixel(self, x: int, y: int, value: int) -> None:
        assert isinstance(x, int), f"x must be an int, not {type(x).__name__}"
        assert isinstance(y, int), f"y must be an int, not {type(y).__name__}"
        assert isinstance(
            value, int
        ), f"value must be an int, not {type(value).__name__}"

        if value < 0 or 9 < value:
            raise ValueError("brightness out of bounds")

        if x < 0 or 4 < x or y < 0 or 4 < y:
            raise ValueError(f"invalid position {x}, {y}")

        self.__pixels[y][x] = value

        self.__peer.send_command(MicrobitDisplaySetPixelCommand(x=x, y=y, value=value))

    def clear(self) -> None:
        """Set the brightness of all LEDs to 0 (off)."""
        self.__pixels = [[0 for _ in range(5)] for _ in range(5)]
        self.__peer.send_command(MicrobitDisplayClearCommand())

    def show(
        self,
        image: Union[Image, str, float, int, Iterable[Image]],
        delay: int = 400,
        *,
        wait: bool = True,
        loop: bool = False,
        clear: bool = False,
    ) -> None:
        if isinstance(image, Image):
            self.__send_image(image)
            return

        assert isinstance(
            image, (str, float, int, Iterable)
        ), f"image must be a str, float, int or Iterable[Image], got {type(image).__name__}"
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

    def scroll(
        self,
        text: Union[str, int, float],
        delay: int = 150,
        *,
        wait: bool = True,
        loop: bool = False,
        monospace: bool = False,
    ) -> None:
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

        image = Image(4 + 5 * len(text), 5)

        for i, char in enumerate(text):
            image.blit(Image(char), 0, 0, 5, 5, 4 + 5 * i, 0)

        def target() -> None:
            self.__scroll_image(image, delay)
            while loop:
                self.__scroll_image(image, delay)

        if wait:
            target()
        else:
            Thread(target=target, daemon=True).start()

    def on(self) -> None:
        self.__is_on = True
        self.__peer.send_command(MicrobitDisplayOnCommand())

    def off(self) -> None:
        self.__is_on = False
        self.__peer.send_command(MicrobitDisplayOffCommand())

    def is_on(self) -> bool:
        return self.__is_on

    def read_light_level(self) -> int:
        return self.__light_level

    def __scroll_image(self, image: Image, delay: int) -> None:
        for i in range(image.width() + 1):
            self.__send_image(image.crop(i, 0, 5, 5))
            sleep(delay / 1000)

    def __send_images(self, images: Iterable[Image], delay: int) -> None:
        for image in images:
            self.__send_image(image)
            sleep(delay / 1000)

    def __send_image(self, image: Image) -> None:
        self.__peer.send_command(
            MicrobitDisplayShowCommand(
                image=[
                    [image.get_pixel(x, y) for x in range(image.width())]
                    for y in range(image.height())
                ]
            )
        )
