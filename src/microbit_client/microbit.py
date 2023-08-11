import logging
import time
from typing import Union

from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.commands.microbit import (
    MicrobitResetCommand,
    MicrobitTemperatureCommand,
)
from microbit_protocol.peer import MicrobitPeer

logger = logging.getLogger(__name__)


class Microbit:
    """Microbit class for the client side."""

    def __init__(self, peer: MicrobitPeer) -> None:
        """Initialise a new Microbit instance.

        Args:
            peer (MicrobitPeer): The peer to communicate with.
        """
        self.__start_time = time.time()
        self.__peer = peer
        self.__temperature = 0

        def listener(command: MicrobitCommand) -> None:
            if isinstance(command, MicrobitTemperatureCommand):
                self.__temperature = command.temperature

        peer.add_listener(listener)

    def reset(self) -> None:
        """Reset the micro:bit."""
        self.__peer.send_command(MicrobitResetCommand())

    def sleep(self, n: Union[int, float]) -> None:
        """Sleep for n milliseconds.

        Args:
            n (Union[int, float]): The number of milliseconds to sleep for.
        """
        time.sleep(n / 1000)

    def running_time(self) -> Union[int, float]:
        """Get the number of milliseconds since the micro:bit was powered on.

        Returns:
            Union[int, float]: The number of milliseconds since the micro:bit
                was powered on.
        """
        return (time.time() - self.__start_time) * 1000

    def scale(
        self,
        value: Union[int, float],
        from_: tuple[Union[int, float], Union[int, float]],
        to: tuple[Union[int, float], Union[int, float]],
    ) -> Union[int, float]:
        """Scale a value from one range to another.

        Args:
            value (Union[int, float]): The value to scale.
            from_ (tuple[Union[int, float], Union[int, float]]): The range to
                scale from.
            to (tuple[Union[int, float], Union[int, float]]): The range to
                scale to.

        Returns:
            Union[int, float]: The scaled value.
        """
        from_min, from_max = from_
        to_min, to_max = to

        from_ratio = from_max - from_min
        to_ratio = to_max - to_min

        result = (value - from_min) / from_ratio * to_ratio + to_min

        if isinstance(to_min, float) or isinstance(to_max, float):
            return result
        else:
            return round(result)

    def temperature(self) -> int:
        """Get the temperature in degrees Celsius.

        Returns:
            int: The temperature in degrees Celsius.
        """
        return self.__temperature
