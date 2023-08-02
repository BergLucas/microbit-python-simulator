from microbit_protocol.peer import MicrobitWebsocketPeer, MicrobitIoPeer
from microbit._internal.microbit import Microbit

# peer = MicrobitWebsocketPeer.connect("localhost", 8765)
peer = MicrobitIoPeer()

microbit = Microbit(peer)

microbit.start()
