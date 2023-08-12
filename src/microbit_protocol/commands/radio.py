from typing import Literal

from pydantic import BaseModel, Field

MIN_LENGTH = 0
MAX_LENGTH = 254

MIN_CHANNEL = 0
MAX_CHANNEL = 83

MIN_GROUP = 0
MAX_GROUP = 255

MIN_POWER = 0
MAX_POWER = 7


class RadioSendBytesCommand(BaseModel):
    """A command that sends bytes over the radio."""

    command: Literal["radio.send_bytes"] = "radio.send_bytes"
    address: int
    channel: int = Field(..., ge=MIN_CHANNEL, le=MAX_CHANNEL)
    group: int = Field(..., ge=MIN_GROUP, le=MAX_GROUP)
    power: int = Field(..., ge=MIN_POWER, le=MAX_POWER)
    message: bytes = Field(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH)
