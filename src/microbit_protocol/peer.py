from __future__ import annotations
from microbit_protocol.exceptions import ConnectionClosed
from microbit_protocol.commands import MicrobitCommandAdapter, MicrobitCommand
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    ConnectionClosed as WebsocketConnectionClosed,
)
from websockets.extensions.permessage_deflate import enable_server_permessage_deflate
from websockets.sync.connection import Connection
from websockets.sync.server import ServerConnection
from websockets.server import ServerProtocol
from websockets.sync.client import connect
from threading import Thread, main_thread
from typing import Callable, Optional, Type
from pydantic import ValidationError
from types import TracebackType
import logging
import socket

logger = logging.getLogger(__name__)


class MicrobitPeer:
    @classmethod
    def connect(cls, host: str, port: int) -> MicrobitPeer:
        websocket = connect(f"ws://{host}:{port}")
        return MicrobitPeer(websocket)

    @classmethod
    def wait_for_connection(cls, host: str, port: int) -> MicrobitPeer:
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

            return MicrobitPeer(connection)

    def __init__(self, websocket: Connection) -> None:
        self.__websocket = websocket
        self.__is_listening = False

        # Temporary fix because websockets create a non-daemon thread
        # that prevents the program from exiting
        # if the socket is not closed properly
        def close_socket_gracefully() -> None:
            main_thread().join()
            self.close(1011)

        Thread(target=close_socket_gracefully).start()

    def send_command(self, command: MicrobitCommand) -> None:
        request = command.model_dump_json()

        try:
            self.__websocket.send(request)
        except WebsocketConnectionClosed as e:
            raise ConnectionClosed() from e

    @property
    def is_listening(self) -> bool:
        return self.__is_listening

    def listen(self, listener: Callable[[MicrobitCommand], None]) -> None:
        self.__is_listening = True

        while self.__is_listening:
            try:
                response = self.__websocket.recv()
            except ConnectionClosedError as e:
                raise ConnectionClosed() from e
            except ConnectionClosedOK:
                self.stop()
                break

            try:
                command = MicrobitCommandAdapter.validate_json(response)
            except ValidationError as e:
                logger.warning(f"Received invalid command: {response}")
                continue

            listener(command)

    def stop(self) -> None:
        self.__is_listening = False

    def close(self, code: int = 1000, reason: str = "") -> None:
        self.__websocket.close(code, reason)
        self.__websocket.close_socket()

    def __enter__(self) -> MicrobitPeer:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close(1000 if exc_type is None else 1011)
