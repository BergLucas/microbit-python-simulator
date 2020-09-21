import socket, json, time
from .Order import Order
from .Connection import Connection
from .AddressesLinker import Address
from typing import Union
from threading import Lock
class SynchronisationClient:
    def __init__(self, debug=False):
        """ Client that can requests data from a validation server

        Parameters:
        -----------
        debug : Debug mode if True (optional - default: False) (bool)
        """
        self.__debug = debug
        self.__data_lock = Lock()
        self.__data_addr = None
        self.__data_connection: Connection = None

    @property
    def connected(self):
        self.__data_lock.acquire()
        connected = self.__data_connection is not None and self.__data_connection.alive
        self.__data_lock.release()
        return connected

    def connect(self, addr: Address):
        """ Connect the client to a validation server
        
        Parameters:
        -----------
        addr : The address of the validation server (Tuple[str, int])

        Raises:
        -------
        ConnectionError if the connection fails TypeError if a parameter have an invalid type ValueError if a parameter have an invalid value
        """
        self.disconnect()
        self.__data_connection = Connection.try_connection(addr)
    
    def disconnect(self):
        """ Disconnect the client """
        if self.connected:
            self.__data_lock.acquire()
            self.__data_connection.close()
            self.__data_addr = None
            self.__data_connection = None
            self.__data_lock.release()

    def linkPort(self, value: str, port: int):
        """ Send to the server an order to link the port with the value

        Parameters:
        -----------
        value : The value which is requested (str)
        port : The port which need to be added (int) 

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        order = Order()
        order.link(value, port)
        self.sendOrder(order)
    
    def unlinkPort(self, port: int):
        """ Send to the server an order to unlink the port
        
        Parameters:
        -----------
        port : The port which need to be removed (int) 

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        order = Order()
        order.unlink(port)
        self.sendOrder(order)
    
    def getAddresses(self, value:str) -> list:
        """ Send to the server an order to get the addresses linked to the value
        
        Parameters:
        -----------
        value : The value which is requested (str)

        Returns:
        --------
        addresses : The list of addresses from the server (list)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        order = Order()
        order.get(value)
        data = self.sendOrder(order, True)
        if value in data:
            return data[value]
        else:
            return []

    def sendOrder(self, order: Order, retrieve: bool = False) -> any:
        """ Send order to the server

        Parameters:
        -----------
        order : The order which is going to be sent to the server (Order)
        retrieve : True if the server should send something to the client (optional - default: False) (bool)

        Returns:
        --------
        data : The data from the server if retrieve (any)

        Raises:
        -------
        ConnectionAbordedError if connection is lost
        """
        # Send the order
        if self.__debug:
            print(f'SynchronisationClient : Trying to ask order to the SynchronisationServer')
        self.__data_lock.acquire()
        try:
            self.__data_connection.send(order.toJSON())
            if self.__debug:
                print(f'SynchronisationClient : Asked order {order.orderDict} to the SynchronisationServer')
        except:
            if self.__debug:
                print(f'SynchronisationClient : Connection lost with the SynchronisationServer')
            self.__data_addr = None
            self.__data_connection = None
        self.__data_lock.release()
        # Retrieve when get
        if retrieve and self.connected:
            if self.__debug:
                print(f'SynchronisationClient : Trying to get data from the SynchronisationServer')
            self.__data_lock.acquire()
            try:
                data = self.__data_connection.recv()
            except:
                if self.__debug:
                    print(f'SynchronisationClient : Connection lost with the SynchronisationServer')
                self.__data_addr = None
                self.__data_connection = None
            self.__data_lock.release()
            if self.__debug:
                print(f'SynchronisationClient : Got data {data} from the SynchronisationServer')
            try:
                return json.loads(data)
            except:
                if self.__debug:
                    print('SynchronisationClient : Could not read the data from the SynchronisationServer')
                return None