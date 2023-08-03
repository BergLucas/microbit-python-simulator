from pydantic import BaseModel, Field
from typing import Literal, Union


class MicrobitDisplaySetPixelCommand(BaseModel):
    command: Literal["microbit.display.set_pixel"] = "microbit.display.set_pixel"
    x: int = Field(..., ge=0, le=4)
    y: int = Field(..., ge=0, le=4)
    value: int = Field(..., ge=0, le=9)


class MicrobitDisplayClearCommand(BaseModel):
    command: Literal["microbit.display.clear"] = "microbit.display.clear"


class MicrobitDisplayShowCommand(BaseModel):
    command: Literal["microbit.display.show"] = "microbit.display.show"
    image: list[list[int]]


class MicrobitDisplayOnCommand(BaseModel):
    command: Literal["microbit.display.on"] = "microbit.display.on"


class MicrobitDisplayOffCommand(BaseModel):
    command: Literal["microbit.display.off"] = "microbit.display.off"


class MicrobitDisplayReadLightLevelCommand(BaseModel):
    command: Literal[
        "microbit.display.read_light_level"
    ] = "microbit.display.read_light_level"
    light_level: int = Field(..., ge=0, le=255)


MicrobitDisplayModuleCommand = Union[
    MicrobitDisplaySetPixelCommand,
    MicrobitDisplayClearCommand,
    MicrobitDisplayShowCommand,
    MicrobitDisplayOnCommand,
    MicrobitDisplayOffCommand,
    MicrobitDisplayReadLightLevelCommand,
]
