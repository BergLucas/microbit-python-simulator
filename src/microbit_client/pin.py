from typing import Protocol, Literal


class MicroBitDigitalPin(Protocol):

    PULL_UP = 3
    PULL_DOWN = 1
    NO_PULL = 0

    def read_digital(self) -> Literal[0, 1]:
        """Return 1 if the pin is high, and 0 if it's low.

        Returns:
            Literal[0, 1]: 1 if the pin is high, and 0 if it's low.
        """
        ...

    def write_digital(self, value: Literal[0, 1]) -> None:
        """Set the pin to high if `value` is 1, or to low, if it is 0.

        Args:
            value (Literal[0, 1]): 1 if the pin is high, and 0 if it's low.
        """
        ...

    def set_pull(self, value: Literal[0, 1, 3]) -> None:
        """Set the pull state of the pin to one of the values: `pin.PULL_UP`, `pin.PULL_DOWN`, or `pin.NO_PULL`.
        (where pin is an instance of a pin).

        See below for discussion of default pull states.

        The pull mode for a pin is automatically configured when the pin changes to an input mode.
        Input modes are when you call `read_analog` / `read_digital` / `is_touched`.
        The default pull mode for these is, respectively, `NO_PULL`, `PULL_DOWN`, `PULL_UP`.
        Calling `set_pull` will configure the pin to be in `read_digital` mode with the given pull mode.

        Args:
            value (Literal[0, 1, 3]): `pin.PULL_UP`, `pin.PULL_DOWN`, or `pin.NO_PULL`.
        """
        ...

    def get_pull(self) -> Literal[0, 1, 3]:
        """Returns the pull configuration on a pin, which can be one of three possible values: `NO_PULL`, `PULL_DOWN`, or `PULL_UP`.
        These are set using the `set_pull()` method or automatically configured when a pin mode requires it.

        Returns:
            Literal[0, 1, 3]: `pin.NO_PULL`, `pin.PULL_DOWN`, or `pin.PULL_UP`.
        """
        ...

    def get_mode(
        self,
    ) -> Literal[
        "unused",
        "analog",
        "read_digital",
        "write_digital",
        "display",
        "button",
        "music",
        "audio",
        "touch",
        "i2c",
        "spi",
    ]:
        """Returns the pin mode.

        When a pin is used for a specific function, like writing a digital value, or reading an analog value, the pin mode changes.
        Pins can have one of the following modes: `"unused"`, `"analog"`, `"read_digital"`, `"write_digital"`, `"display"`, `"button"`, `"music"`, `"audio"`, `"touch"`, `"i2c"`, `"spi"`.
        """
        ...

    def write_analog(self, value: int) -> None:
        """Output a PWM signal on the pin, with the duty cycle proportional to the provided `value`.
        The `value` may be either an integer or a floating point number between 0 (0% duty cycle) and 1023 (100% duty).

        Args:
            value (int): The duty cycle of the PWM signal.
        """
        ...

    def set_analog_period(self, period: int) -> None:
        """Set the period of the PWM signal being output to `period` in milliseconds. The minimum valid value is 1ms.

        Args:
            period (int): The period of the PWM signal being output to `period` in milliseconds.
        """
        ...

    def set_analog_period_microseconds(self, period: int) -> None:
        """Set the period of the PWM signal being output to `period` in microseconds. The minimum valid value is 256µs."""
        ...

    def get_analog_period_microseconds(self) -> int:
        """Returns the configured period of the PWM signal in microseconds.

        Returns:
            int: The configured period of the PWM signal in microseconds.
        """
        ...


class MicroBitAnalogDigitalPin(MicroBitDigitalPin, Protocol):
    def read_analog(self) -> int:
        """Read the voltage applied to the pin, and return it as an integer between 0 (meaning 0V) and 1023 (meaning 3.3V).

        Returns:
            int: The voltage applied to the pin, and return it as an integer between 0 (meaning 0V) and 1023 (meaning 3.3V).
        """
        ...


class MicroBitTouchPin(MicroBitDigitalPin, Protocol):
    """Touch sensitive pin on the Micro:Bit board"""

    def is_touched(self) -> None:
        """Return `True` if the pin is being touched with a finger, otherwise return `False`.

        This test is done by measuring how much resistance there is between the pin and ground.
        A low resistance gives a reading of `True`.
        To get a reliable reading using a finger you may need to touch the ground pin with another part of your body,
        for example your other hand.
        """
        ...
