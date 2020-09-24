"""
This package is the simulation of the radio module from the microbit

Some options are available in the Options.py file

Documentation: https://microbit-micropython.readthedocs.io/fr/latest/radio.html
"""
from .Radio import RATE_250KBIT, RATE_1MBIT, RATE_2MBIT
from typing import Tuple, Union
def __startRadio():
    """ Start a radio 
    
    Returns:
    --------
    radio : The radio (Radio)

    Raises:
    -------
    TypeError if a parameter has an invalid type
    """
    from .Radio import Radio
    from .Options import SYNCHRONISATION_IP, SYNCHRONISATION_PORT, AUTO_START_SYNCHRONISATION_SERVER, BLUETOOTH_PORT, INTERVAL, TIMEOUT, DEBUG
    from synchronisation import Connection, checkAddress, SynchronisationServer
    # Check types
    if not isinstance(AUTO_START_SYNCHRONISATION_SERVER, bool):
        raise TypeError(f'invalid type : {type(AUTO_START_SYNCHRONISATION_SERVER)} is not bool')
    if not isinstance(SYNCHRONISATION_PORT, int):
        raise TypeError(f'invalid type : {type(SYNCHRONISATION_PORT)} is not int')
    if not isinstance(TIMEOUT, (int, type(None))):
        raise TypeError(f'invalid type : {type(TIMEOUT)} is not int')
    # Find the SynchronisationServer
    if SYNCHRONISATION_IP is None:
        SYNCHRONISATION_IP = __find_sync_server(SYNCHRONISATION_PORT, TIMEOUT)
        if SYNCHRONISATION_IP is None:
            SYNCHRONISATION_IP = '127.0.0.1'
    sync_address = (SYNCHRONISATION_IP, SYNCHRONISATION_PORT)
    checkAddress(sync_address)
    # Check if the server is on
    if not Connection.isPortOpen(sync_address, TIMEOUT):
        if AUTO_START_SYNCHRONISATION_SERVER:
            SynchronisationServer(SYNCHRONISATION_PORT, DEBUG).start()
            sync_address = ('127.0.0.1', SYNCHRONISATION_PORT)
        else:
            raise ConnectionError('Could not connect to the SynchronisationServer')
    return Radio(sync_address, BLUETOOTH_PORT, interval=INTERVAL, timeout=TIMEOUT, debug=DEBUG)

def __find_sync_server(port: int, timeout: int = None) -> Union[str, None]:
    """ Find the ip of a synchronisation server 
    
    Parameters:
    -----------
    port : The port to check (int)

    timeout : The timeout (optional - default: None) (int)

    Returns:
    --------
    ip : The ip of the server if found, None otherwise (Union[str, None])

    Raises:
    -------
    TypeError if a parameter has an invalid type
    """
    # Check types
    if not isinstance(port, int):
        raise TypeError(f'invalid type : {type(port)} is not int')
    if not isinstance(timeout, (int, type(None))):
        raise TypeError(f'invalid type : {type(timeout)} is not int')
    # Init
    import socket
    from synchronisation import Connection
    from threading import Thread, Lock
    from queue import Queue
    ips_queue = Queue()
    ips_lock = Lock()
    ip_list = []
    ip_lock = Lock()
    threads = []
    # Get the ip
    for ip in socket.gethostbyname_ex(socket.gethostname())[-1]:
        ip_parts = ip.split('.')
        if len(ip_parts) > 3:
            for i in range(256):
                ips_queue.put(f'{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{i}')
    # Create the ping function
    def ping():
        continue_ping = True
        while continue_ping:
            # Get the target ip
            ip_lock.acquire()
            ips_lock.acquire()
            if not ips_queue.empty and len(ip) == 0:
                target_ip = ips_queue.get()
            else:
                continue_ping = False
                target_ip = None
            ip_lock.release()
            ips_lock.release()
            # Check if target ip is a server
            if target_ip is not None and Connection.isPortOpen((target_ip, port)):
                ip_lock.acquire()
                if len(ip) == 0:
                    ip_list.append(target_ip)
                ip_lock.release()
                continue_ping = False
    # Check the localhost
    if Connection.isPortOpen(('127.0.0.1', port)):
        ip_list.append('127.0.0.1')
    else:
        # Create the threads
        for i in range(256):
            t = Thread(target=ping, daemon=True)
            t.start()
            threads.append(t)
        # Wait the threads
        for t in threads:
            t.join()
    # Return the ip if there is one
    if len(ip_list) == 0:
        return None
    else:
        return ip_list[0]

