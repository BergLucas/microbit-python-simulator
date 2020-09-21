from .AddressesLinker import AddressesLinker, Address, checkAddress
from .ConnectionServer import ConnectionServer
from .Connection import Connection
from .Order import Order
from typing import Dict, List, Tuple, Union
from threading import Lock, Thread
from time import sleep
import socket, json
class SynchronisationServer:
    def __init__(self, synchronisation_port: int, data_port: int, *, ip: str = None, target_ips: List[str] = None, interval: float = 0, debug: bool = False):
        """ Create a Synchronisation server 
        
        Parameters:
        -----------
        synchronisation_port: The port which will be used for sync connection (int)

        data_port : The port which will be used for data connection (int)

        ip : The local ip of the server (optional - default: None) (str)

        targets_ips : The ips which are going to be check for synchronisation (List[str])

        interval : The interval beetween each check (float)

        debug : Print debug info if True (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if interval is not positive
        """
        # Check types
        if not isinstance(synchronisation_port, int):
            raise TypeError(f'invalid type : {type(synchronisation_port)} is not a int')
        if not isinstance(data_port, int):
            raise TypeError(f'invalid type : {type(data_port)} is not a int')
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
        if not isinstance(debug, bool):
            raise TypeError(f'invalid type : {type(debug)} is not a bool')
        # Check values
        if interval < 0:
            raise ValueError(f'invalid value : interval must be positive')
        # Get or guess the ips and ip
        if ip != None and ip not in ['localhost', '127.0.0.1']:
            self.__ips = [ip]
        else:
            self.__ips = socket.gethostbyname_ex(socket.gethostname())[-1]
        # Get or create the target ips
        if target_ips == None:
            self.__target_ips = []
            for ip in self.__ips:
                # Split the ips
                ip_parts = ip.split('.')
                if len(ip_parts) >= 3:
                    for i in range(1, 255):
                        self.__target_ips.append(f'{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{i}')
        else:
            self.__target_ips = target_ips
        # Init
        self.__ips += ['localhost', '127.0.0.1']
        self.__on = False
        self.__debug = debug
        self.__interval = interval
        self.__synchronisation_port = synchronisation_port
        self.__data_port = data_port
        self.__addressesLinker = AddressesLinker()
        self.__connected_servers: List[Address] = []
        self.__connected_servers_lock = Lock()

    def start(self):
        """ Start the synchronisation and the data transfert
        
        Raises:
        -------
        Exception if the synchronisation port or the data port are already in use
        """
        if self.__on:
            return
        self.__on = True
        self.__sync_server = ConnectionServer(self.__synchronisation_port)
        self.__data_server = ConnectionServer(self.__data_port)
        # Create acceptation task
        Thread(target=self.__acceptSyncConnection, daemon=True).start()
        Thread(target=self.__acceptDataConnection, daemon=True).start()
        # Create connection task
        for ip in self.__target_ips:
            if ip not in self.__ips:
                Thread(target=self.__connectToSyncServer, args=((ip, self.__synchronisation_port),), daemon=True).start()

    def stop(self):
        """ Stop the synchronisation and the data transfert """
        if not self.__on:
            return
        self.__on = False
        self.__sync_server.close()
                
    def isRunning(self) -> bool:
        """ Check if the server is running

        Returns:
        --------
        running : True if the server is running (bool)
        """
        return self.__on

    def __acceptSyncConnection(self):
        """ Accept synchronisation connections while the server is running. """
        while self.isRunning():
            try:
                if self.__debug:
                    print('SynchronisationServer : Waiting for a SynchronisationServer connection')
                connection, addr = self.__sync_server.accept()
                addr = (addr[0], self.__synchronisation_port)
                if self.__debug:
                    print(f'SynchronisationServer : Connected to the SynchronisationServer at {addr}')
                Thread(target=self.__synchroniseLinker, args=(addr, connection,), daemon=True).start()
            except Exception as e:
                if self.__debug:
                    print(f'SynchronisationServer : __acceptSyncConnection - {e}')

    def __acceptDataConnection(self):
        """ Accept data connections while the server is running. """
        while self.isRunning():
            try:
                if self.__debug:
                    print('SynchronisationServer : Waiting for a SynchronisationClient connection')
                connection, addr = self.__data_server.accept()
                if self.__debug:
                    print(f'SynchronisationServer : Connected to the SynchronisationClient at {addr}')
                Thread(target=self.__modifyLinker, args=(addr, connection,), daemon=True).start()
            except Exception as e:
                if self.__debug:
                    print(f'SynchronisationServer : __acceptDataConnection - {e}')

    def __connectToSyncServer(self, addr: Address):
        """ Try to connect to the synchronisation server if not already in synchronisation
        
        Parameters:
        -----------
        addr : The address of the server (Tuple[str, int])

        Raises:
        -------
        TypeError: if a parameter has an invalid type.
        """
        checkAddress(addr)
        while self.isRunning():
            # Ping until connected
            self.__connected_servers_lock.acquire()
            inSync = addr in self.__connected_servers
            self.__connected_servers_lock.release()
            connected = False
            while not connected and not inSync:
                # Try to connect
                connection = Connection.create_connection(addr)
                # Sleep if not connected
                if connection is None:
                    # Break the loop if in sync
                    self.__connected_servers_lock.acquire()
                    inSync = addr in self.__connected_servers
                    self.__connected_servers_lock.release()
                    if inSync:
                        break
                    else:
                        sleep(self.__interval)
                else:
                    connected = True
                    if self.__debug:
                        print(f'SynchronisationServer : Connected to SynchronisationServer at {addr}')
            # Synchronise with the server if not inSync
            if inSync:
                sleep(self.__interval)
            else:
                self.__synchroniseLinker(addr, connection)

    def __synchroniseLinker(self, addr: Address, connection: Connection):
        """ Synchronise the AddressesLinker with the address until the connection is lost if the synchronisation doesn't already exists

        Parameters:
        -----------
        addr : The address of the server (Tuple[str, int])

        connection : The connection with the address (Connection)

        Raises:
        -------
        TypeError: if a parameter has an invalid type.
        """
        if not isinstance(connection, Connection):
            raise TypeError(f'invalid type - {type(connection)} is not Connection')
        checkAddress(addr)
        # Add the addr to the connected server
        self.__connected_servers_lock.acquire()
        if addr not in self.__connected_servers:
            self.__connected_servers.append(addr)
        else:
            connection.close()
        self.__connected_servers_lock.release()
        # Synchronise the AddressesLinker with the address if the connection is alive and the server is running
        while connection.alive:
            if self.isRunning():
                try:
                    connection.send(self.__addressesLinker.toJSON())
                    syncLinker = AddressesLinker.fromJSON(connection.recv())
                    self.__addressesLinker.mergeAddressesLinker(syncLinker)
                    sleep(self.__interval)
                except:
                    connection.close()
                    if self.__debug:
                        print(f'SynchronisationServer : Disconnected from SynchronisationServer at {addr}')
            else:
                connection.close()
        # Remove the addr to the connected server if present
        self.__connected_servers_lock.acquire()
        if addr in self.__connected_servers:
            self.__connected_servers.remove(addr)
        self.__connected_servers_lock.release()

    def __modifyLinker(self, addr: Address, connection: Connection):
        """ Receive order from a SynchronisationClient until the connection is lost

        Parameters:
        -----------
        addr : The address of the server (Tuple[str, int])
        
        connection : The connection with the address (Connection)

        Raises:
        -------
        TypeError: if a parameter has an invalid type.
        """
        if not isinstance(connection, Connection):
            raise TypeError(f'invalid type - {type(connection)} is not Connection')
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
                        print(f'SynchronisationServer : Disconnected from SynchronisationClient at {addr}')
                    break
                # Try to read the order
                try:
                    order = Order.fromJSON(encoded_order)
                    if self.__debug:
                        print(f'SynchronisationServer : Got order {order.orderDict} from the SynchronisationClient')
                    # Execute the order
                    if 'link' in order.orderDict:
                        [value, port] = order.orderDict['link']
                        if link is not None:
                            self.__addressesLinker.unlinkAddress(link)
                        else:
                            link = (addr[0], port)
                        self.__addressesLinker.linkAddress(link, value)
                        
                    if 'unlink' in order.orderDict:
                        if link is not None and link == (addr[0], order.orderDict['unlink']):
                            self.__addressesLinker.unlinkAddress(link)
                            link = None
                    if 'get' in order.orderDict:
                        data = self.__addressesLinker.getValues([order.orderDict['get']])
                        connection.send(json.dumps(data).encode())
                except Exception as e:
                    if self.__debug:
                        print(f'SynchronisationServer : Could not read the order from the SynchronisationClient {e}')
            else:
                connection.close()