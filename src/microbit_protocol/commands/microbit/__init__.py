from typing import Literal, Union

from pydantic import BaseModel, Field


class MicrobitResetCommand(BaseModel):
    """A command that resets the micro:bit."""

    command: Literal["microbit.reset"] = "microbit.reset"


class MicrobitTemperatureCommand(BaseModel):
    """A command that sets the temperature of the micro:bit."""

    command: Literal["microbit.temperature"] = "microbit.temperature"
    temperature: int = Field(..., ge=0, le=255)


class MicrobitButtonIsPressedCommand(BaseModel):
    """A command that sets if a button is pressed."""

    command: Literal["microbit.Button.is_pressed"] = "microbit.Button.is_pressed"
    instance: Literal["button_a", "button_b"]
    is_pressed: bool


MicrobitModuleCommand = Union[
    MicrobitResetCommand,
    MicrobitTemperatureCommand,
    MicrobitButtonIsPressedCommand,
]
