from queue import Empty, Queue
from threading import Thread
from time import time
from typing import Optional

from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.commands.radio import (
    MAX_CHANNEL,
    MAX_GROUP,
    MAX_LENGTH,
    MAX_POWER,
    MIN_CHANNEL,
    MIN_GROUP,
    MIN_LENGTH,
    MIN_POWER,
    RadioSendBytesCommand,
)
from microbit_protocol.exceptions import CommunicationClosedError
from microbit_protocol.peer import MicrobitWebsocketPeer

RATE_250KBIT = 250
"""Deprecated.

This rate is possible with micro:bit V1,
but it is not guaranteed to work on V2,
so it has been deprecated for compatibility reasons.
"""

RATE_1MBIT = 1000
"""Constant used to indicate a throughput of 1 Mbit a second."""

RATE_2MBIT = 2000
"""Constant used to indicate a throughput of 2 Mbit a second."""

MIN_QUEUE = 0

MESSAGE_PREFIX = b"\x01\x00\x01"

SECONDS_TO_MICROSECONDS = 1000000

INVERT_POWER_TO_RSSI = 8


class Radio:
    """This type represents a micro:bit's radio client."""

    def __init__(self, host: str, port: int) -> None:
        """Initialises `self` to a new Radio instance.

        Args:
            host (str): The host to connect to.
            port (int): The port to connect to.
        """
        self.__peer: Optional[MicrobitWebsocketPeer] = None
        self.__host = host
        self.__port = port
        self.reset()

    def on(self) -> None:
        """Enable the radio."""
        if self.__peer is not None:
            return

        self.__peer = MicrobitWebsocketPeer.connect(self.__host, self.__port)

        def listener(command: MicrobitCommand) -> None:
            if (
                not isinstance(command, RadioSendBytesCommand)
                or command.address != self.__address
                or command.channel != self.__channel
                or command.group != self.__group
                or self.__queue.full()
            ):
                return

            self.__queue.put(
                (
                    command.message,
                    (MAX_POWER - command.power) * INVERT_POWER_TO_RSSI,
                    round(time() * SECONDS_TO_MICROSECONDS),
                )
            )

        self.__peer.add_listener(listener)

        def listen(peer: MicrobitWebsocketPeer) -> None:
            try:
                peer.listen()
            except CommunicationClosedError:
                self.off()

        Thread(target=listen, args=(self.__peer,), daemon=True).start()

    def off(self) -> None:
        """Disable the radio."""
        if self.__peer is None:
            return

        self.__peer.stop()
        self.__peer.close()
        self.__peer = None

    def config(  # noqa: PLR0913
        self,
        *,
        length: int = 32,
        queue: int = 3,
        channel: int = 7,
        power: int = 6,
        address: int = 0x75626974,
        group: int = 0,
        data_rate: int = RATE_1MBIT,
    ) -> None:
        """Configure the radio.

        Args:
            length (int, optional): The maximum length of a message in bytes.
                Defaults to 32.
            queue (int, optional): The maximum number of messages that can be stored
                in the queue. Defaults to 3.
            channel (int, optional): The radio channel. Defaults to 7.
            power (int, optional): The radio power. Defaults to 6.
            address (int, optional): The radio address. Defaults to 0x75626974.
            group (int, optional): The radio group. Defaults to 0.
            data_rate (int, optional): The radio data rate. Defaults to RATE_1MBIT.
        """
        if length < MIN_LENGTH or MAX_LENGTH < length:
            raise ValueError("length must be between 0 and 251")

        if queue < MIN_QUEUE:
            raise ValueError("queue must be greater than 0")

        if channel < MIN_CHANNEL or MAX_CHANNEL < channel:
            raise ValueError("channel must be between 0 and 83")

        if power < MIN_POWER or MAX_POWER < power:
            raise ValueError("power must be between 0 and 7")

        if group < MIN_GROUP or MAX_GROUP < group:
            raise ValueError("group must be between 0 and 255")

        if data_rate not in {RATE_250KBIT, RATE_1MBIT, RATE_2MBIT}:
            raise ValueError("data_rate must be RATE_250KBIT, RATE_1MBIT or RATE_2MBIT")

        self.__length = length
        self.__queue: Queue[tuple[bytes, int, int]] = Queue(queue)
        self.__channel = channel
        self.__power = power
        self.__address = address
        self.__group = group

    def reset(self) -> None:
        """Reset the radio to the default configuration."""
        self.config()

    def send_bytes(self, message: bytes) -> None:
        """Send a message in bytes.

        Args:
            message (bytes): The message to be sent.

        Raises:
            ValueError: If the message is too long as specified in config().
        """
        assert isinstance(
            message, bytes
        ), f"message must be bytes, not {type(message).__name__}"

        if self.__peer is None:
            return

        if len(message) > self.__length:
            raise ValueError(
                f"message must be between 0 and {self.__length} bytes long"
            )

        self.__peer.send_command(
            RadioSendBytesCommand(
                address=self.__address,
                channel=self.__channel,
                group=self.__group,
                power=self.__power,
                message=message,
            )
        )

    def receive_bytes(self) -> Optional[bytes]:
        """Receive a message in bytes.

        Returns:
            Optional[bytes]: The message received or None if no message.
        """
        if self.__peer is None:
            return None

        try:
            message, _, _ = self.__queue.get_nowait()
            return message
        except Empty:
            return None

    def receive_bytes_into(self, buffer: bytearray) -> Optional[int]:
        """Receive a message in bytes into a buffer.

        Args:
            buffer (bytearray): The buffer to receive the message.

        Returns:
            Optional[int]: The number of bytes received or None if no message.
        """
        if self.__peer is None:
            return None

        message = self.receive_bytes()

        if message is None:
            return None

        buffer[0 : min(len(message), len(buffer))] = message

        return len(message)

    def send(self, message: str) -> None:
        """Send a message.

        Args:
            message (str): The message to be sent.

        Raises:
            ValueError: If the message is too long as specified in config().
        """
        assert isinstance(
            message, str
        ), f"message must be a str, not {type(message).__name__}"
        self.send_bytes(MESSAGE_PREFIX + bytes(message, "utf8"))

    def receive(self) -> Optional[str]:
        """Receive a message.

        Raises:
            ValueError: If the message conversion from bytes to string fails.

        Returns:
            Optional[str]: The message received or None if no message.
        """
        if self.__peer is None:
            return None

        message = self.receive_bytes()

        if message is None:
            return None

        if not message.startswith(MESSAGE_PREFIX):
            raise ValueError("message does not start with \\x01\\x00\\x01")

        try:
            return str(message, "utf8")
        except ValueError as e:
            raise ValueError("Conversion from bytes to string failed") from e

    def receive_full(self) -> Optional[tuple[bytes, int, int]]:
        """Receive a message with metadata.

        Returns:
            Optional[tuple[bytes, int, int]]: The message received
                or None if no message.
        """
        if self.__peer is None:
            return None

        try:
            return self.__queue.get_nowait()
        except Empty:
            return None
