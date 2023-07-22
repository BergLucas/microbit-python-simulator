from microbit._internal.microbit import Microbit
from microbit_protocol.peer import MicrobitPeer

peer = MicrobitPeer.connect("localhost", 8765)

microbit = Microbit(peer)

microbit.start()
