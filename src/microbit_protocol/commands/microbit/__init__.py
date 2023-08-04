from pydantic import BaseModel, Field
from typing import Literal, Union


class MicrobitResetCommand(BaseModel):
    command: Literal["microbit.reset"] = "microbit.reset"


class MicrobitRunningTimeCommand(BaseModel):
    command: Literal["microbit.running_time"] = "microbit.running_time"
    running_time: int = Field(..., ge=0)


class MicrobitTemperatureCommand(BaseModel):
    command: Literal["microbit.temperature"] = "microbit.temperature"
    temperature: int = Field(..., ge=0, le=255)


class MicrobitButtonIsPressedCommand(BaseModel):
    command: Literal["microbit.Button.is_pressed"] = "microbit.Button.is_pressed"
    instance: Literal["button_a", "button_b"]
    is_pressed: bool


MicrobitModuleCommand = Union[
    MicrobitResetCommand,
    MicrobitRunningTimeCommand,
    MicrobitTemperatureCommand,
    MicrobitButtonIsPressedCommand,
]
