from pydantic.type_adapter import TypeAdapter
from typing import Union

from microbit_protocol.commands.microbit.accelerometer import (
    MicrobitAccelerometerModuleCommand,
)
from microbit_protocol.commands.microbit.display import MicrobitDisplayModuleCommand
from microbit_protocol.commands.microbit import MicrobitModuleCommand


MicrobitCommand = Union[
    MicrobitModuleCommand,
    MicrobitDisplayModuleCommand,
    MicrobitAccelerometerModuleCommand,
]

MicrobitCommandAdapter = TypeAdapter(MicrobitCommand)
