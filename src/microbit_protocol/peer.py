from __future__ import annotations
from microbit_protocol.exceptions import CommunicationClosed
from microbit_protocol.commands import MicrobitCommandAdapter, MicrobitCommand
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    ConnectionClosed,
)
from websockets.extensions.permessage_deflate import enable_server_permessage_deflate
from websockets.sync.connection import Connection
from websockets.sync.server import ServerConnection
from websockets.server import ServerProtocol
from websockets.sync.client import connect
from threading import Thread, main_thread
from typing import Callable, Optional, Type, Protocol, TextIO
from typing_extensions import Self
from pydantic import ValidationError
from types import TracebackType
from enum import Enum, auto
import logging
import socket
import sys

logger = logging.getLogger(__name__)


class ExitStatus(Enum):
    SUCCESS = auto()
    ERROR = auto()


class MicrobitPeer(Protocol):
    def send_command(self, command: MicrobitCommand) -> None:
        ...

    def add_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        ...

    def remove_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        ...

    @property
    def listeners(self) -> set[Callable[[MicrobitCommand], None]]:
        ...

    @property
    def is_listening(self) -> bool:
        ...

    def listen(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def close(self, code: ExitStatus = ExitStatus.SUCCESS, reason: str = "") -> None:
        ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close(ExitStatus.SUCCESS if exc_type is None else ExitStatus.ERROR)


class MicrobitIoPeer(MicrobitPeer):
    def __init__(
        self,
        io_input: TextIO = sys.stdin,
        io_output: TextIO = sys.stdout,
        io_error: TextIO = sys.stderr,
        auto_close_io: bool = False,
    ) -> None:
        self.__io_input = io_input
        self.__io_output = io_output
        self.__io_error = io_error
        self.__auto_close_io = auto_close_io
        self.__listeners: set[Callable[[MicrobitCommand], None]] = set()
        self.__is_listening = False

    def send_command(self, command: MicrobitCommand) -> None:
        request = command.model_dump_json()

        self.__io_output.write(f"{request}\n")
        self.__io_output.flush()

    def add_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.add(listener)

    def remove_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.remove(listener)

    @property
    def listeners(self) -> set[Callable[[MicrobitCommand], None]]:
        return self.__listeners.copy()

    @property
    def is_listening(self) -> bool:
        return self.__is_listening

    def listen(self) -> None:
        self.__is_listening = True

        while self.__is_listening:
            try:
                response = self.__io_input.readline()[:-1]
            except Exception as e:
                raise CommunicationClosed() from e

            try:
                command = MicrobitCommandAdapter.validate_json(response)
            except ValidationError as e:
                logger.warning(f"Received invalid command: {response}")
                continue

            for listener in self.__listeners:
                listener(command)

    def stop(self) -> None:
        self.__is_listening = False

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
    @classmethod
    def connect(cls, host: str, port: int) -> MicrobitWebsocketPeer:
        websocket = connect(f"ws://{host}:{port}")
        return MicrobitWebsocketPeer(websocket)

    @classmethod
    def wait_for_connection(cls, host: str, port: int) -> MicrobitWebsocketPeer:
        extensions = enable_server_permessage_deflate(None)

        server_socket = socket.create_server((host, port))
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

        while True:
            peer_socket, _ = server_socket.accept()

            protocol = ServerProtocol(extensions=extensions)

            connection = ServerConnection(peer_socket, protocol)

            try:
                connection.handshake()
            except Exception:
                peer_socket.close()
                continue

            server_socket.close()

            return MicrobitWebsocketPeer(connection)

    def __init__(self, websocket: Connection) -> None:
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

    def send_command(self, command: MicrobitCommand) -> None:
        request = command.model_dump_json()

        try:
            self.__websocket.send(request)
        except ConnectionClosed as e:
            raise CommunicationClosed() from e

    def add_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.add(listener)

    def remove_listener(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__listeners.remove(listener)

    @property
    def listeners(self) -> set[Callable[[MicrobitCommand], None]]:
        return self.__listeners.copy()

    @property
    def is_listening(self) -> bool:
        return self.__is_listening

    def listen(self) -> None:
        self.__is_listening = True

        while self.__is_listening:
            try:
                response = self.__websocket.recv()
            except ConnectionClosedError as e:
                raise CommunicationClosed() from e
            except ConnectionClosedOK:
                self.stop()
                break

            try:
                command = MicrobitCommandAdapter.validate_json(response)
            except ValidationError as e:
                logger.warning(f"Received invalid command: {response}")
                continue

            for listener in self.__listeners:
                listener(command)

    def stop(self) -> None:
        self.__is_listening = False

    def close(self, code: ExitStatus = ExitStatus.SUCCESS, reason: str = "") -> None:
        self.__websocket.close(1000 if code is ExitStatus.SUCCESS else 1011, reason)
        self.__websocket.close_socket()
