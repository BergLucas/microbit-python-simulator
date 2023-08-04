from microbit_protocol.exceptions import CommunicationClosed
from microbit_protocol.peer import MicrobitWebsocketPeer
from microbit_client.pin import (
    MicroBitAnalogDigitalPin,
    MicroBitDigitalPin,
    MicroBitTouchPin,
)
from microbit_client.button import Button, MicrobitButton
from microbit_client.microbit import Microbit
from microbit_client.display import Display
from _thread import interrupt_main
from threading import Thread
import logging

logger = logging.getLogger(__name__)

peer = MicrobitWebsocketPeer.connect("localhost", 8765)

microbit = Microbit(peer)
display = Display(peer)
button_a: Button = MicrobitButton(peer, "button_a")
button_b: Button = MicrobitButton(peer, "button_b")

pin0: MicroBitTouchPin
pin1: MicroBitTouchPin
pin2: MicroBitTouchPin
pin3: MicroBitAnalogDigitalPin
pin4: MicroBitAnalogDigitalPin
pin5: MicroBitDigitalPin
pin6: MicroBitDigitalPin
pin7: MicroBitDigitalPin
pin8: MicroBitDigitalPin
pin9: MicroBitDigitalPin
pin10: MicroBitAnalogDigitalPin
pin11: MicroBitDigitalPin
pin12: MicroBitAnalogDigitalPin
pin13: MicroBitDigitalPin
pin14: MicroBitDigitalPin
pin15: MicroBitDigitalPin
pin16: MicroBitDigitalPin
pin19: MicroBitDigitalPin
pin20: MicroBitDigitalPin


def target() -> None:
    try:
        peer.listen()
    except CommunicationClosed:
        logger.warning("Connection closed unexpectedly")
    interrupt_main()


Thread(target=target, daemon=True).start()