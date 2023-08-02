from microbit_protocol.peer import MicrobitWebsocketPeer
from microbit._internal.microbit import Microbit

peer = MicrobitWebsocketPeer.connect("localhost", 8765)

microbit = Microbit(peer)

microbit.start()
