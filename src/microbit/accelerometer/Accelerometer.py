from typing import Tuple
class Accelerometer:
    def get_x(self) -> int:
        """Get the acceleration measurement in the x axis, as a positive or negative integer, depending on the direction. The measurement is given in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg."""
        pass

    def get_y(self) -> int:
        """Get the acceleration measurement in the y axis, as a positive or negative integer, depending on the direction. The measurement is given in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg."""
        pass

    def get_z(self) -> int:
        """Get the acceleration measurement in the z axis, as a positive or negative integer, depending on the direction. The measurement is given in milli-g. By default the accelerometer is configured with a range of +/- 2g, and so this method will return within the range of +/- 2000mg."""
        pass

    def get_values(self) -> Tuple[int]:
        """Get the acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z. By default the accelerometer is configured with a range of +/- 2g, and so X, Y, and Z will be within the range of +/-2000mg."""
        pass

    def current_gesture(self) -> str:
        """Return the name of the current gesture."""
        pass

    def is_gesture(self, name: str) -> bool:
        """Return True or False to indicate if the named gesture is currently active."""
        pass

    def was_gesture(self, name: str) -> bool:
        """Return True or False to indicate if the named gesture was active since the last call."""
        pass

    def get_gestures(self) -> Tuple[str]:
        """Return a tuple of the gesture history. The most recent is listed last. Also clears the gesture history before returning."""
        pass