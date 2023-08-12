from typing import Union

from pydantic.type_adapter import TypeAdapter

from microbit_protocol.commands.microbit import MicrobitModuleCommand
from microbit_protocol.commands.microbit.accelerometer import (
    MicrobitAccelerometerModuleCommand,
)
from microbit_protocol.commands.microbit.display import MicrobitDisplayModuleCommand
from microbit_protocol.commands.radio import RadioSendBytesCommand

MicrobitCommand = Union[
    MicrobitModuleCommand,
    MicrobitDisplayModuleCommand,
    MicrobitAccelerometerModuleCommand,
    RadioSendBytesCommand,
]

MicrobitCommandAdapter = TypeAdapter(MicrobitCommand)
