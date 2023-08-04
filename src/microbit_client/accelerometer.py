from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.commands.microbit.accelerometer import (
    Gesture,
    MicrobitAccelerometerGetX,
    MicrobitAccelerometerGetY,
    MicrobitAccelerometerGetZ,
    MicrobitAccelerometerCurrentGesture,
    MicrobitAccelerometerSetRange,
)
from microbit_protocol.peer import MicrobitPeer
from typing import Union, Literal
import math


class Accelerometer:
    def __init__(self, peer: MicrobitPeer) -> None:
        self.__peer = peer
        self.__current_gesture: Union[Gesture, Literal[""]] = ""
        self.__gestures: list[Gesture] = []
        self.set_range(2)
        self.__x = 0
        self.__y = 0
        self.__z = 0

        def listener(command: MicrobitCommand) -> None:
            if isinstance(command, MicrobitAccelerometerGetX):
                self.__x = command.x
            if isinstance(command, MicrobitAccelerometerGetY):
                self.__y = command.y
            if isinstance(command, MicrobitAccelerometerGetZ):
                self.__z = command.z
            if isinstance(command, MicrobitAccelerometerCurrentGesture):
                self.__current_gesture = command.current_gesture
                if command.current_gesture != "":
                    self.__gestures.append(command.current_gesture)

        peer.add_listener(listener)

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_z(self) -> int:
        return self.__z

    def get_values(self) -> tuple[int, int, int]:
        return (self.__x, self.__y, self.__z)

    def get_strength(self) -> int:
        return round(
            math.sqrt(self.__x * self.__x + self.__y * self.__y + self.__z * self.__z)
        )

    def current_gesture(self) -> Union[Gesture, Literal[""]]:
        return self.__current_gesture

    def is_gesture(self, name: Gesture) -> bool:
        return self.__current_gesture == name

    def was_gesture(self, name: Gesture) -> bool:
        return name in self.__gestures

    def get_gestures(self) -> tuple[Gesture]:
        gestures = tuple(self.__gestures)
        self.__gestures.clear()
        return gestures

    def set_range(self, value: Literal[2, 4, 8]) -> None:
        self.__peer.send_command(MicrobitAccelerometerSetRange(value=value))
