import json
from threading import Thread

from .AddressesLinker import Address, AddressesLinker, checkAddress
from .Connection import Connection
from .ConnectionServer import ConnectionServer
from .Order import Order


class SynchronisationServer:
    def __init__(self, synchronisation_port: int, debug: bool = False):
        """Create a Synchronisation server.

        Parameters:
        -----------
        synchronisation_port: The port which will be used for sync connection (int)

        debug : Print debug info if True (optional - default: True) (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        # Check types
        if not isinstance(synchronisation_port, int):
            raise TypeError(f"invalid type : {type(synchronisation_port)} is not a int")
        if not isinstance(debug, bool):
            raise TypeError(f"invalid type : {type(debug)} is not a bool")
        # Init
        self.__on = False
        self.__debug = debug
        self.__synchronisation_port = synchronisation_port
        self.__addressesLinker = AddressesLinker()

    def start(self):
        """Start the synchronisation and the data transfert.

        Raises:
        -------
        Exception if the synchronisation port or the data port are already in use
        """
        if self.__on:
            return
        self.__on = True
        self.__sync_server = ConnectionServer(self.__synchronisation_port)
        Thread(target=self.__acceptSyncConnection, daemon=True).start()

    def stop(self):
        """Stop the synchronisation and the data transfert."""
        if not self.__on:
            return
        self.__on = False
        self.__sync_server.close()

    def isRunning(self) -> bool:
        """Check if the server is running.

        Returns:
        --------
        running : True if the server is running (bool)
        """
        return self.__on

    def __acceptSyncConnection(self):
        """Accept sync connections while the server is running."""
        while self.isRunning():
            try:
                if self.__debug:
                    print(
                        "SynchronisationServer : Waiting for a SynchronisationClient connection"
                    )
                connection, addr = self.__sync_server.accept()
                if self.__debug:
                    print(
                        f"SynchronisationServer : Connected to the SynchronisationClient at {addr}"
                    )
                Thread(
                    target=self.__modifyLinker,
                    args=(
                        addr,
                        connection,
                    ),
                    daemon=True,
                ).start()
            except Exception as e:
                if self.__debug:
                    print(f"SynchronisationServer : __acceptSyncConnection - {e}")

    def __modifyLinker(self, addr: Address, connection: Connection):
        """Receive order from a SynchronisationClient until the connection is lost.

        Parameters:
        -----------
        addr : The address of the server (Tuple[str, int])

        connection : The connection with the address (Connection)

        Raises:
        -------
        TypeError: if a parameter has an invalid type.
        """
        if not isinstance(connection, Connection):
            raise TypeError(f"invalid type - {type(connection)} is not Connection")
        checkAddress(addr)
        link = None
        while connection.alive:
            if self.isRunning():
                # Wait for an order
                try:
                    encoded_order = connection.recv()
                except:
                    if link is not None:
                        self.__addressesLinker.unlinkAddress(link)
                    if self.__debug:
                        print(
                            f"SynchronisationServer : Disconnected from SynchronisationClient at {addr}"
                        )
                    break
                # Try to read the order
                try:
                    order = Order.fromJSON(encoded_order)
                    if self.__debug:
                        print(
                            f"SynchronisationServer : Got order {order.orderDict} from the SynchronisationClient"
                        )
                    # Execute the order
                    if "link" in order.orderDict:
                        [value, port] = order.orderDict["link"]
                        if link is not None:
                            self.__addressesLinker.unlinkAddress(link)
                        else:
                            link = (addr[0], port)
                        self.__addressesLinker.linkAddress(link, value)

                    if "unlink" in order.orderDict:
                        if link is not None and link == (
                            addr[0],
                            order.orderDict["unlink"],
                        ):
                            self.__addressesLinker.unlinkAddress(link)
                            link = None
                    if "get" in order.orderDict:
                        data = self.__addressesLinker.getValues(
                            [order.orderDict["get"]]
                        )
                        connection.send(json.dumps(data).encode())
                except Exception as e:
                    if self.__debug:
                        print(
                            f"SynchronisationServer : Could not read the order from the SynchronisationClient {e}"
                        )
            else:
                connection.close()
