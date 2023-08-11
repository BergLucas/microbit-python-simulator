from typing import Union

from microbit_client.pin import MicroBitDigitalPin

from microbit._internal import pin19, pin20


def init(
    freq: int = 100000, sda: MicroBitDigitalPin = pin20, scl: MicroBitDigitalPin = pin19
) -> None:
    """Re-initialize peripheral with the specified clock frequency `freq`.

      This frequency will apply on the specified `sda` and `scl` pins.

    .. warning::
        Changing the I²C pins from defaults will make the accelerometer and
        compass stop working, as they are connected internally to those pins.

    Args:
        freq (int, optional): The clock frequency. Defaults to 100000.
        sda (MicroBitDigitalPin, optional): The SDA pin to use. Defaults to pin20.
        scl (MicroBitDigitalPin, optional): The SCL pin to use. Defaults to pin19.
    """
    ...


def scan() -> list[int]:
    """Scan the bus for devices.

    Returns:
        list[int]: A list of 7-bit addresses corresponding to those devices
            that responded to the scan.
    """
    ...


def read(addr: int, n: int, repeat: bool = False) -> bytes:
    """Read `n` bytes from the device with 7-bit address `addr`.

    If `repeat` is `True`, no stop bit will be sent.

    Args:
        addr (int): The address of the device to read from.
        n (int): The number of bytes to read.
        repeat (bool, optional): Whether to send a stop bit after reading.
            Defaults to False.

    Returns:
        bytes: The bytes read.
    """
    ...


def write(addr: int, buf: Union[bytes, bytearray], repeat: bool = False) -> None:
    """Write bytes from `buf` to the device with 7-bit address `addr`.

    If `repeat` is `True`, no stop bit will be sent.

    Args:
        addr (int): The address of the device to write to.
        buf (Union[bytes, bytearray]): The bytes to write.
        repeat (bool, optional): Whether to send a stop bit after writing.
            Defaults to False.
    """
    ...
