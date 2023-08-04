from microbit_protocol.commands.microbit.accelerometer import Gesture
from microbit._internal import accelerometer as _accelerometer
from typing import Union, Literal


def get_x() -> int:
    """The acceleration measurement in the `x` axis in milli-g, as a positive or negative integer.

    Returns:
        int: The acceleration measurement in the x axis in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg.
    """
    return _accelerometer.get_x()


def get_y() -> int:
    """The acceleration measurement in the `y` axis in milli-g, as a positive or negative integer.

    Returns:
        int: The acceleration measurement in the y axis in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg.
    """
    return _accelerometer.get_y()


def get_z() -> int:
    """The acceleration measurement in the `z` axis in milli-g, as a positive or negative integer.

    Returns:
        int: The acceleration measurement in the z axis in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg.
    """
    return _accelerometer.get_z()


def get_values() -> tuple[int, int, int]:
    """The acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z.

    Returns:
        tuple[int, int, int]: The acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z. By default the accelerometer is configured with a range of +/- 2g, and so X, Y, and Z will be within the range of +/-2000mg."""
    return _accelerometer.get_values()


def get_strength() -> int:
    """Get the acceleration measurement of all axes combined, as a positive integer. This is the Pythagorean sum of the X, Y and Z axes.

    Returns:
        int: The combined acceleration strength of all the axes, in milli-g.
    """
    return _accelerometer.get_strength()


def current_gesture() -> Union[Gesture, Literal[""]]:
    """Return a String with the name of the current gesture.

    Returns:
        Union[Gesture, Literal[""]]: The name of the current gesture.
    """
    return _accelerometer.current_gesture()


def is_gesture(name: Gesture) -> bool:
    """Return a Boolean indicating if the named gesture is currently active.

    Args:
        name (Gesture): String with the name of the gesture to check.

    Returns:
        bool: True if the named gesture is currently active, False otherwise.
    """
    return _accelerometer.is_gesture(name)


def was_gesture(name: Gesture) -> bool:
    """Return a Boolean indicating if the named gesture was active since the last call.

    Args:
        name (Gesture): String with the name of the gesture to check.

    Returns:
        bool: True if the named gesture was active since the last call, False otherwise.
    """
    return _accelerometer.was_gesture(name)


def get_gestures() -> tuple[Gesture]:
    """Get a historical list of the registered gestures.

    Calling this function clears the gesture history before returning.

    Returns:
        A tuple of the gesture history, most recent is listed last.
    """
    return _accelerometer.get_gestures()


def set_range(value: Literal[2, 4, 8]) -> None:
    """Set the accelerometer sensitivity range, in g (standard gravity),
    to the closest values supported by the hardware, so it rounds to either `2`, `4`, or `8` g.

    Args:
        value (Literal[2, 4, 8]): New range for the accelerometer, an integer in g.
    """
    return _accelerometer.set_range(value)