__radio = __startRadio()

def on():
    """ Turns the radio on. This needs to be explicitly called since the radio draws power and takes up memory that you may otherwise need. """
    __radio.on()

def off():
    """ Turns off the radio, thus saving power and memory. """
    __radio.off()

def config(**kwargs):
    """ Configures various keyword based settings relating to the radio. The available settings and their sensible default values are listed below.

    The length (default=32) defines the maximum length, in bytes, of a message sent via the radio. It can be up to 251 bytes long (254 - 3 bytes for S0, LENGTH and S1 preamble).

    The queue (default=3) specifies the number of messages that can be stored on the incoming message queue. If there are no spaces left on the queue for incoming messages, then the incoming message is dropped.

    The channel (default=7) can be an integer value from 0 to 83 (inclusive) that defines an arbitrary « channel » to which the radio is tuned. Messages will be sent via this channel and only messages received via this channel will be put onto the incoming message queue. Each step is 1MHz wide, based at 2400MHz.

    The power (default=6) is an integer value from 0 to 7 (inclusive) to indicate the strength of signal used when broadcasting a message. The higher the value the stronger the signal, but the more power is consumed by the device. The numbering translates to positions in the following list of dBm (decibel milliwatt) values: -30, -20, -16, -12, -8, -4, 0, 4.

    The address (default=0x75626974) is an arbitrary name, expressed as a 32-bit address, that’s used to filter incoming packets at the hardware level, keeping only those that match the address you set. The default used by other micro:bit related platforms is the default setting used here.

    The group (default=0) is an 8-bit value (0-255) used with the address when filtering messages. Conceptually, « address » is like a house/office address and « group » is like the person at that address to which you want to send your message.

    The data_rate (default=radio.RATE_1MBIT) indicates the speed at which data throughput takes place. Can be one of the following contants defined in the radio module : RATE_250KBIT, RATE_1MBIT or RATE_2MBIT.

    If config is not called then the defaults described above are assumed.
    """
    __radio.config(**kwargs)

def reset():
    """Reset the settings to their default values (as listed in the documentation for the config function above)."""
    __radio.reset()

def send_bytes(message: bytes):
    """ Sends a message containing bytes. """
    __radio.send_bytes(message)

def receive_bytes() -> bytes:
    """ Receive the next incoming message on the message queue.
    Returns None if there are no pending messages. Messages are returned as bytes.
    """
    return __radio.receive_bytes()

def receive_bytes_into(buffer):
    """ DOESNT WORK YET - Receive the next incoming message on the message queue.
    Copies the message into buffer, trimming the end of the message if necessary.
    Returns None if there are no pending messages, otherwise it returns the length of the message (which might be more than the length of the buffer)."""
    return __radio.receive_bytes_into(buffer)

def send(message: str):
    """ Sends a message string. This is the equivalent of send_bytes(bytes(message, 'utf8')) but with b'\\x01\\x00\\x01' prepended to the front (to make it compatible with other platforms that target the micro:bit). """
    __radio.send(message)

def receive() -> str:
    """ Works in exactly the same way as receive_bytes but returns whatever was sent.

    Currently, it’s equivalent to str(receive_bytes(), 'utf8') but with a check that the the first three bytes are b'\x01\x00\x01' (to make it compatible with other platforms that may target the micro:bit). It strips the prepended bytes before converting to a string.

    A ValueError exception is raised if conversion to string fails.
    """
    return __radio.receive()

def receive_full() -> Tuple[bytes, int, int]:
    """ Returns a tuple containing three values representing the next incoming message on the message queue. If there are no pending messages then None is returned.

    The three values in the tuple represent:

    the next incoming message on the message queue as bytes.
    the RSSI (signal strength): a value between 0 (strongest) and -255 (weakest) as measured in dBm.
    a microsecond timestamp: the value returned by time.ticks_us() when the message was received.
    """
    return __radio.receive_full()