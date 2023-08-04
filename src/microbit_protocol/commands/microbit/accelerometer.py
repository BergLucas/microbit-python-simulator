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
    command: Literal["microbit.accelerometer.get_x"] = "microbit.accelerometer.get_x"
    x: int


class MicrobitAccelerometerGetY(BaseModel):
    command: Literal["microbit.accelerometer.get_y"] = "microbit.accelerometer.get_y"
    y: int


class MicrobitAccelerometerGetZ(BaseModel):
    command: Literal["microbit.accelerometer.get_z"] = "microbit.accelerometer.get_z"
    z: int


class MicrobitAccelerometerCurrentGesture(BaseModel):
    command: Literal[
        "microbit.accelerometer.current_gesture"
    ] = "microbit.accelerometer.current_gesture"
    current_gesture: Union[Gesture, Literal[""]]


class MicrobitAccelerometerSetRange(BaseModel):
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
