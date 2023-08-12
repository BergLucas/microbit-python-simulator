from __future__ import annotations

import logging
import socket
import sys
from contextlib import contextmanager
from enum import Enum, auto
from threading import Thread, main_thread
from typing import (
    TYPE_CHECKING,
    Callable,
    Generator,
    Iterator,
    Optional,
    Protocol,
    TextIO,
    Type,
)

from pydantic import ValidationError
from typing_extensions import override
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    ConnectionClosedOK,
)
from websockets.extensions.permessage_deflate import enable_server_permessage_deflate
from websockets.server import ServerProtocol
from websockets.sync.client import connect
from websockets.sync.server import ServerConnection

from microbit_protocol.commands import MicrobitCommand, MicrobitCommandAdapter
from microbit_protocol.exceptions import CommunicationClosedError

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self
    from websockets.sync.connection import Connection

logger = logging.getLogger(__name__)


class ExitStatus(Enum):
    """An enum representing the exit status of a peer."""

    SUCCESS = auto()
    ERROR = auto()


class MicrobitPeer(Protocol):
    """A protocol for a micro:bit peer."""

    def send_command(self, command: MicrobitCommand) -> None:
        """Sends a command to the peer.

        Args:
            command (MicrobitCommand): The command to send.

        Raises:
            CommunicationClosedError: If the communication channel is closed.
        """
        ...

    def add_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        """Adds a listener to the peer.

        Args:
            listener (Callable[[MicrobitCommand], None]): The listener to add.
        """
        ...

    def remove_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        """Removes a listener from the peer.

        Args:
            listener (Callable[[MicrobitCommand], None]): The listener to remove.
        """
        ...

    @property
    def listeners(self) -> set[Callable[[MicrobitCommand], None]]:
        """Returns a set of listeners.

        Returns:
            set[Callable[[MicrobitCommand], None]]: A set of listeners.
        """
        ...

    @property
    def is_listening(self) -> bool:
        """Returns whether the peer is listening.

        Returns:
            bool: Whether the peer is listening.
        """
        ...

    def listen(self) -> None:
        """Starts listening for commands.

        Raises:
            CommunicationClosedError: If the communication channel is closed.
        """
        ...

    def stop(self) -> None:
        """Stops listening for commands."""
        ...

    def close(self, code: ExitStatus = ExitStatus.SUCCESS, reason: str = "") -> None:
        """Closes the peer.

        Args:
            code (ExitStatus, optional): The exit status code.
                Defaults to ExitStatus.SUCCESS.
            reason (str, optional): The reason for closing. Defaults to "".
        """
        ...

    def __enter__(self) -> Self:
        """Enter the context manager.

        Returns:
            Self: The peer.
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the context manager.

        Args:
            exc_type (Optional[Type[BaseException]]): The exception type.
            exc_value (Optional[BaseException]): The exception value.
            traceback (Optional[TracebackType]): The traceback.
        """
        self.close(ExitStatus.SUCCESS if exc_type is None else ExitStatus.ERROR)


class MicrobitIoPeer(MicrobitPeer):
    """A peer that communicates over stdin and stdout."""

    def __init__(
        self,
        io_input: TextIO = sys.stdin,
        io_output: TextIO = sys.stdout,
        io_error: TextIO = sys.stderr,
        auto_close_io: bool = False,
    ) -> None:
        """Initializes `self` a new MicrobitIoPeer.

        Args:
            io_input (TextIO, optional): The input stream. Defaults to sys.stdin.
            io_output (TextIO, optional): The output stream. Defaults to sys.stdout.
            io_error (TextIO, optional): The error stream. Defaults to sys.stderr.
            auto_close_io (bool, optional): Whether to automatically close the streams.
                Defaults to False.
        """
        self.__io_input = io_input
        self.__io_output = io_output
        self.__io_error = io_error
        self.__auto_close_io = auto_close_io
        self.__listeners: set[Callable[[MicrobitCommand], None]] = set()
        self.__is_listening = False

    @override
    def send_command(self, command: MicrobitCommand) -> None:
        request = command.model_dump_json()

        self.__io_output.write(f"{request}\n")
        self.__io_output.flush()

    @override
    def add_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.add(listener)

    @override
    def remove_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.remove(listener)

    @property
    @override
    def listeners(self) -> set[Callable[[MicrobitCommand], None]]:
        return self.__listeners.copy()

    @property
    @override
    def is_listening(self) -> bool:
        return self.__is_listening

    @override
    def listen(self) -> None:
        self.__is_listening = True

        while self.__is_listening:
            try:
                response = self.__io_input.readline()[:-1]
            except Exception as e:
                raise CommunicationClosedError() from e

            try:
                command: MicrobitCommand = MicrobitCommandAdapter.validate_json(
                    response
                )  # type: ignore
            except ValidationError:
                logger.warning(f"Received invalid command: {response}")
                continue

            for listener in self.__listeners:
                listener(command)

    @override
    def stop(self) -> None:
        self.__is_listening = False

    @override
    def close(self, code: ExitStatus = ExitStatus.SUCCESS, reason: str = "") -> None:
        if code is ExitStatus.ERROR:
            self.__io_error.write("Error:\n")

        self.__io_error.write(f"{reason}\n")
        self.__io_error.flush()

        if self.__auto_close_io:
            self.__io_input.close()
            self.__io_output.close()
            self.__io_error.close()


