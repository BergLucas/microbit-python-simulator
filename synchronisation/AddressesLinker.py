from threading import Lock
from copy import deepcopy
from typing import Dict, List, Tuple, Union
import json
Address = Tuple[str, int]

def checkAddress(address: Address):
    """ Check if the address is valid.

    Parameters:
    -----------
    address: The address (ip, port) (Tuple[str, int])

    Raises:
    -------
    TypeError: if the address is invalid.
    """
    # Check the address
    if not isinstance(address, (list, tuple)) or len(address) != 2:
        raise TypeError('The address must be a tuple of length 2')
    ip, port = address
    if not isinstance(ip, str):
        raise TypeError('The ip must be a str')
    if not isinstance(port, int):
        raise TypeError('The port must be a int')

class AddressesLinker:
    def __init__(self):
        """ A class that link addresses (ip, port) to values. This class is thread-safe """
        self.__addresses = {}
        self.__addresses_lock = Lock()
    
    @property
    def addresses(self):
        self.__addresses_lock.acquire()
        addresses = deepcopy(self.__addresses)
        self.__addresses_lock.release()
        return addresses

    def linkAddress(self, address: Address, value: str) -> None:
        """ Link the address with a value. This method is thread-safe.

        Parameters:
        -----------
        address: The address (ip, port) which is going to be linked (Tuple[str, int])
        
        value: The value which is going to be linked. (str)

        Raises:
        -------
        TypeError: if a parameter has an invalid type.
        """
        # Check the parameters
        checkAddress(address)
        if not isinstance(value, str):
            raise TypeError(f'invalid type : {type(value)} is not str')
        # Link the address to the value
        self.__addresses_lock.acquire()
        self.__addresses[address] = value
        self.__addresses_lock.release()
    
    def unlinkAddress(self, address: Address) -> None:
        """ Unlink the address. This method is thread-safe.

        Parameters:
        -----------
        address: The address (ip, port) which is going to be unlinked (Tuple[str, int])

        Raises:
        -------
        TypeError: if the address is invalid.
        """
        # Check the address
        checkAddress(address)

        # Unlink the address
        self.__addresses_lock.acquire()
        self.__addresses.pop(address)
        self.__addresses_lock.release()

    def mergeAddressesLinker(self, addressesLinker) -> None:
        """ Merge the new AddressesLinker with the current AddressesLinker. This method is thread-safe.

        Parameters:
        -----------
        addressesLinker: The AddressesLinker which is going to be merged. (AddressesLinker)

        Raises:
        -------
        TypeError: if a parameter is invalid.
        """
        # Check if addresses is a dict
        if not isinstance(addressesLinker, AddressesLinker):
            raise TypeError(f'invalid type : {type(addressesLinker)} is not an AddressesLinker')
        
        # Merge the addresses
        self.__addresses_lock.acquire()
        self.__addresses.update(addressesLinker.addresses)
        self.__addresses_lock.release()

    def getAddresses(self, addresses: Union[Tuple[Address], List[Address]]) -> Dict[str, List[Address]]:
        """ Get the values which are linked to the addresses. This method is thread-safe.

        Parameters:
        -----------
        addresses: The addresses that are requested. (Union[Tuple[Tuple[str, int]], List[Tuple[str, int]]])

        Returns:
        --------
        linked_addresses: The requested linked addresses. (Dict[str, List[Address]])

        Raises:
        -------
        TypeError: if addresses has an invalid type
        """
        # Check if the addresses has a valid type
        if not isinstance(addresses, (tuple, list)):
            raise TypeError('addresses must be a tuple or a list')
        # Get the linked addresses
        linked_addresses = {}
        self.__addresses_lock.acquire()
        for address in addresses:
            # Check if address exists
            if address in self.__addresses:
                value = self.__addresses[address]
                if value not in linked_addresses:
                    linked_addresses[value] = []
                linked_addresses[value].append(address)
        self.__addresses_lock.release()
        return linked_addresses

    def existsAddresses(self, addresses: Union[Tuple[Address], List[Address]]) -> bool:
        """ Check if the addresses exists. This method is thread-safe.

        Parameters:
        -----------
        addresses: The addresses that need to be checked. (Union[Tuple[Tuple[str, int]], List[Tuple[str, int]]])

        Returns:
        --------
        exists: True if every address in the list/tuple exists, otherwise False
        """
        exists = True
        self.__addresses_lock.acquire()
        for address in addresses:
            if address not in self.__addresses:
                exists = False
        self.__addresses_lock.release()
        return exists

    def getValues(self, values: Union[Tuple[str], List[str]]) -> Dict[str, List[Address]]:
        """ Get the addresses which are linked with requested values. This method is thread-safe.

        Parameters:
        -----------
        values: The values that are requested. (Union[Tuple[str], List[str]])

        Returns:
        --------
        linked_addresses: The requested linked addresses. (Dict[str, List[Address]])

        Raises:
        -------
        TypeError: if a parameter has an invalid type.
        """
        # Check if the values has a valid type
        if not isinstance(values, (tuple, list)):
            raise TypeError('values must be a tuple or a list')
        for value in values:
            if not isinstance(value, str):
                raise TypeError(f'invalid type : {type(value)} is not str')
        # Get the linked addresses
        linked_addresses = {}
        self.__addresses_lock.acquire()
        for value in values:
            linked_addresses[value] = []
        for address in self.__addresses:
            # Check if address is linked with one of the values
            if self.__addresses[address] in values:
                linked_addresses[self.__addresses[address]].append(address)
        self.__addresses_lock.release()
        return linked_addresses

    def existsValues(self, values: Union[Tuple[str], List[str]]) -> bool:
        """ Check if the values exists. This method is thread-safe.

        Parameters:
        -----------
        values: The values that need to be checked. (Union[Tuple[str], List[str]])

        Returns:
        --------
        exists: True if every value in the list/tuple exists, otherwise False
        """
        self.__addresses_lock.acquire()
        for value in values:
            # Check if the value exists
            exists = False
            for address in self.__addresses:
                if self.__addresses[address] == value:
                    exists = True
            # Return False if it does not exist
            if not exists:
                self.__addresses_lock.release()
                return False
        self.__addresses_lock.release()
        return True

    def toJSON(self) -> bytes:
        """ Serialize the addressesLinker

        Returns:
        --------
        serialised_adressesLinker : The serialised adresseslinker (bytes)
        """
        # Prepare the addresses
        values_dict = {}
        self.__addresses_lock.acquire()
        for addr in self.__addresses:
            value = self.__addresses[addr]
            if value not in values_dict:
                values_dict[value] = []
            values_dict[value].append(addr)
        self.__addresses_lock.release()
        # Encode and convert the preparation addresses
        return json.dumps(values_dict).encode()

    @staticmethod
    def fromJSON(serialised_adresseslinker: bytes):
        """ Deserialize the addressesLinker
        
        Parameters:
        -----------
        serialised_adressesLinker : The serialised adresseslinker (bytes)
        
        Returns:
        --------
        adressesLinker : The addressesLinker (AdressesLinker)

        Raises:
        -------
        TypeError : if encoded_addresses is not bytes
        ValueError : if encoded_addresses is invalid
        """
        # Check the encoded addresses
        if not isinstance(serialised_adresseslinker, bytes):
            raise TypeError(f'invalid type : {type(serialised_adresseslinker)} is not bytes')
        try:
            values_dict: Dict[str, Tuple[str, int]] = json.loads(serialised_adresseslinker)
            addressesLinker = AddressesLinker()
            for value in values_dict:
                for addr in values_dict[value]:
                    addressesLinker.linkAddress(tuple(addr), value)
            return addressesLinker
        except Exception as e:
            print(e)
            raise ValueError(f'invalid value : serialised_adresseslinker has an invalid value')