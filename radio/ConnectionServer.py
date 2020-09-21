import socket, struct
from .Connection import Connection
from typing import Union, Tuple
class ConnectionServer:
    def __init__(self, port: int, ip: str = '', timeout: float = None) -> None:
        """ Create a connection server

        Parameters:
        -----------
        port: The addr which listen (int)

        ip : The ip that is going to be accepted (optionnal - default:'') (str)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        
        Exception if the port is already in use
        """
        if not isinstance(port, int):
            raise TypeError(f'invalid type : {type(port)} is not int')
        if not isinstance(ip, str):
            raise TypeError(f'invalid type : {type(ip)} is not str')
        self.__alive = True
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.settimeout(timeout)
        self.__socket.bind((ip, port))
        self.__socket.listen()
    
    @property
    def alive(self):
        return self.__alive

    def accept(self) -> Tuple[Connection, Tuple[str, int]]:
        """ Wait for an incoming connection

        Returns:
        --------
        connection_info : A tuple Connection and addr (Tuple[Connection, Tuple[str, int]])"""
        socket, addr = self.__socket.accept()
        return Connection(socket), addr
    
    def close(self):
        """ Close the connection server"""
        self.__alive = False
        self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()