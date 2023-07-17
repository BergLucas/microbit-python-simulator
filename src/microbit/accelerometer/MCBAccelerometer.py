from .Accelerometer import Accelerometer
from typing import Tuple

class MCBAccelerometer(Accelerometer):
    GESTURES = ['up', 'down', 'left', 'right', 'face up', 'face down', 'freefall', '3g', '6g', '8g', 'shake']
    def __init__(self):
        """ Create a MCBAccelerometer object """
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.reset_gestures()

    def reset_gestures(self):
        """ Reset the current gesture and gesture history """
        self.__gesture = ''
        self.__gestures_history = []

    def do_gesture(self, gesture: str):
        """ Do a gesture 
        
        Parameters:
        -----------
        gesture : A gesture from the GESTURES constant (str)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the gesture is not in the GESTURES constant
        """
        if not isinstance(gesture, str):
            raise TypeError(f'invalid type : {type(gesture)} is not a str')
        if not gesture in MCBAccelerometer.GESTURES:
            raise ValueError(f'invalid gesture {gesture}')
        self.__gesture = gesture
        self.__gestures_history.append(gesture)
    
    def stop_gesture(self):
        """ Stop the current gesture """
        self.__gesture = ''

    def set_x(self, value : int):
        """ Set the x value

        Parameters:
        -----------
        value : The value between -2000 and 2000 (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if value is not between -2000 and 2000
        """
        if not isinstance(value, int):
            raise TypeError(f'invalid type : {type(value)} is not a int')
        if value < -2000 and 2000 < value:
            raise ValueError('x must be a integer between -2000 and 2000')
        self.__x = value

    def get_x(self) -> int:
        """ Get the x value

        Returns:
        -----------
        x : The x value between -2000 and 2000 (int)
        """
        return self.__x

    def set_y(self, value: int):
        """ Set the y value

        Parameters:
        -----------
        value : The value between -2000 and 2000 (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if value is not between -2000 and 2000
        """
        if not isinstance(value, int):
            raise TypeError(f'invalid type : {type(value)} is not a int')
        if value < -2000 and 2000 < value:
            raise ValueError('y must be a integer between -2000 and 2000')
        self.__y = value

    def get_y(self):
        """ Get the y value

        Returns:
        -----------
        y : The y value between -2000 and 2000 (int)
        """
        return self.__y

    def set_z(self, value: int):
        """ Set the z value

        Parameters:
        -----------
        value : The value between -2000 and 2000 (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if value is not between -2000 and 2000
        """
        if not isinstance(value, int):
            raise TypeError(f'invalid type : {type(value)} is not a int')
        if not isinstance(value, int) or value < -2000 and 2000 < value:
            raise ValueError('z must be a integer between -2000 and 2000')
        self.__z = value

    def get_z(self):
        """ Get the z value

        Returns:
        --------
        z : The z value between -2000 and 2000 (int)
        """
        return self.__z

    def get_values(self) -> Tuple[int]:
        """ Get the (x, y, z) tuple

        Returns:
        --------
        (x, y, z) : The (x, y, z) tuple between -2000 and 2000 (Tuple[int])
        """
        return (self.__x, self.__y, self.__z)

    def current_gesture(self) -> str:
        """ Get the current gesture

        Returns:
        --------
        gesture : The current gesture (str)
        """
        return self.__gesture

    def is_gesture(self, name: str) -> bool:
        """ Check if the current gesture is name

        Parameters:
        -----------
        name : The name of the gesture (str)

        Returns:
        --------
        is_gesture : True if the current gesture is name (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(name, str):
            raise TypeError(f'invalid type : {type(name)} is not a str')
        return name == self.__gesture

    def was_gesture(self, name: str) -> bool:
        """ Check if there is name in the gesture history

        Parameters:
        -----------
        name : The name of the gesture (str)
        
        Returns:
        --------
        is_gesture : True if if there is name in the gesture history (bool)

        Raises:
        -------
        TypeError if a parameter has an invalid type
        """
        if not isinstance(name, str):
            raise TypeError(f'invalid type : {type(name)} is not a str')
        return name in self.__gestures_history

    def get_gestures(self) -> Tuple[str]:
        """ Get the gestures history
        
        Returns:
        --------
        gestures : The gestures history (Tuple[str])
        """
        gestures = tuple(gesture for gesture in self.__gestures_history)
        self.reset_gestures()
        return gestures