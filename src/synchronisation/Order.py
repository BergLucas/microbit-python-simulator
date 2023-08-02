import json


class Order:
    def __init__(self):
        """Create an order"""
        self.__order = {}

    @property
    def orderDict(self):
        return self.__order

    def link(self, value: str, port: int):
        """Add an link order

        Parameters:
        -----------
        value : The value which is requested (str)
        port : The port which need to be added (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(value, str):
            raise TypeError(f"invalid type : {type(value)} is not str")
        if not isinstance(port, int):
            raise TypeError(f"invalid type : {type(port)} is not int")
        self.__order = {"link": [value, port]}

    def unlink(self, port: int):
        """Add a unlink order

        Parameters:
        -----------
        port : The port which need to be removed (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(port, int):
            raise TypeError(f"invalid type : {type(port)} is not int")
        self.__order = {"unlink": port}

    def get(self, value: str):
        """Add a get order

        Parameters:
        -----------
        value : The value which is requested (str)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(value, str):
            raise TypeError(f"invalid type : {type(value)} is not str")
        self.__order = {"get": value}

    def toJSON(self) -> bytes:
        """Convert the order to JSON format

        Returns:
        --------
        encoded_order : The encoded order (bytes)
        """
        return json.dumps(self.__order).encode()

    @staticmethod
    def fromJSON(encoded_order: bytes):
        """Convert the order in JSON format to an order

        Parameters:
        -----------
        encoded_order : The encoded order (bytes)

        Returns:
        --------
        order : The decoded order (Order)
        """
        order = Order()
        order.orderDict.update(json.loads(encoded_order))
        return order
