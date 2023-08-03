from microbit_protocol.exceptions import CommunicationClosed
from microbit_protocol.peer import MicrobitWebsocketPeer
from microbit_client.microbit import Microbit
from microbit_client.display import Display
from microbit_client.button import Button, MicrobitButton
from _thread import interrupt_main
from threading import Thread
import logging

logger = logging.getLogger(__name__)

peer = MicrobitWebsocketPeer.connect("localhost", 8765)

microbit = Microbit(peer)
display = Display(peer)
button_a: Button = MicrobitButton(peer, "button_a")
button_b: Button = MicrobitButton(peer, "button_b")


def target() -> None:
    try:
        peer.listen()
    except CommunicationClosed:
        logger.warning("Connection closed unexpectedly")
    interrupt_main()


Thread(target=target, daemon=True).start()
