import math
from typing import Literal, Union

from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.commands.microbit.accelerometer import (
    Gesture,
    MicrobitAccelerometerCurrentGesture,
    MicrobitAccelerometerGetX,
    MicrobitAccelerometerGetY,
    MicrobitAccelerometerGetZ,
    MicrobitAccelerometerSetRange,
)
from microbit_protocol.peer import MicrobitPeer


class Accelerometer:
    """This type represents a micro:bit's accelerometer client."""

    def __init__(self, peer: MicrobitPeer) -> None:
        """Initialises `self` to a new Accelerometer instance.

        Args:
            peer (MicrobitPeer): The peer to communicate with.
        """
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
        """Gets the x value of the accelerometer.

        Returns:
            int: The x value of the accelerometer.
        """
        return self.__x

    def get_y(self) -> int:
        """Gets the y value of the accelerometer.

        Returns:
            int: The y value of the accelerometer.
        """
        return self.__y

    def get_z(self) -> int:
        """Gets the z value of the accelerometer.

        Returns:
            int: The z value of the accelerometer.
        """
        return self.__z

    def get_values(self) -> tuple[int, int, int]:
        """Gets the x, y and z values of the accelerometer.

        Returns:
            tuple[int, int, int]: The x, y and z values of the accelerometer.
        """
        return (self.__x, self.__y, self.__z)

    def get_strength(self) -> int:
        """Gets the strength of the accelerometer.

        Returns:
            int: The strength of the accelerometer.
        """
        return round(
            math.sqrt(self.__x * self.__x + self.__y * self.__y + self.__z * self.__z)
        )

    def current_gesture(self) -> Union[Gesture, Literal[""]]:
        """Gets the current gesture of the accelerometer.

        Returns:
            Union[Gesture, Literal[""]]: The current gesture of the accelerometer.
        """
        return self.__current_gesture

    def is_gesture(self, name: Gesture) -> bool:
        """Checks if the current gesture is the given gesture.

        Args:
            name (Gesture): The gesture to check.

        Returns:
            bool: Whether the current gesture is the given gesture.
        """
        return self.__current_gesture == name

    def was_gesture(self, name: Gesture) -> bool:
        """Checks if the given gesture has just been performed.

        Args:
            name (Gesture): The gesture to check.

        Returns:
            bool: Whether the given gesture has just been performed.
        """
        return name in self.__gestures

    def get_gestures(self) -> tuple[Gesture]:
        """Gets the list of gestures that have just been performed.

        Returns:
            tuple[Gesture]: The list of gestures that have just been performed.
        """
        gestures = tuple(self.__gestures)
        self.__gestures.clear()
        return gestures

    def set_range(self, value: Literal[2, 4, 8]) -> None:
        """Sets the range of the accelerometer.

        Args:
            value (Literal[2, 4, 8]): The range to set the accelerometer to.
        """
        self.__peer.send_command(MicrobitAccelerometerSetRange(value=value))
