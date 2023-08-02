from .Settings import *
from tkinter import (
    Frame,
    ttk,
    Scale,
    Label,
    Spinbox,
    Button,
    IntVar,
    Widget,
    Tk,
)
from tkinter.font import Font


class MCBAccelerometerRenderer(ttk.Notebook):
    def __init__(self, master: Widget, width: int, height: int):
        """Create a MCBAccelerometerRenderer object

        Parameters:
        -----------
        master : The parent widget (Widget)

        width : The width of the accelerometer (int)

        height : The height of the accelerometer (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if height <= 0 or width <= 0
        """
        if not isinstance(master, (Widget, Tk)):
            raise TypeError(f"invalid type : {type(master)} is not a Widget")
        if not isinstance(width, int):
            raise TypeError(f"invalid type : {type(width)} is not a int")
        if not isinstance(height, int):
            raise TypeError(f"invalid type : {type(height)} is not a int")
        if height <= 0:
            raise ValueError(f"invalid height : height can not be negative")
        if width <= 0:
            raise ValueError(f"invalid width : width can not be negative")
        ttk.Notebook.__init__(self, master, height=round(0.95 * height), width=width)
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.reset_gestures()
        # Add sliders
        self.__add_slidersFrame(width)
        self.__add_gesturesFrame()

    def __add_slidersFrame(self, width: int):
        """Add a sliders frame

        Parameters:
        -----------
        width : The slidersFrame width (int)
        """
        slidersFrame = Frame(self)
        slidersFrame.place()
        self.add(slidersFrame, text="Sliders")
        slider_width = round(width * 0.2)
        slidersFrame.rowconfigure(0, weight=1)
        slidersFrame.columnconfigure(0, pad=slider_width // 2)
        slidersFrame.columnconfigure(1, pad=slider_width // 2)
        slidersFrame.columnconfigure(2, pad=slider_width // 2)
        # X slider
        x_slider = self.__add_slider(
            slidersFrame, slider_width, "X", lambda value: self.set_x(value), False
        )
        x_slider.grid(row=0, column=0, sticky="ns")
        # Y slider
        y_slider = self.__add_slider(
            slidersFrame, slider_width, "Y", lambda value: self.set_y(value), True
        )
        y_slider.grid(row=0, column=1, sticky="ns")
        # Z slider
        z_slider = self.__add_slider(
            slidersFrame, slider_width, "Z", lambda value: self.set_z(value), False
        )
        z_slider.grid(row=0, column=2, sticky="ns")

    def __add_slider(
        self, master: Widget, width: int, name: str, value_callback, invertSlider: bool
    ):
        """Add a slider

        Parameters:
        -----------
        master : The parent widget (Widget)

        width : The width of the slider (int)

        name : The name of the slider (str)

        value_callback : The callback on value change (function)

        invertSlider : Invert the slider if True (bool)
        """
        sliderFrame = Frame(master, width=width, bg="")
        sliderFrame.rowconfigure(2, weight=1)
        intValue = IntVar(sliderFrame, 0)
        intValue.trace_add(
            "write", lambda var, index, mode: value_callback(intValue.get())
        )
        label = Label(sliderFrame, text=name, font=Font(size=width // 5))
        label.grid(row=0, column=0)
        spinbox = Spinbox(
            sliderFrame,
            from_=-2000,
            to=2000,
            textvariable=intValue,
            width=5,
            font=Font(size=width // 5),
        )
        spinbox.grid(row=1, column=0)
        if invertSlider:
            slider = Scale(
                sliderFrame,
                from_=-2000,
                to=2000,
                showvalue=False,
                width=width,
                variable=intValue,
            )
        else:
            slider = Scale(
                sliderFrame,
                from_=2000,
                to=-2000,
                showvalue=False,
                width=width,
                variable=intValue,
            )
        slider.bind("<Double-Button-1>", lambda e: intValue.set(0))
        slider.grid(row=2, column=0, sticky="ns")
        if (
            f"{name}_increase" in SLIDERS_BUTTONS
            and SLIDERS_BUTTONS[f"{name}_increase"] is not None
        ):
            self.bind_all(
                f'<KeyPress-{SLIDERS_BUTTONS[f"{name}_increase"]}>',
                lambda e: intValue.set(min(2000, intValue.get() + SLIDERS_SPEED)),
            )
            if JOYSTICK_MODE:
                self.bind_all(
                    f'<KeyRelease-{SLIDERS_BUTTONS[f"{name}_increase"]}>',
                    lambda e: intValue.set(0),
                )
        if (
            f"{name}_decrease" in SLIDERS_BUTTONS
            and SLIDERS_BUTTONS[f"{name}_decrease"] is not None
        ):
            self.bind_all(
                f'<KeyPress-{SLIDERS_BUTTONS[f"{name}_decrease"]}>',
                lambda e: intValue.set(max(-2000, intValue.get() - SLIDERS_SPEED)),
            )
            if JOYSTICK_MODE:
                self.bind_all(
                    f'<KeyRelease-{SLIDERS_BUTTONS[f"{name}_decrease"]}>',
                    lambda e: intValue.set(0),
                )
        return sliderFrame

    def __add_gesturesFrame(self):
        """Add a gesturesFrame"""
        gesturesFrame = Frame(self)
        gesturesFrame.place()
        self.add(gesturesFrame, text="Gestures")

        def getCallback(gesture):
            return lambda: self.do_gesture(gesture)

        def getCommand(gesture):
            return lambda e: self.do_gesture(gesture)

        gesture_id = 0
        for gesture in self.GESTURES:
            self.__add_gesture(
                gesturesFrame,
                10,
                3,
                gesture_id // 2,
                gesture_id % 2,
                gesture,
                getCallback(gesture),
            )
            if gesture in GESTURES_BUTTONS and GESTURES_BUTTONS[gesture] is not None:
                self.bind_all(
                    f"<KeyPress-{GESTURES_BUTTONS[gesture]}>", getCommand(gesture)
                )
                self.bind_all(
                    f"<KeyRelease-{GESTURES_BUTTONS[gesture]}>",
                    lambda e: self.stop_gesture(),
                )
            gesture_id += 1
        self.__add_gesture(
            gesturesFrame,
            10,
            3,
            gesture_id // 2,
            gesture_id % 2,
            "Stop gesture",
            lambda: self.stop_gesture(),
        )

    def __add_gesture(
        self,
        master: Widget,
        width: int,
        height: int,
        row: int,
        column: int,
        name: str,
        value_callback,
    ):
        """Add a gesture

        Parameters:
        -----------
        master : The parent widget (Widget)

        width : The width of the gesture frame (int)

        height : The height of the gesture frame (int)

        row : The row position of the gesture frame (int)

        column : The row position of the gesture frame (int)

        name : The name of the gesture frame (str)

        value_callback : The callback on value change (function)
        """
        gesture_button = Button(
            master,
            text=name,
            command=value_callback,
            padx=5,
            pady=5,
            width=width,
            height=height,
        )
        master.rowconfigure(row, weight=1)
        master.columnconfigure(column, weight=1)
        gesture_button.grid(row=row, column=column)

    GESTURES = [
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

    def reset_gestures(self):
        """Reset the current gesture and gesture history"""
        self.__gesture = ""
        self.__gestures_history = []

    def do_gesture(self, gesture: str):
        """Do a gesture

        Parameters:
        -----------
        gesture : A gesture from the GESTURES constant (str)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if the gesture is not in the GESTURES constant
        """
        if not isinstance(gesture, str):
            raise TypeError(f"invalid type : {type(gesture)} is not a str")
        if not gesture in self.GESTURES:
            raise ValueError(f"invalid gesture {gesture}")
        self.__gesture = gesture
        self.__gestures_history.append(gesture)

    def stop_gesture(self):
        """Stop the current gesture"""
        self.__gesture = ""

    def set_x(self, value: int):
        """Set the x value

        Parameters:
        -----------
        value : The value between -2000 and 2000 (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if value is not between -2000 and 2000
        """
        if not isinstance(value, int):
            raise TypeError(f"invalid type : {type(value)} is not a int")
        if value < -2000 and 2000 < value:
            raise ValueError("x must be a integer between -2000 and 2000")
        self.__x = value

    def get_x(self) -> int:
        """Get the x value

        Returns:
        -----------
        x : The x value between -2000 and 2000 (int)
        """
        return self.__x

    def set_y(self, value: int):
        """Set the y value

        Parameters:
        -----------
        value : The value between -2000 and 2000 (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if value is not between -2000 and 2000
        """
        if not isinstance(value, int):
            raise TypeError(f"invalid type : {type(value)} is not a int")
        if value < -2000 and 2000 < value:
            raise ValueError("y must be a integer between -2000 and 2000")
        self.__y = value

    def get_y(self):
        """Get the y value

        Returns:
        -----------
        y : The y value between -2000 and 2000 (int)
        """
        return self.__y

    def set_z(self, value: int):
        """Set the z value

        Parameters:
        -----------
        value : The value between -2000 and 2000 (int)

        Raises:
        -------
        TypeError if a parameter has an invalid type

        ValueError if value is not between -2000 and 2000
        """
        if not isinstance(value, int):
            raise TypeError(f"invalid type : {type(value)} is not a int")
        if not isinstance(value, int) or value < -2000 and 2000 < value:
            raise ValueError("z must be a integer between -2000 and 2000")
        self.__z = value

    def get_z(self):
        """Get the z value

        Returns:
        --------
        z : The z value between -2000 and 2000 (int)
        """
        return self.__z

    def get_values(self) -> tuple[int, int, int]:
        """Get the (x, y, z) tuple

        Returns:
        --------
        (x, y, z) : The (x, y, z) tuple between -2000 and 2000 (Tuple[int])
        """
        return (self.__x, self.__y, self.__z)

    def current_gesture(self) -> str:
        """Get the current gesture

        Returns:
        --------
        gesture : The current gesture (str)
        """
        return self.__gesture

    def is_gesture(self, name: str) -> bool:
        """Check if the current gesture is name

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
            raise TypeError(f"invalid type : {type(name)} is not a str")
        return name == self.__gesture

    def was_gesture(self, name: str) -> bool:
        """Check if there is name in the gesture history

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
            raise TypeError(f"invalid type : {type(name)} is not a str")
        return name in self.__gestures_history

    def get_gestures(self) -> tuple[str, ...]:
        """Get the gestures history

        Returns:
        --------
        gestures : The gestures history (Tuple[str])
        """
        gestures = tuple(gesture for gesture in self.__gestures_history)
        self.reset_gestures()
        return gestures
