def rgb(r: int, g: int, b: int) -> str:
    """Converts rgb to hexadecimal value.

    Args:
        r (int): The red value (0-255)
        g (int): The green value (0-255)
        b (int): The blue value (0-255)

    Returns:
        str: The hexadecimal value.
    """
    assert 0 <= r and r <= 255
    assert 0 <= g and g <= 255
    assert 0 <= b and b <= 255
    return "#%02x%02x%02x" % (r, g, b)
