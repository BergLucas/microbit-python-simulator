from microbit_client.pin import MicroBitDigitalPin
from microbit._internal import pin13, pin15, pin14
from typing import Union


def init(
    baudrate: int = 1000000,
    bits: int = 8,
    mode: int = 0,
    sclk: MicroBitDigitalPin = pin13,
    mosi: MicroBitDigitalPin = pin15,
    miso: MicroBitDigitalPin = pin14,
) -> None:
    """Initialize SPI communication with the specified parameters on the specified pins. Note that for correct communication, the parameters have to be the same on both communicating devices.

    The `baudrate` defines the speed of communication.

    The `bits` defines the size of bytes being transmitted. Currently only bits=8 is supported. However, this may change in the future.

    The `mode` determines the combination of clock polarity and phase according to the following convention, with polarity as the high order bit and phase as the low order bit:

    +----------+-----------------+---------------+
    | SPI Mode | Polarity (CPOL) | Phase (CPHA)  |
    +==========+=================+===============+
    | 0        | 0               | 0             |
    | 1        | 0               | 1             |
    | 2        | 1               | 0             |
    | 3        | 1               | 1             |
    +----------+-----------------+---------------+

    Polarity (aka CPOL) 0 means that the clock is at logic value 0 when idle and goes high (logic value 1) when active;
    polarity 1 means the clock is at logic value 1 when idle and goes low (logic value 0) when active.
    Phase (aka CPHA) 0 means that data is sampled on the leading edge of the clock, and 1 means on the trailing edge
    (viz. https://en.wikipedia.org/wiki/Signal_edge).

    The `sclk`, `mosi` and `miso` arguments specify the pins to use for each type of signal.

    Args:
        baudrate (int, optional): the speed of communication. Defaults to 1000000.
        bits (int, optional): the size of bytes being transmitted. Defaults to 8.
        mode (int, optional): the combination of clock polarity and phase. Defaults to 0.
        sclk (MicroBitDigitalPin, optional): the pin to use for the clock signal. Defaults to pin13.
        mosi (MicroBitDigitalPin, optional): the pin to use for the MOSI signal. Defaults to pin15.
        miso (MicroBitDigitalPin, optional): the pin to use for the MISO signal. Defaults to pin14.
    """
    ...


def read(nbytes: int) -> bytes:
    """Read at most `nbytes`. Returns what was read.

    Args:
        nbytes (int): the maximum number of bytes to read

    Returns:
        bytes: the bytes read
    """
    ...


def write(buffer: Union[bytes, bytearray]) -> None:
    """Write the `buffer` of bytes to the bus.

    Args:
        buffer (bytes): the bytes to write
    """
    ...


def write_readinto(out: Union[bytes, bytearray], in_: bytearray) -> None:
    """Write the `out` buffer to the bus and read any response into the `in_` buffer.

    The length of the buffers should be the same.

    The buffers can be the same object.

    Args:
        out (Union[bytes, bytearray]): the bytes to write
        in_ (bytearray): the buffer to read into
    """
    ...
