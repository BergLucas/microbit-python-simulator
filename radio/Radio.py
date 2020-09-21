from .SynchronisationClient import SynchronisationClient
from .SynchronisationServer import SynchronisationServer
from .Connection import Connection
from .ConnectionServer import ConnectionServer
from .AddressesLinker import Address, AddressesLinker, checkAddress
from typing import Dict, Tuple, Union, List
from queue import Queue
from threading import Thread, Lock
from time import sleep, time
import socket, json

RATE_250KBIT = 250
RATE_1MBIT = 1000
RATE_2MBIT = 2000

class Radio:
    def __init__(self, synchronisation_address: Address, data_address: Address, bluetooth_port: int, *, ip: str = None, target_ips: List[str] = None, interval: float = 0, timeout: int = None, debug: bool = False):
        """ Create a radio
        
        Parameters:
        -----------
        synchronisation_address: The address used for sync connection (Tuple[str, int])

        data_address : The address used for data connection (Tuple[str, int])

        bluetooth_port : The port used which listen for incoming connection (int)

        ip : The local ip of the server (optional - default: None) (str)

        targets_ips : The ips which are going to be check for synchronisation (List[str])

        interval : The interval beetween each check (float)

        timeout : The number of seconds before a connection timeout (int)

        debug : Print debug info if True (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if interval is not positive
        """
        # Check types
        checkAddress(synchronisation_address)
        checkAddress(data_address)
        if not isinstance(bluetooth_port, int):
            raise TypeError(f'invalid type : {type(bluetooth_port)} is not a int')
        if not isinstance(ip, (str, type(None))):
            raise TypeError(f'invalid type : {type(ip)} is not a str')
        if not isinstance(target_ips, (list, type(None))):
            raise TypeError(f'invalid type : {type(target_ips)} is not a list')
        if target_ips is not None:
            for target_ip in target_ips:
                if not isinstance(target_ip, str):
                    raise TypeError(f'invalid type : {type(target_ip)} is not a str')
        if not isinstance(interval, (int, float)):
            raise TypeError(f'invalid type : {type(interval)} is not a float')
        if not isinstance(timeout, (int, type(None))):
            raise TypeError(f'invalid type : {type(interval)} is not a int')
        if not isinstance(debug, bool):
            raise TypeError(f'invalid type : {type(debug)} is not a bool')
        self.__synchronisation_address = synchronisation_address
        self.__data_address = data_address
        self.__bluetooth_port = bluetooth_port
        self.__ip = ip
        self.__target_ips = target_ips
        self.__interval = interval
        self.__timeout = timeout
        self.__debug = debug
        # Check values
        if interval < 0:
            raise ValueError(f'invalid value : interval must be positive')
        self.__ips = socket.gethostbyname_ex(socket.gethostname())[-1] + ['localhost', '127.0.0.1']
        self.__sync_client = SynchronisationClient(self.__debug)
        # Create and start a validation server if not already open
        if not Connection.isPortOpen(self.__synchronisation_address):
            SynchronisationServer(self.__synchronisation_address[1], self.__data_address[1], ip=self.__ip, target_ips=self.__target_ips, interval=self.__interval, debug=self.__debug).start()
        # Init the attributes
        self.__on = False
        self.__group = 'channel1group1'
        # The queue of the radio
        self.__data_queue = Queue()
        self.__data_lock = Lock()
        # The address from the synchronisation server
        self.__addr = []
        self.__addr_lock = Lock()
        # The connected address {addr:connection}
        self.__connected_clients: Dict[Address, Connection] = {}
        self.__connected_lock = Lock()
        self.config()

    def on(self):
        """ Enable the radio """
        if self.__on:
            return
        self.__on = True
        self.__start_time = time()
        # Getting a port
        count = 0
        while True:
            self.__port = self.__bluetooth_port + count
            try:
                self.__receive_server = ConnectionServer(self.__port, '', self.__timeout)
                break
            except:
                count += 1
        self.__sync_client.connect(self.__data_address)
        self.__sync_client.linkPort(self.__group, self.__port)
        Thread(target=self.__synchroniseAddresses, daemon=True).start()
        Thread(target=self.__acceptClientConnection, daemon=True).start()

    def off(self):
        """ Disable the radio """
        if not self.__on:
            return
        self.__sync_client.unlinkPort(self.__port)
        self.__sync_client.disconnect()
        self.__on = False
        self.__receive_server.close()

    def config(self, **kwargs):
        """ Configure the radio

        Parameters:
        -----------
        length : The max length of a message in bytes (optional - default: 32) (int)

        queue_size : The queue size (optional - default: 3) (int)

        channel : The channel number (optional - default: 7) (int)

        power : The signal strength (optional - default: 6) (int)

        address : The address (optional - default: 0x75626974) (bytes)

        group : The group number (optional - default: 0) (int)

        data_rate : The data rate (optional  - default: RATE_1MBIT)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if a parameter has an invalid value
        """
        # Length
        if 'length' in kwargs:
            if not isinstance(kwargs['length'], int):
                raise TypeError(f'invalid type : {type(kwargs["length"])} is not int')
            if kwargs['length'] < 1 or 251 < kwargs['length']:
                raise ValueError(f'invalid value : {kwargs["length"]} must be between 1 and 251')
            self._length = kwargs['length']
        else:
            self.__length = 32
        # Queue
        if 'queue' in kwargs:
            if not isinstance(kwargs['queue'], int):
                raise TypeError(f'invalid type : {type(kwargs["queue"])} is not int')
            if kwargs['queue'] < 1:
                raise ValueError(f'invalid value : {kwargs["queue"]} must be greater than 1')
            self._queue_size = kwargs['queue']
        else:
            self.__queue_size = 3
        # Channel
        if 'channel' in kwargs:
            if not isinstance(kwargs['channel'], int):
                raise TypeError(f'invalid type : {type(kwargs["channel"])} is not int')
            if kwargs['channel'] < 0 or 83 < kwargs['channel']:
                raise ValueError(f'invalid value : {kwargs["channel"]} must be between 0 and 83')
            self.__channel = kwargs['channel']
        else:
            self.__channel = 7
        # Power
        if 'power' in kwargs:
            if not isinstance(kwargs['power'], int):
                raise TypeError(f'invalid type : {type(kwargs["power"])} is not int')
            if kwargs['power'] < 0 or 7 < kwargs['power']:
                raise ValueError(f'invalid value : {kwargs["power"]} must be between 0 and 7')
            self.__power = kwargs['power']
        else:
            self.__power = 6
        # Address
        if 'address' in kwargs:
            if not isinstance(kwargs['address'], int):
                raise TypeError(f'invalid type : {type(kwargs["address"])} is not int')
            if kwargs['address'] < 0 or 2147483647 < kwargs['address']:
                raise ValueError(f'invalid value : {kwargs["address"]} is must be between 0 and 2147483647')
            self.__address = kwargs['address']
        else:
            self.__address = 0x75626974
        # Group
        if 'group' in kwargs:
            if not isinstance(kwargs['group'], int):
                raise TypeError(f'invalid type : {type(kwargs["group"])} is not int')
            if kwargs['group'] < 0 or 255 < kwargs['group']:
                raise ValueError(f'invalid value : {kwargs["group"]} is must be between 0 and 255')
            self.__group = kwargs['group']
        else:
            self.__group = 0
        # Data rate
        if 'data_rate' in kwargs:
            if kwargs['data_rate'] not in (RATE_250KBIT, RATE_1MBIT, RATE_2MBIT):
                raise ValueError(f'invalid value : {kwargs["data_rate"]} is must be either RATE_250KBIT, RATE_1MBIT or RATE_2MBIT')
            self.__data_rate = kwargs['data_rate']
        else:
            self.__data_rate = RATE_1MBIT
        # Change the queue size
        self.__data_lock.acquire()
        self.__data_queue = Queue(self.__queue_size)
        self.__data_lock.release()
        if self.__on:
            self.__sync_client.unlinkPort(self.__port)
        self.__group = f'channel{self.__channel}group{self.__group}'
        if self.__on:
            self.__sync_client.linkPort(self.__group, self.__port)

    def reset(self):
        """ Reset the radio to its default values """
        config()

    def send_bytes(self, message: bytes):
        """ Send a message in bytes 
        
        Parameters:
        -----------
        message : The message to be sent (bytes)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the length in bytes is greater than the specified in config()
        """
        if not self.__on:
            return
        if not isinstance(message, (bytes, bytearray)):
            raise TypeError(f'invalid type : {type(message)} is not bytes')
        if len(message) > self.__length:
            raise ValueError('The message has a length greater than the specified in config()')
        # Send the message
        self.__connected_lock.acquire()
        for addr in dict(self.__connected_clients):
            try:
                self.__connected_clients[addr].send(message)
            except:
                if self.__debug:
                    print(f'Radio : Connection lost with Radio at {addr}')
                self.__connected_clients.pop(addr)
        self.__connected_lock.release()

    def send(self, message: str):
        """ Send a message
        
        Parameters:
        -----------
        message : The message to be sent (str)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the length in bytes is greater than the specified in config()
        """
        if not self.__on:
            return
        if not isinstance(message, str):
            raise TypeError(f'invalid type : {type(message)} is not str')
        self.send_bytes(bytes(message, 'utf8'))

    def receive_bytes(self) -> Union[bytes, None]:
        """ Receive a message in bytes

        Returns
        -------
        message : The message received in bytes or None if no message (Union[bytes, None])
        """
        if not self.__on:
            return
        self.__data_lock.acquire()
        if self.__data_queue.empty():
            data = None
        else:
            data = self.__data_queue.get()
        self.__data_lock.release()
        return data

    def receive_bytes_into(self, buffer):
        """ Doesnt work yet """
        if not self.__on:
            return

    def receive(self) -> Union[str, None]:
        """ Receive a message

        Returns
        -------
        message : The message received or None if no message (Union[str, None])

        Raises:
        -------
        ValueError if the convertion from bytes to string fails
        """
        if not self.__on:
            return
        message = self.receive_bytes()
        try:
            return None if message == None else str(message, 'utf8')
        except:
            raise ValueError('Convertion from bytes to string failed')

    def receive_full(self) -> Tuple[Union[bytes, None], int, int]:
        """ Receive a full message

        Returns
        -------
        message : The message received or None if no message (Union[bytes, None])

        rssi : The signal stength (int)

        timestamp : The number of microseconds since the radio is on (int)
        """
        if not self.__on:
            return
        return (self.receive_bytes(), self.__power, int((time() - self.__start_time)*1000000))

    def __acceptClientConnection(self):
        """ Accept a client connection """
        while self.__on:
            try:
                if self.__debug:
                    print('Radio : Waiting for a Radio connection')
                connection, addr = self.__receive_server.accept()
                Thread(target=self.__receiveData, args=(connection,), daemon=True).start()
            except Exception as e:
                if self.__debug:
                    print(f'Radio : __acceptClientConnection - {e}')

    def __receiveData(self, connection: Connection):
        """ Receive data from a connection and put it in the data queue
        
        Parameters:
        -----------
        connection : The connection (Connection)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(connection, Connection):
            raise TypeError(f'invalid type : {type(connection)} is not a Connection')
        while connection.alive:
            if self.__on:
                try:
                    data = connection.recv()
                    if self.__debug:
                        print(f'Radio : Received {data} from the Radio')
                    self.__data_lock.acquire()
                    if not self.__data_queue.full():
                        self.__data_queue.put(data)
                    self.__data_lock.release()
                except:
                    if self.__debug:
                        print('Radio : Connection lost with the Radio')
            else:
                connection.close()

    def __refresh_connected_clients(self):
        """ Try to connect to the address given by SynchronisationServer """
        self.__addr_lock.acquire()
        self.__connected_lock.acquire()
        for addr in list(self.__addr):
            # Check if already connected to the address
            if addr not in self.__connected_clients and not (addr[0] in self.__ips and addr[1] == self.__port):
                connection = Connection.create_connection(addr, self.__timeout)
                # Try to connect to the address
                if connection is not None:
                    self.__connected_clients[addr] = connection
                else:
                    self.__addr.remove(addr)
        self.__addr_lock.release()
        self.__connected_lock.release()

    def __synchroniseAddresses(self):
        """ Synchronise the self.__ips with the SynchronisationServer until the connection is lost if the synchronisation doesn't already exists """
        if self.__debug:
            print('Radio : Try to Synchronise address with the SynchronisationServer')
        while self.__on:
            # Connect to the server if not connected
            if not self.__sync_client.connected:
                try:
                    self.__sync_client.connect(self.__data_address)
                    if self.__debug:
                        print(f'Radio : Connected to the SynchronisationServer at {self.__data_address}')
                except:
                    if self.__debug:
                        print('Radio : Could not connect to the SynchronisationServer')
                    sleep(self.__interval)
            # Synchronise until the connection is lost
            while self.__sync_client.connected:
                # Stop the sync if the radio is off
                if self.__on:
                    # Try to sync the ips with the server
                    try:
                        addresses = self.__sync_client.getAddresses(self.__group)
                    except:
                        if self.__debug:
                            print('Radio : Connection lost with the SynchronisationServer')
                        break
                    # Try to read the data from the server
                    try:
                        self.__addr_lock.acquire()
                        self.__addr = []
                        for addr in addresses:
                            self.__addr.append(tuple(addr))
                        self.__addr_lock.release()
                        self.__refresh_connected_clients()
                        sleep(self.__interval)
                    except Exception as e:
                        if self.__debug:
                            print(f'Radio : Could not read the data from the SynchronisationServer {e}')
                # Disconnect if the radio is off
                else:
                    self.__sync_client.disconnect()
                    if self.__debug:
                        print(f'Radio : Disconnected from the SynchronisationServer at {self.__data_address}')