from microbit_protocol.peer import MicrobitWebsocketPeer
from microbit_client.microbit import Microbit

peer = MicrobitWebsocketPeer.connect("localhost", 8765)

microbit = Microbit(peer)
display = microbit.display
button_a = microbit.button_a
button_b = microbit.button_b

microbit.start()
