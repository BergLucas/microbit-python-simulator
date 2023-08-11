import socket
import struct
from typing import Tuple

from .AddressesLinker import Address, checkAddress


class Connection:
    def __init__(self, connected_socket: socket.socket) -> None:
        """Hold the connection of a socket.

        Parameters:
        -----------
        connected_socket : The socket (socket.socket)

        Raises:
        -------
        TypeError if connected_socket is not a socket
        """
        if not isinstance(connected_socket, (socket.socket)):
            raise TypeError(f"invalid type : {type(connected_socket)} is not a socket")
        self.__socket = connected_socket
        self.__alive = True

    @property
    def alive(self) -> bool:
        return self.__alive

    def send(self, packet: bytes) -> None:
        """Send a packet of data.

        Parameters:
        -----------
        packet: The packet of bytes to send (bytes)

        Raises:
        -------
        TypeError if packet is not bytes

        ConnectionAbordedError if connection is lost
        """
        if isinstance(packet, (bytes, bytearray)):
            # Prefix with a 4-byte length (network byte order)
            struct_packet = struct.pack(">I", len(packet)) + packet
            try:
                if self.__alive:
                    self.__socket.sendall(struct_packet)
            except:
                self.close()
                raise ConnectionAbortedError("Connection lost")
        else:
            raise TypeError(f"invalid type : {type(packet)} is not bytes")

    def recv(self) -> bytes:
        """Receive a packet of data.

        Returns:
        --------
        packet: The packet (bytes)

        Raises:
        -------
        ConnectionAbordedError if connection is lost

        Notes:
        ------
        A valid packet start with 4 byte which are the length of the packet without these 4 bytes
        """
        if self.__alive:
            # Read packet length
            packet_raw_length = self.__recv_nbytes(4)
            packet_length: int = struct.unpack(">I", packet_raw_length)[0]
            # Return the packet
            return self.__recv_nbytes(packet_length)
        else:
            return b""

    def send_msg(self, message: str) -> None:
        """Send a message.

        Parameters:
        -----------
        message: The message to send (str)

        Raises:
        -------
        TypeError if packet is not str

        ConnectionAbordedError if connection is lost
        """
        if isinstance(message, (str)):
            self.send(message.encode("utf-8"))
        else:
            raise TypeError(f"invalid type : {type(message)} is not str")

    def recv_msg(self) -> str:
        """Receive a message.

        Returns:
        --------
        message: The message (str)

        Raises:
        -------
        ConnectionAbordedError if connection is lost
        """
        return str(self.recv(), "utf-8")

    def close(self) -> None:
        """Close the connection."""
        if self.__alive:
            self.__alive = False
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()

    def __recv_nbytes(self, number: int) -> bytes:
        """Receive nbytes.

        Parameters:
        -----------
        number: The number of bytes to receive (int)

        Returns:
        --------
        nbytes: The requested nbytes(bytes)

        Raises:
        -------
        ConnectionAbordedError if connection is lost
        """
        data = bytearray()
        while len(data) < number:
            # Try to receive data
            try:
                data.extend(self.__socket.recv(number - len(data)))
            except:
                self.close()
                raise ConnectionAbortedError("Connection lost")
        return bytes(data)

    @staticmethod
    def try_connection(addr: Tuple[str, int], timeout: float = None):
        """Try to create a connection to the addr.

        Parameters:
        -----------
        addr: The tuple ip, port (Tuple[str, int])

        timeout: The timeout before the connection fail (optional - default: None) (float)

        Returns:
        --------
        connection : The connection (Connection)

        Raises:
        -------
        ConnectionError if the connection fails

        TypeError if a parameter have an invalid type

        ValueError if a parameter have an invalid value
        """
        checkAddress(addr)
        if not isinstance(timeout, (float, int, type(None))):
            raise TypeError(f"invalid type : {type(timeout)} is not a float")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(timeout)
        if sock.connect_ex(addr) == 0:
            return Connection(sock)
        else:
            raise ConnectionError("could not connect")

    @staticmethod
    def create_connection(addr: Tuple[str, int], timeout: float = None):
        """Try to create a connection to the addr.

        Parameters:
        -----------
        addr: The tuple ip, port (Tuple[str, int])

        timeout: The timeout before the connection fail (optional - default: None) (float)

        Returns:
        --------
        connection : The connection if connected succesfully, None otherwise (Union[Connection, None])

        Raises:
        -------
        TypeError if a parameter have an invalid type

        ValueError if a parameter have an invalid value
        """
        checkAddress(addr)
        if not isinstance(timeout, (float, int, type(None))):
            raise TypeError(f"invalid type : {type(timeout)} is not a float")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(timeout)
        if sock.connect_ex(addr) == 0:
            return Connection(sock)
        else:
            return None

    @staticmethod
    def isPortOpen(addr: Address, timeout: float = None):
        """Check if the port at the address is listening.

        Parameters:
        -----------
        addr: The tuple ip, port (Tuple[str, int])

        timeout: The timeout before the connection fail (optional - default: None) (float)

        Returns:
        --------
        open : True if the server listen, False otherwise (bool)

        Raises:
        -------
        TypeError if a parameter have an invalid type

        ValueError if a parameter have an invalid value
        """
        checkAddress(addr)
        if not isinstance(timeout, (float, int, type(None))):
            raise TypeError(f"invalid type : {type(timeout)} is not a float")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(timeout)
        if sock.connect_ex(addr) == 0:
            sock.close()
            return True
        else:
            return False
