from typing import Literal, Union

from pydantic import BaseModel, Field

LED_MIN_VALUE = 0
LED_MAX_VALUE = 9

DISPLAY_MIN_X = 0
DISPLAY_MAX_X = 4

DISPLAY_MIN_Y = 0
DISPLAY_MAX_Y = 4

MIN_LIGHT_LEVEL = 0
MAX_LIGHT_LEVEL = 255


class MicrobitDisplaySetPixelCommand(BaseModel):
    """A command that sets the pixel of the display."""

    command: Literal["microbit.display.set_pixel"] = "microbit.display.set_pixel"
    x: int = Field(..., ge=DISPLAY_MIN_X, le=DISPLAY_MAX_X)
    y: int = Field(..., ge=DISPLAY_MIN_Y, le=DISPLAY_MAX_Y)
    value: int = Field(..., ge=LED_MIN_VALUE, le=LED_MAX_VALUE)


class MicrobitDisplayClearCommand(BaseModel):
    """A command that clears the display."""

    command: Literal["microbit.display.clear"] = "microbit.display.clear"


class MicrobitDisplayShowCommand(BaseModel):
    """A command that shows an image on the display."""

    command: Literal["microbit.display.show"] = "microbit.display.show"
    image: list[list[int]]


class MicrobitDisplayOnCommand(BaseModel):
    """A command that turns on the display."""

    command: Literal["microbit.display.on"] = "microbit.display.on"


class MicrobitDisplayOffCommand(BaseModel):
    """A command that turns off the display."""

    command: Literal["microbit.display.off"] = "microbit.display.off"


class MicrobitDisplayReadLightLevelCommand(BaseModel):
    """A command that sets the light level."""

    command: Literal[
        "microbit.display.read_light_level"
    ] = "microbit.display.read_light_level"
    light_level: int = Field(..., ge=MIN_LIGHT_LEVEL, le=MAX_LIGHT_LEVEL)


MicrobitDisplayModuleCommand = Union[
    MicrobitDisplaySetPixelCommand,
    MicrobitDisplayClearCommand,
    MicrobitDisplayShowCommand,
    MicrobitDisplayOnCommand,
    MicrobitDisplayOffCommand,
    MicrobitDisplayReadLightLevelCommand,
]
