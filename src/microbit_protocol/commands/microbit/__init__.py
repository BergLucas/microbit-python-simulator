from pydantic import BaseModel, Field
from typing import Literal


class MicrobitPanicCommand(BaseModel):
    command: Literal["microbit.panic"] = "microbit.panic"
    n: int = Field(..., ge=0, le=255)


class MicrobitResetCommand(BaseModel):
    command: Literal["microbit.reset"] = "microbit.reset"


class MicrobitRunningTimeCommand(BaseModel):
    command: Literal["microbit.running_time"] = "microbit.running_time"
    running_time: int = Field(..., ge=0)


class MicrobitSleepCommand(BaseModel):
    command: Literal["microbit.sleep"] = "microbit.sleep"
    n: int = Field(..., ge=0)


class MicrobitTemperatureCommand(BaseModel):
    command: Literal["microbit.temperature"] = "microbit.temperature"
    temperature: int = Field(..., ge=0, le=255)
