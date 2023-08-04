from microbit._internal import (
    microbit as __microbit,
    button_a,
    button_b,
    pin0,
    pin1,
    pin2,
    pin3,
    pin4,
    pin5,
    pin6,
    pin7,
    pin8,
    pin9,
    pin10,
    pin11,
    pin12,
    pin13,
    pin14,
    pin15,
    pin16,
    pin19,
    pin20,
)
from microbit import display, spi, uart, ic2, compass
from microbit_client.image import Image
import time, time as utime
from typing import Union


def panic(error_code: int) -> None:
    """Enter a panic mode that stops all execution, scrolls an error code in the micro:bit display and requires restart:

    ```python
    microbit.panic(255)
    ```

    Args:
        n (int): An arbitrary integer between 0 and 255 to indicate an error code.
    """
    __microbit.panic(error_code)


def reset() -> None:
    """Restart the board."""
    __microbit.reset()


def sleep(n: Union[int, float]) -> None:
    """Wait for `n` milliseconds.

    One second is 1000 milliseconds, so `microbit.sleep(1000)`
    will pause the execution for one second.

    Args:
        n (Union[int, float]) : An integer or floating point number indicating the number of milliseconds to wait."""
    __microbit.sleep(n)


def running_time() -> Union[int, float]:
    """Returns the number of milliseconds since the board was switched on or restarted.

    Returns:
        Union[int, float] : The number of milliseconds since the board was switched on or restarted.
    """
    return __microbit.running_time()


def temperature() -> int:
    """Returns the temperature of the micro:bit in degrees Celcius.

    Returns:
        int : An integer with the temperature of the micro:bit in degrees Celcius.
    """
    return __microbit.temperature()
