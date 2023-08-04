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
from microbit import display, spi, uart
from microbit_client.image import Image
import time, time as utime
from typing import Union


class _i2c:
    def init(self, freq=100000, sda=pin20, scl=pin19):
        """Re-initialize peripheral with the specified clock frequency freq on the specified sda and scl pins.
        Warning
        Changing the I²C pins from defaults will make the accelerometer and compass stop working, as they are connected internally to those pins."""

    def scan(self):
        """Scan the bus for devices. Returns a list of 7-bit addresses corresponding to those devices that responded to the scan."""
        return []

    def read(self, addr, n, repeat=False):
        """Read n bytes from the device with 7-bit address addr. If repeat is True, no stop bit will be sent."""

    def write(self, addr, buf, repeat=False):
        """Write bytes from buf to the device with 7-bit address addr. If repeat is True, no stop bit will be sent."""


class _compass:
    def calibrate(self):
        """Starts the calibration process. An instructive message will be scrolled to the user after which they will need to rotate the device in order to draw a circle on the LED display."""

    def is_calibrated(self):
        """Returns True if the compass has been successfully calibrated, and returns False otherwise."""
        return True

    def clear_calibration(self):
        """Undoes the calibration, making the compass uncalibrated again."""

    def get_x(self):
        """Gives the reading of the magnetic field strength on the x axis in nano tesla, as a positive or negative integer, depending on the direction of the field."""
        return 0

    def get_y(self):
        """Gives the reading of the magnetic field strength on the y axis in nano tesla, as a positive or negative integer, depending on the direction of the field."""
        return 0

    def get_z(self):
        """Gives the reading of the magnetic field strength on the z axis in nano tesla, as a positive or negative integer, depending on the direction of the field."""
        return 0

    def heading(self):
        """Gives the compass heading, calculated from the above readings, as an integer in the range from 0 to 360, representing the angle in degrees, clockwise, with north as 0."""
        return 0

    def get_field_strength(self):
        """Returns an integer indication of the magnitude of the magnetic field around the device in nano tesla."""
        return 0


i2c = _i2c()
compass = _compass()

# Microbit functions


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
