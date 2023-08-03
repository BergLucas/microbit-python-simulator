from microbit_protocol.commands.microbit import (
    MicrobitPanicCommand,
    MicrobitResetCommand,
    MicrobitTemperatureCommand,
)
from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.peer import MicrobitPeer
from typing import Union
import logging
import time

logger = logging.getLogger(__name__)


class Microbit:
    def __init__(self, peer: MicrobitPeer) -> None:
        self.__start_time = time.time()
        self.__peer = peer
        self.__temperature = 0

        def listener(command: MicrobitCommand) -> None:
            if isinstance(command, MicrobitTemperatureCommand):
                self.__temperature = command.temperature

        peer.add_listener(listener)

    def panic(self, n: int) -> None:
        self.__peer.send_command(MicrobitPanicCommand(n=n))

    def reset(self) -> None:
        self.__peer.send_command(MicrobitResetCommand())

    def sleep(self, n: Union[int, float]) -> None:
        time.sleep(n / 1000)

    def running_time(self) -> Union[int, float]:
        return (time.time() - self.__start_time) * 1000

    def temperature(self) -> int:
        return self.__temperature
