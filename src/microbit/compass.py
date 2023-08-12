def calibrate() -> None:
    """Starts the calibration process.

    An instructive message will be scrolled to the user after which they
    will need to rotate the device in order to draw a circle on the LED display.
    """
    ...


def is_calibrated() -> bool:  # type: ignore
    """Returns `True` if the compass has been successfully calibrated.

    Returns `False` otherwise.

    Returns:
        bool: Whether the compass has been calibrated.
    """
    ...


def clear_calibration() -> None:
    """Undoes the calibration, making the compass uncalibrated again."""
    ...


def get_x() -> int:  # type: ignore
    """Gives the reading of the magnetic field strength on the `x` axis in nano tesla.

    It is a positive or negative integer, depending on the direction of the field.

    Returns:
        int: The reading of the magnetic field strength on the x axis.
    """
    ...


def get_y() -> int:  # type: ignore
    """Gives the reading of the magnetic field strength on the `y` axis in nano tesla.

    It is a positive or negative integer, depending on the direction of the field.

    Returns:
        int: The reading of the magnetic field strength on the y axis.
    """
    ...


def get_z() -> int:  # type: ignore
    """Gives the reading of the magnetic field strength on the `z` axis in nano tesla.

    It is a positive or negative integer, depending on the direction of the field.

    Returns:
        int: The reading of the magnetic field strength on the z axis.
    """
    ...


def heading() -> int:  # type: ignore
    """Gives the compass heading, calculated from the above readings.

    It is an integer in the range from 0 to 360, representing the angle in degrees,
    clockwise, with north as 0.

    Returns:
        int: The compass heading, from 0 to 360.
    """
    ...


def get_field_strength() -> int:  # type: ignore
    """Returns an indication of the magnitude of the magnetic field around the device.

    It is an integer in nano tesla.

    Returns:
        int: The magnitude of the magnetic field around the device in nano tesla.
    """
    ...
