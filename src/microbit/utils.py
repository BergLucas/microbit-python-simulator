def rgb(r, g, b):
    """Convert rgb to hexadecimal value

    Parameters:
    -----------
    r : The red value (int)

    g : The green value (int)

    b : The blue value (int)

    Returns:
    --------
    hexa : The hexadecimal value (str)
    """
    return "#%02x%02x%02x" % (r, g, b)
