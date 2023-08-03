from microbit_protocol.commands.microbit import (
    MicrobitPanicCommand,
    MicrobitResetCommand,
    MicrobitTemperatureCommand,
    MicrobitButtonIsPressedCommand,
)
from microbit_protocol.commands import MicrobitDisplayModuleCommand
from microbit_protocol.exceptions import CommunicationClosed
from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.peer import MicrobitPeer
from microbit_client.button import MicrobitButton, Button
from microbit_client.display import Display
from _thread import interrupt_main
from typing import Union, get_args
from threading import Thread
import logging
import time

logger = logging.getLogger(__name__)


class Microbit:
    def __init__(self, peer: MicrobitPeer) -> None:
        self.__start_time = time.time()
        self.__peer = peer
        self.__temperature = 0
        self.__thread = None
        self.__button_a = MicrobitButton()
        self.__button_b = MicrobitButton()
        self.__display = Display(peer)

    @property
    def button_a(self) -> Button:
        return self.__button_a

    @property
    def button_b(self) -> Button:
        return self.__button_b

    @property
    def display(self) -> Display:
        return self.__display

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
        elif isinstance(command, MicrobitButtonIsPressedCommand):
            if command.instance == "button_a":
                self.__button_a.execute(command)
            elif command.instance == "button_b":
                self.__button_b.execute(command)
            else:
                raise ValueError(f"Unknown button instance: {command.instance}")
        elif isinstance(command, get_args(MicrobitDisplayModuleCommand)):
            self.__display.execute(command)
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