class MicrobitWebsocketPeer(MicrobitPeer):
    """A peer that communicates over a websocket."""

    @classmethod
    def connect(cls, host: str, port: int) -> MicrobitWebsocketPeer:
        """Connects to a peer using a websocket.

        Args:
            host (str): The host.
            port (int): The port.

        Returns:
            MicrobitWebsocketPeer: The peer.
        """
        websocket = connect(f"ws://{host}:{port}")
        return MicrobitWebsocketPeer(websocket)

    @classmethod
    def wait_for_connection(cls, host: str, port: int) -> MicrobitWebsocketPeer:
        """Waits for a peer to connect using a websocket.

        Args:
            host (str): The host.
            port (int): The port.

        Returns:
            MicrobitWebsocketPeer: The peer.
        """
        with cls.accept_connections(host, port) as server:
            return next(server)

    @classmethod
    @contextmanager
    def accept_connections(
        cls, host: str, port: int
    ) -> Generator[Iterator[MicrobitWebsocketPeer], None, None]:
        """Accepts connections from peers using a websocket.

        Args:
            host (str): The host.
            port (int): The port.

        Yields:
            Generator[Iterator[MicrobitWebsocketPeer], None, None]: A context manager
                that yields a MicrobitWebsocketPeer server.
        """
        extensions = enable_server_permessage_deflate(None)

        server_socket = socket.create_server((host, port))
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

        def server() -> Iterator[MicrobitWebsocketPeer]:
            while True:
                peer_socket, _ = server_socket.accept()

                protocol = ServerProtocol(extensions=extensions)

                connection = ServerConnection(peer_socket, protocol)

                try:
                    connection.handshake()
                except Exception:
                    peer_socket.close()
                    continue

                yield MicrobitWebsocketPeer(connection)

        try:
            yield server()
        finally:
            server_socket.close()

    def __init__(self, websocket: Connection) -> None:
        """Initializes `self` a new MicrobitWebsocketPeer.

        Args:
            websocket (Connection): The websocket.
        """
        self.__websocket = websocket
        self.__listeners: set[Callable[[MicrobitCommand], None]] = set()
        self.__is_listening = False

        # Temporary fix because websockets create a non-daemon thread
        # that prevents the program from exiting
        # if the socket is not closed properly
        def close_socket_gracefully() -> None:
            main_thread().join()
            self.close(ExitStatus.SUCCESS)

        Thread(target=close_socket_gracefully).start()

    @override
    def send_command(self, command: MicrobitCommand) -> None:
        request = command.model_dump_json()

        try:
            self.__websocket.send(request)
        except ConnectionClosed as e:
            raise CommunicationClosedError() from e

    @override
    def add_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.add(listener)

    @override
    def remove_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.remove(listener)

    @property
    @override
    def listeners(self) -> set[Callable[[MicrobitCommand], None]]:
        return self.__listeners.copy()

    @property
    @override
    def is_listening(self) -> bool:
        return self.__is_listening

    @override
    def listen(self) -> None:
        self.__is_listening = True

        while self.__is_listening:
            try:
                response = self.__websocket.recv()
            except ConnectionClosedError as e:
                raise CommunicationClosedError() from e
            except ConnectionClosedOK:
                self.stop()
                break

            try:
                command: MicrobitCommand = MicrobitCommandAdapter.validate_json(
                    response
                )  # type: ignore
            except ValidationError:
                logger.warning(f"Received invalid command: {response!r}")
                continue

            for listener in self.__listeners:
                listener(command)

    @override
    def stop(self) -> None:
        self.__is_listening = False

    @override
    def close(self, code: ExitStatus = ExitStatus.SUCCESS, reason: str = "") -> None:
        self.__websocket.close(1000 if code is ExitStatus.SUCCESS else 1011, reason)
        self.__websocket.close_socket()
