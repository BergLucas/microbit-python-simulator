from typing import Literal, Optional, Union

from microbit_client.pin import MicroBitDigitalPin

EVEN = 2
ODD = 1


def init(  # noqa: PLR0913
    baudrate: int = 9600,
    bits: Literal[8] = 8,
    parity: Literal[None, 1, 2] = None,
    stop: Literal[1] = 1,
    *,
    tx: Optional[MicroBitDigitalPin] = None,
    rx: Optional[MicroBitDigitalPin] = None
) -> None:
    """Initialize serial communication with the specified parameters.

    It will apply on the specified `tx` and `rx` pins.

    Note that for correct communication, the parameters have to be the same
    on both communicating devices.

    .. warning::
        Initializing the UART on external pins will cause the Python console on USB
        to become unaccessible, as it uses the same hardware. To bring the console
        back you must reinitialize the UART without passing anything for `tx` or `rx`
        (or passing `None` to these arguments). This means that calling
        `uart.init(115200)` is enough to restore the Python console.

    The `baudrate` defines the speed of communication. Common baud rates include:
    - 9600
    - 14400
    - 19200
    - 28800
    - 38400
    - 57600
    - 115200

    The `bits` defines the size of bytes being transmitted,
    and the board only supports 8.

    The `parity` parameter defines how parity is checked, and it can be `None`,
    `microbit.uart.ODD` or `microbit.uart.EVEN`.

    The `stop` parameter tells the number of stop bits, and has to be 1 for this board.

    If `tx` and `rx` are not specified then the internal USB-UART TX/RX pins are used
    which connect to the USB serial converter on the micro:bit, thus connecting the UART
    to your PC. You can specify any other pins you want by passing the desired pin
    objects to the `tx` and `rx` parameters.

    .. note::
        When connecting the device, make sure you “cross” the wires - the TX pin on your
        board needs to be connected with the RX pin on the device, and the RX pin - with
        the TX pin on the device. Also make sure the ground pins of both devices
        are connected.

    Args:
        baudrate (int, optional): The speed of communication. Defaults to 9600.
        bits (Literal[8], optional): The size of bytes being transmitted. Defaults to 8.
        parity (Literal[None, 1, 2], optional): How parity is checked. Defaults to None.
        stop (Literal[1], optional): The number of stop bits. Defaults to 1.
        tx (Optional[MicroBitDigitalPin], optional): The TX pin to use.
            Defaults to None.
        rx (Optional[MicroBitDigitalPin], optional): The RX pin to use.
            Defaults to None.
    """
    ...


def any() -> bool:
    """Return `True` if any data is waiting, else `False`."""
    ...


def read(nbytes: Optional[int] = None) -> Optional[bytes]:
    """Read bytes. If `nbytes` is specified then read at most that many bytes.

    Otherwise read as many bytes as possible.

    A bytes object contains a sequence of bytes.
    Because [ASCII](https://en.wikipedia.org/wiki/ASCII) characters can fit in single
    bytes this type of object is often used to represent simple text and offers methods
    to manipulate it as such, e.g. you can display the text using
    the `print()` function.

    You can also convert this object into a string object, and if there are
    non-ASCII characters present the encoding can be specified:

    ```python
    msg_bytes = uart.read()
    msg_str = str(msg, 'UTF-8')
    ```

    .. note::
        The timeout for all UART reads depends on the baudrate and is otherwise not
        changeable via Python. The timeout, in milliseconds, is given by:
        `microbit_uart_timeout_char = 13000 / baudrate + 1`

    .. note::
        The internal UART RX buffer is 64 bytes, so make sure data is read before the
        buffer is full or some of the data might be lost.

    .. warning:
        Receiving `0x03` will stop your program by raising a Keyboard Interrupt.
        You can enable or disable this using `micropython.kbd_intr()`.

    Args:
        nbytes (Optional[int], optional): The number of bytes to read. Defaults to None.

    Returns:
        Optional[bytes]: A bytes object or `None` on timeout.
    """
    ...


def readall() -> Optional[bytes]:
    """Removed since version 1.0.

    Instead, use `uart.read()` with no arguments, which will read as much data as
    possible.

    Returns:
        Optional[bytes]: The bytes read or `None` on timeout.
    """
    return read()


def readInto(  # noqa: N802
    buf: bytearray, nbytes: Optional[int] = None
) -> Optional[int]:
    """Read bytes into the `buf`. If `nbytes` is specified then read at most that many.

    Otherwise, read at most `len(buf)` bytes.

    Args:
        buf (bytearray): The buffer to read into.
        nbytes (Optional[int], optional): The number of bytes to read. Defaults to None.

    Returns:
        Optional[int]: The number of bytes read and stored into `buf` or `None`
            on timeout.
    """
    ...


def readline() -> Optional[bytes]:
    """Read a line, ending in a newline character.

    Returns:
        Optional[bytes]: The line read or `None` on timeout. The newline character is
            included in the returned bytes.
    """
    ...


def write(buf: Union[str, bytes, bytearray]) -> Optional[int]:
    """Write the buffer to the bus, it can be a bytes object or a string.

    ```python
    uart.write('hello world')
    uart.write(b'hello world')
    uart.write(bytes([1, 2, 3]))
    ```

    Args:
        buf (Union[str, bytes, bytearray]): The buffer to write.

    Returns:
        Optional[int]: The number of bytes written or None on timeout.
    """
    ...
