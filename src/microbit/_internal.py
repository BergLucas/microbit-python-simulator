import logging
import subprocess
from _thread import interrupt_main
from threading import Thread

from microbit_client.accelerometer import Accelerometer
from microbit_client.button import Button, MicrobitButton
from microbit_client.display import Display
from microbit_client.microbit import Microbit
from microbit_client.pin import (
    MicroBitAnalogDigitalPin,
    MicroBitDigitalPin,
    MicroBitTouchPin,
)
from microbit_protocol.exceptions import CommunicationClosedError
from microbit_protocol.peer import MicrobitWebsocketPeer

logger = logging.getLogger(__name__)

process = subprocess.Popen(
    ["python", "-m", "microbit_simulator"], shell=True  # noqa: S602, S607
)

peer = MicrobitWebsocketPeer.connect("localhost", 8765)

microbit = Microbit(peer)
display = Display(peer)
accelerometer = Accelerometer(peer)
button_a: Button = MicrobitButton(peer, "button_a")
button_b: Button = MicrobitButton(peer, "button_b")

pin0: MicroBitTouchPin = ...  # type: ignore
pin1: MicroBitTouchPin = ...  # type: ignore
pin2: MicroBitTouchPin = ...  # type: ignore
pin3: MicroBitAnalogDigitalPin = ...  # type: ignore
pin4: MicroBitAnalogDigitalPin = ...  # type: ignore
pin5: MicroBitDigitalPin = ...  # type: ignore
pin6: MicroBitDigitalPin = ...  # type: ignore
pin7: MicroBitDigitalPin = ...  # type: ignore
pin8: MicroBitDigitalPin = ...  # type: ignore
pin9: MicroBitDigitalPin = ...  # type: ignore
pin10: MicroBitAnalogDigitalPin = ...  # type: ignore
pin11: MicroBitDigitalPin = ...  # type: ignore
pin12: MicroBitAnalogDigitalPin = ...  # type: ignore
pin13: MicroBitDigitalPin = ...  # type: ignore
pin14: MicroBitDigitalPin = ...  # type: ignore
pin15: MicroBitDigitalPin = ...  # type: ignore
pin16: MicroBitDigitalPin = ...  # type: ignore
pin19: MicroBitDigitalPin = ...  # type: ignore
pin20: MicroBitDigitalPin = ...  # type: ignore


def target() -> None:
    try:
        peer.listen()
    except CommunicationClosedError:
        logger.warning("Connection closed unexpectedly")
    process.kill()
    interrupt_main()


Thread(target=target, daemon=True).start()
