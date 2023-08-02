from microbit_protocol.commands.microbit import (
    MicrobitPanicCommand,
    MicrobitResetCommand,
    MicrobitTemperatureCommand,
)
from microbit_protocol.exceptions import CommunicationClosed
from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.peer import MicrobitPeer
from _thread import interrupt_main
from threading import Thread
from typing import Union
import logging
import time

logger = logging.getLogger(__name__)


class Microbit:
    def __init__(self, peer: MicrobitPeer) -> None:
        self.__start_time = time.time()
        self.__peer = peer
        self.__temperature = 0
        self.__thread = None

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

    def execute(self, command: MicrobitCommand) -> None:
        if isinstance(command, MicrobitTemperatureCommand):
            self.__temperature = command.temperature
        else:
            raise ValueError(f"Unknown command: {command}")

    def start(self) -> None:
        def listener(command: MicrobitCommand) -> None:
            try:
                self.execute(command)
            except ValueError as e:
                logger.warning(e)

        def target() -> None:
            try:
                self.__peer.listen(listener)
            except CommunicationClosed:
                logger.warning("Connection closed unexpectedly")
            interrupt_main()

        self.__thread = Thread(target=target, daemon=True)
        self.__thread.start()

    def stop(self) -> None:
        self.__peer.stop()
