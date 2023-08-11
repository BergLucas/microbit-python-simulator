from typing import Literal, Union

from pydantic import BaseModel

Gesture = Literal[
    "up",
    "down",
    "left",
    "right",
    "face up",
    "face down",
    "freefall",
    "3g",
    "6g",
    "8g",
    "shake",
]


class MicrobitAccelerometerGetX(BaseModel):
    """A command that sets the x value of the accelerometer."""

    command: Literal["microbit.accelerometer.get_x"] = "microbit.accelerometer.get_x"
    x: int


class MicrobitAccelerometerGetY(BaseModel):
    """A command that sets the y value of the accelerometer."""

    command: Literal["microbit.accelerometer.get_y"] = "microbit.accelerometer.get_y"
    y: int


class MicrobitAccelerometerGetZ(BaseModel):
    """A command that sets the z value of the accelerometer."""

    command: Literal["microbit.accelerometer.get_z"] = "microbit.accelerometer.get_z"
    z: int


class MicrobitAccelerometerCurrentGesture(BaseModel):
    """A command that sets the current gesture of the accelerometer."""

    command: Literal[
        "microbit.accelerometer.current_gesture"
    ] = "microbit.accelerometer.current_gesture"
    current_gesture: Union[Gesture, Literal[""]]


class MicrobitAccelerometerSetRange(BaseModel):
    """A command that sets the range of the accelerometer."""

    command: Literal[
        "microbit.accelerometer.set_range"
    ] = "microbit.accelerometer.set_range"
    value: Literal[2, 4, 8]


MicrobitAccelerometerModuleCommand = Union[
    MicrobitAccelerometerGetX,
    MicrobitAccelerometerGetY,
    MicrobitAccelerometerGetZ,
    MicrobitAccelerometerCurrentGesture,
    MicrobitAccelerometerSetRange,
]
