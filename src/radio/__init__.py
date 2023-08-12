from typing import Optional

from microbit_client.radio import (
    RATE_1MBIT,  # noqa: F401
    RATE_2MBIT,  # noqa: F401
    RATE_250KBIT,  # noqa: F401
)

from radio._internal import radio as __radio


def on() -> None:
    """Turns the radio on.

    Since MicroPython-on-micro:bit v1.1 the radio is turned on by default
    when the radio module is imported. In earlier releases, to reduce power
    consumption until needed, this function had to be explicitly called.
    For those cases `radio.off()` can be called after import.
    """
    __radio.on()


def off() -> None:
    """Turns off the radio, thus saving power and memory."""
    __radio.off()


def config(  # noqa: PLR0913
    *,
    length: int = 32,
    queue: int = 3,
    channel: int = 7,
    power: int = 6,
    address: int = 0x75626974,
    group: int = 0,
    data_rate: int = RATE_1MBIT,
) -> None:
    """Configures various keyword based settings relating to the radio.

    The available settings and their sensible default values are listed below.

    The `length` (default=32) defines the maximum length, in bytes, of a message
    sent via the radio. It can be up to 251 bytes long
    (254 - 3 bytes for S0, LENGTH and S1 preamble).

    The `queue` (default=3) specifies the number of messages that can be stored on
    the incoming message queue. If there are no spaces left on the queue for incoming
    messages, then the incoming message is dropped.

    The `channel` (default=7) can be an integer value from 0 to 83 (inclusive)
    that defines an arbitrary “channel” to which the radio is tuned.
    Messages will be sent via this channel and only messages received via
    this channel will be put onto the incoming message queue.
    Each step is 1MHz wide, based at 2400MHz.

    The `power` (default=6) is an integer value from 0 to 7 (inclusive) to indicate
    the strength of signal used when broadcasting a message.
    The higher the value the stronger the signal, but the more power is consumed
    by the device. The numbering translates to positions in the following list of
    dBm (decibel milliwatt) values: -30, -20, -16, -12, -8, -4, 0, 4.

    The `address` (default=0x75626974) is an arbitrary name, expressed as a
    32-bit address, that's used to filter incoming packets at the hardware level,
    keeping only those that match the address you set. The default used by other
    micro:bit related platforms is the default setting used here.

    The `group` (default=0) is an 8-bit value (0-255) used with the `address` when
    filtering messages. Conceptually, "address" is like a house/office address and
    "group" is like the person at that address to which you want to send your message.

    The `data_rate` (default=radio.RATE_1MBIT) indicates the speed at which data
    throughput takes place. Can be one of the following contants defined in the
    `radio` module : `RATE_1MBIT` or `RATE_2MBIT`.

    If `config` is not called then the defaults described above are assumed.

    Args:
        length (int, optional): The maximum length of a message sent via the radio.
            Defaults to 32.
        queue (int, optional): The number of messages that can be stored on the
            incoming message queue. Defaults to 3.
        channel (int, optional): The channel to which the radio is tuned.
            Defaults to 7.
        power (int, optional): The strength of signal used when broadcasting
            a message. Defaults to 6.
        address (int, optional): The address used to filter incoming packets.
            Defaults to 0x75626974.
        group (int, optional): The group used with the address when filtering messages.
            Defaults to 0.
        data_rate (int, optional): The speed at which data throughput takes place.
            Defaults to RATE_1MBIT.
    """
    __radio.config(
        length=length,
        queue=queue,
        channel=channel,
        power=power,
        address=address,
        group=group,
        data_rate=data_rate,
    )


def reset() -> None:
    """Reset the settings to their default values.

    (As listed in the documentation for the `config` function above).
    """
    __radio.reset()


def send_bytes(message: bytes) -> None:
    """Sends a message containing bytes.

    Args:
        message (bytes): The message to send.
    """
    __radio.send_bytes(message)


def receive_bytes() -> Optional[bytes]:
    """Receive the next incoming message on the message queue.

    Returns `None` if there are no pending messages. Messages are returned as bytes.

    Returns:
        Optional[bytes]: The next incoming message on the message queue.
    """
    return __radio.receive_bytes()


def receive_bytes_into(buffer: bytearray) -> Optional[int]:
    """Receive the next incoming message on the message queue.

    Copies the message into `buffer`, trimming the end of the message if necessary.

    Returns `None` if there are no pending messages,
    otherwise it returns the length of the message
    (which might be more than the length of the buffer).

    Args:
        buffer (bytearray): The buffer to receive the message.

    Returns:
        Optional[int]: The number of bytes received or None if no message.
    """
    return __radio.receive_bytes_into(buffer)


def send(message: str) -> None:
    r"""Sends a message string.

    This is the equivalent of `send_bytes(bytes(message, 'utf8'))`
    but with `b'\x01\x00\x01'` prepended to the front
    (to make it compatible with other platforms that target the micro:bit).

    Args:
        message (str): The message to send.

    Raises:
        ValueError: If the message is too long as specified in config().
    """
    __radio.send(message)


def receive() -> Optional[str]:
    r"""Works in exactly the same way as `receive_bytes` but returns whatever was sent.

    Currently, it's equivalent to `str(receive_bytes(), 'utf8')` but with a check that
    the the first three bytes are `b'\x01\x00\x01'` (to make it compatible with other
    platforms that may target the micro:bit).

    It strips the prepended bytes before converting to a string.

    A `ValueError` exception is raised if conversion to string fails.

    Raises:
        ValueError: If the message conversion from bytes to string fails.

    Returns:
        Optional[str]: The message received or None if no message.
    """
    return __radio.receive()


def receive_full() -> Optional[tuple[bytes, int, int]]:
    """Returns a tuple containing three values representing the next incoming message.

    The incoming message comes from the message queue.
    If there are no pending messages then `None` is returned.

    The three values in the tuple represent:

    - the next incoming message on the message queue as bytes.
    - the RSSI (signal strength): a value between 0 (strongest) and
        -255 (weakest) as measured in dBm.
    - a microsecond timestamp: the value returned by `time.ticks_us()`
        when the message was received.

    For example:

    ```python
    details = radio.receive_full()
    if details:
        msg, rssi, timestamp = details
    ```

    This function is useful for providing information needed for triangulation and/or
    triliteration with other micro:bit devices.
    """
    return __radio.receive_full()
