from .Accelerometer import Accelerometer

class MCBAccelerometer(Accelerometer):
    GESTURES = ['up', 'down', 'left', 'right', 'face up', 'face down', 'freefall', '3g', '6g', '8g', 'shake']
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.reset_gestures()

    def reset_gestures(self):
        self.__gesture = ''
        self.__gestures_history = []

    def do_gesture(self, gesture):
        if not gesture in MCBAccelerometer.GESTURES:
            raise ValueError(f'invalid gesture {gesture}')
        self.__gesture = gesture
        self.__gestures_history.append(gesture)
    
    def stop_gesture(self):
        self.__gesture = ''

    def set_x(self, value):
        if not isinstance(value, int) or value < -2000 and 2000 < value:
            raise ValueError('x must be a integer between -2000 and 2000')
        self.__x = value

    def get_x(self):
        return self.__x

    def set_y(self, value):
        if not isinstance(value, int) or value < -2000 and 2000 < value:
            raise ValueError('y must be a integer between -2000 and 2000')
        self.__y = value

    def get_y(self):
        return self.__y

    def set_z(self, value):
        if not isinstance(value, int) or value < -2000 and 2000 < value:
            raise ValueError('z must be a integer between -2000 and 2000')
        self.__z = value

    def get_z(self):
        return self.__z

    def get_values(self):
        return [self.__x, self.__y, self.__z]

    def current_gesture(self):
        return self.__gesture

    def is_gesture(self, name):
        return name == self.__gesture

    def was_gesture(self, name):
        return name in self.__gestures_history

    def get_gestures(self):
        gestures = tuple(gesture for gesture in self.__gestures_history)
        self.reset_gestures()
        return gestures