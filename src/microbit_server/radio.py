from functools import partial
from threading import Lock, Thread

from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.exceptions import CommunicationClosedError
from microbit_protocol.peer import MicrobitWebsocketPeer


class RadioServer:
    """A server that connects to multiple radios and broadcasts commands to them."""

    def __init__(self, host: str, port: int) -> None:
        """Initialises `self` to a new RadioServer.

        Args:
            host (str): The host to listen on.
            port (int): The port to listen on.
        """
        self.host = host
        self.port = port
        self.__radios: set[MicrobitWebsocketPeer] = set()
        self.__radios_lock = Lock()

    def start(self) -> None:
        """Starts the server and listens for incoming connections."""
        with MicrobitWebsocketPeer.accept_connections(self.host, self.port) as server:
            for peer in server:
                with self.__radios_lock:
                    self.__radios.add(peer)

                peer.add_listener(partial(self.__broadcast, peer))

                Thread(target=partial(self.__listen, peer), daemon=True).start()

    def __listen(self, peer: MicrobitWebsocketPeer) -> None:
        """Listens for incoming commands from `peer`.

        Args:
            peer (MicrobitWebsocketPeer): The peer to listen to.
        """
        try:
            peer.listen()
        finally:
            with self.__radios_lock:
                self.__radios.remove(peer)

    def __broadcast(
        self, peer: MicrobitWebsocketPeer, command: MicrobitCommand
    ) -> None:
        """Broadcasts `command` to all connected radios except `peer`.

        Args:
            peer (MicrobitWebsocketPeer): The peer to exclude.
            command (MicrobitCommand): The command to broadcast.
        """
        with self.__radios_lock:
            radios = self.__radios.difference({peer})

        for radio in radios:
            try:
                radio.send_command(command)
            except CommunicationClosedError:
                continue
