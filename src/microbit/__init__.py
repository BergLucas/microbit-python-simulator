from typing import Union
from microbit._internal import microbit as __microbit
from microbit._internal.microbit.image import Image


class _MicroBitDigitalPin:
    """Digital pin on the Micro:Bit board"""

    def read_digital(self):
        """Return 1 if the pin is high, and 0 if it's low"""
        return 1

    def write_digital(self, value):
        """Set the pin to High if the value is 1, or else set it to 0"""
        a = value

    def __init__(self):
        a = 0


class _MicroBitAnalogDigitalPin:
    """Analog (PWM) pin on the Micro:Bit board"""

    def read_analog(self):
        """Reads the voltage applied to the pin, and return it as an integer between 0 (0V), and 1024 (3.3V)"""
        return 1023

    def write_analog(self, value):
        """Output a PWM signal on the pin, with a duty cycle proportional to provided value, where 0 = 0%, and 1023 = 100%"""
        a = value

    def set_analog_period(self, period):
        """Set the period of the PWM signal being output to period in ms. Minimum valid is 1ms"""
        a = period

    def set_analog_period_microseconds(self, period):
        """Set the period of the PWM signal being output to period in microseconds. Minimum valid is 256"""
        a = period

    def __init__(self):
        a = 0


class _MicroBitTouchPin:
    """Touch sensitive pin on the Micro:Bit board"""

    def is_touched(self):
        """Return True if the pin is being touched, otherwise False"""
        return True

    def __init__(self):
        a = 0


class _MicroBitAnalogDigitalPinReadOnly:
    """Read only PWM pin"""

    def read_analog(self):
        """Reads the voltage applied to the pin, and return it as an integer between 0 (0V), and 1024 (3.3V)"""
        return 1023

    def __init__(self):
        a = 0


pin0 = _MicroBitTouchPin()
pin1 = _MicroBitTouchPin()
pin2 = _MicroBitTouchPin()
pin3 = _MicroBitAnalogDigitalPin()
pin4 = _MicroBitAnalogDigitalPin()
pin5 = _MicroBitDigitalPin()
pin6 = _MicroBitDigitalPin()
pin7 = _MicroBitDigitalPin()
pin8 = _MicroBitDigitalPin()
pin9 = _MicroBitDigitalPin()
pin10 = _MicroBitAnalogDigitalPin()
pin11 = _MicroBitDigitalPin()
pin12 = _MicroBitAnalogDigitalPin()
pin13 = _MicroBitDigitalPin()
pin14 = _MicroBitDigitalPin()
pin15 = _MicroBitDigitalPin()
pin16 = _MicroBitDigitalPin()
pin19 = _MicroBitDigitalPin()
pin20 = _MicroBitDigitalPin()


class _spi:
    def init(
        self, baudrate=1000000, bits=8, mode=0, sclk=pin13, mosi=pin15, miso=pin14
    ):
        """see: https://microbit-micropython.readthedocs.io/en/latest/spi.html"""

    def read(self, nbytes):
        """Read at most nbytes. Returns what was read."""

    def write(self, buffer):
        """Write the buffer of bytes to the bus."""

    def write_readinto(self, out, inBuffer):
        """Write the out buffer to the bus and read any response into the in buffer. The length of the buffers should be the same. The buffers can be the same object."""


class _uart:
    def init(self, baudrate=9600, bits=8, parity=None, stop=1, *, tx=None, rx=None):
        """Initialize serial communication with the specified parameters on the specified tx and rx pins. Note that for correct communication, the parameters have to be the same on both communicating devices."""

    def any(self):
        """Return True if any data is waiting, else False."""
        return True

    def read(self, nBytes=None):
        """Read at most n Bytes if the parameter is set, else read as much as can be read.
        Returns a Byte array if data can be read, otherwise returns None."""
        return None

    def readInto(self, buf, nBytes=None):
        """Read bytes into the buf. If nbytes is specified then read at most that many bytes. Otherwise, read at most len(buf) bytes.
        Return value: number of bytes read and stored into buf or None on timeout."""

    def readline(self):
        """Read a line, ending in a newline character.
        Return value: the line read or None on timeout. The newline character is included in the returned bytes."""

    def write(self, buf):
        """Write the buffer to the bus, it can be a bytes object or a string.
        Return value: number of bytes written or None on timeout."""


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


button_a = __microbit.button_a
button_b = __microbit.button_b

spi = _spi()
uart = _uart()
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
