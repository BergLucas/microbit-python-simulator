RGB_MIN_VALUE = 0
RGB_MAX_VALUE = 255


def rgb(r: int, g: int, b: int) -> str:
    """Converts rgb to hexadecimal value.

    Args:
        r (int): The red value (0-255)
        g (int): The green value (0-255)
        b (int): The blue value (0-255)

    Returns:
        str: The hexadecimal value.
    """
    assert RGB_MIN_VALUE <= r and r <= RGB_MAX_VALUE
    assert RGB_MIN_VALUE <= g and g <= RGB_MAX_VALUE
    assert RGB_MIN_VALUE <= b and b <= RGB_MAX_VALUE
    return "#%02x%02x%02x" % (r, g, b)
