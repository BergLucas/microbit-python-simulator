from pydantic.type_adapter import TypeAdapter
from typing import Union

from microbit_protocol.commands.microbit import (
    MicrobitPanicCommand,
    MicrobitResetCommand,
    MicrobitRunningTimeCommand,
    MicrobitSleepCommand,
    MicrobitTemperatureCommand,
    MicrobitButtonIsPressedCommand,
)

MicrobitCommand = Union[
    MicrobitPanicCommand,
    MicrobitResetCommand,
    MicrobitRunningTimeCommand,
    MicrobitSleepCommand,
    MicrobitTemperatureCommand,
    MicrobitButtonIsPressedCommand,
]

MicrobitCommandAdapter = TypeAdapter(MicrobitCommand)
