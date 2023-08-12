from typing import Union, overload

from microbit_client.image import Image  # noqa: F401

from microbit import (
    accelerometer,  # noqa: F401
    compass,  # noqa: F401
    display,
    ic2,  # noqa: F401
    spi,  # noqa: F401
    uart,  # noqa: F401
)
from microbit._internal import (
    button_a,  # noqa: F401
    button_b,  # noqa: F401
    pin0,  # noqa: F401
    pin1,  # noqa: F401
    pin2,  # noqa: F401
    pin3,  # noqa: F401
    pin4,  # noqa: F401
    pin5,  # noqa: F401
    pin6,  # noqa: F401
    pin7,  # noqa: F401
    pin8,  # noqa: F401
    pin9,  # noqa: F401
    pin10,  # noqa: F401
    pin11,  # noqa: F401
    pin12,  # noqa: F401
    pin13,  # noqa: F401
    pin14,  # noqa: F401
    pin15,  # noqa: F401
    pin16,  # noqa: F401
    pin19,  # noqa: F401
    pin20,  # noqa: F401
)
from microbit._internal import (
    microbit as __microbit,
)


def panic(n: int) -> None:
    """Enter a panic mode that stops all execution.

    The panic mode scrolls an error code in the micro:bit display and requires restart.

    ```python
    microbit.panic(255)
    ```

    Args:
        n (int): An arbitrary integer between 0 and 255 to indicate an error code.
    """
    display.scroll(n, monospace=True, loop=True)


def reset() -> None:
    """Restart the board."""
    __microbit.reset()


def sleep(n: Union[int, float]) -> None:
    """Wait for `n` milliseconds.

    One second is 1000 milliseconds, so `microbit.sleep(1000)`
    will pause the execution for one second.

    Args:
        n (Union[int, float]): An integer or floating point number
            indicating the number of milliseconds to wait.
    """
    __microbit.sleep(n)


def running_time() -> Union[int, float]:
    """Returns the number of milliseconds since the board was switched on or restarted.

    Returns:
        Union[int, float]: The number of milliseconds since the board
            was switched on or restarted.
    """
    return __microbit.running_time()


@overload
def scale(
    value: Union[int, float],
    from_: tuple[Union[int, float], Union[int, float]],
    to: Union[tuple[float, float], tuple[int, float], tuple[float, int]],
) -> float:
    """Converts a value from a range to another range.

    For example, to convert 30 degrees from Celsius to Fahrenheit:

    ```python
    temp_fahrenheit = scale(30, from_=(0.0, 100.0), to=(32.0, 212.0))
    ```

    This can be useful to convert values between inputs and outputs,
    for example an accelerometer x value to a speaker volume.

    If one of the numbers in the `to` parameter is a floating point
    (i.e a decimal number like `10.0`), this function will return a floating
    point number. If they are both integers (i.e `10`), it will return an integer:

    ```python
    returns_int = scale(accelerometer.get_x(), from_=(-2000, 2000), to=(0, 255))
    ```

    Negative scaling is also supported, for example
    `scale(25, from_=(0, 100), to=(0, -200))` will return `-50`.

    Args:
        value (Union[int, float]): A number to convert.
        from_ (tuple[Union[int, float], Union[int, float]]): A tuple
            to define the range to convert from.
        to (Union[tuple[float, float], tuple[int, float], tuple[float, int]]): A tuple
            to define the range to convert to.

    Returns:
        float: The `value` converted to the `to` range.
    """


@overload
def scale(
    value: Union[int, float],
    from_: tuple[Union[int, float], Union[int, float]],
    to: tuple[int, int],
) -> int:
    """Converts a value from a range to another range.

    Args:
        value (Union[int, float]): A number to convert.
        from_ (tuple[Union[int, float], Union[int, float]]): A tuple
            to define the range to convert from.
        to (tuple[int, int]): A tuple to define the range to convert to.

    Returns:
        int: The `value` converted to the `to` range.
    """


def scale(
    value: Union[int, float],
    from_: tuple[Union[int, float], Union[int, float]],
    to: tuple[Union[int, float], Union[int, float]],
) -> Union[int, float]:
    """Converts a value from a range to another range.

    Args:
        value (Union[int, float]): A number to convert.
        from_ (tuple[Union[int, float], Union[int, float]]): A tuple
            to define the range to convert from.
        to (tuple[Union[int, float], Union[int, float]]): A tuple
            to define the range to convert to.

    Returns:
        Union[int, float]: The `value` converted to the `to` range.
    """
    return __microbit.scale(value, from_, to)


def temperature() -> int:
    """Returns the temperature of the micro:bit in degrees Celcius.

    Returns:
        int: An integer with the temperature of the micro:bit in degrees Celcius.
    """
    return __microbit.temperature()
