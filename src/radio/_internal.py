from threading import Thread

from microbit_client.radio import Radio
from microbit_server.radio import RadioServer

server = RadioServer("localhost", 8766)


def start() -> None:
    try:
        server.start()
    except OSError:
        pass


Thread(target=start, daemon=True).start()

radio = Radio("localhost", 8766)

radio.on()
