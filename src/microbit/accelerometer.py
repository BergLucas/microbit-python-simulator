from typing import Literal

Gesture = Literal[
    "",
    "up",
    "down",
    "left",
    "right",
    "face up",
    "face down",
    "freefall",
    "3g",
    "6g",
    "8g",
    "shake",
]


def get_x() -> int:
    """The acceleration measurement in the `x` axis in milli-g, as a positive or negative integer.

    Returns:
        int: The acceleration measurement in the x axis in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg.
    """
    ...


def get_y() -> int:
    """The acceleration measurement in the `y` axis in milli-g, as a positive or negative integer.

    Returns:
        int: The acceleration measurement in the y axis in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg.
    """
    ...


def get_z() -> int:
    """The acceleration measurement in the `z` axis in milli-g, as a positive or negative integer.

    Returns:
        int: The acceleration measurement in the z axis in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg.
    """
    ...


def get_values() -> tuple[int, int, int]:
    """The acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z.

    Returns:
        tuple[int, int, int]: The acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z. By default the accelerometer is configured with a range of +/- 2g, and so X, Y, and Z will be within the range of +/-2000mg."""
    ...


def get_strength() -> int:
    """Get the acceleration measurement of all axes combined, as a positive integer. This is the Pythagorean sum of the X, Y and Z axes.

    Returns:
        int: The combined acceleration strength of all the axes, in milli-g.
    """
    ...


def current_gesture() -> Gesture:
    """Return a String with the name of the current gesture.

    Returns:
        Gesture: The name of the current gesture.
    """
    ...


def is_gesture(name: Gesture) -> bool:
    """Return a Boolean indicating if the named gesture is currently active.

    Args:
        name (Gesture): String with the name of the gesture to check.

    Returns:
        bool: True if the named gesture is currently active, False otherwise.
    """
    ...


def was_gesture(name: Gesture) -> bool:
    """Return a Boolean indicating if the named gesture was active since the last call.

    Args:
        name (Gesture): String with the name of the gesture to check.

    Returns:
        bool: True if the named gesture was active since the last call, False otherwise.
    """
    ...


def get_gestures() -> tuple[Gesture]:
    """Get a historical list of the registered gestures.

    Calling this function clears the gesture history before returning.

    Returns:
        A tuple of the gesture history, most recent is listed last.
    """
    ...


def set_range(value: Literal[2, 4, 8]) -> None:
    """Set the accelerometer sensitivity range, in g (standard gravity),
    to the closest values supported by the hardware, so it rounds to either `2`, `4`, or `8` g.

    Args:
        value (Literal[2, 4, 8]): New range for the accelerometer, an integer in g.
    """
    ...
