from microbit_protocol.commands.microbit.accelerometer import (
    Gesture,
    MicrobitAccelerometerGetX,
    MicrobitAccelerometerGetY,
    MicrobitAccelerometerGetZ,
    MicrobitAccelerometerCurrentGesture,
    MicrobitAccelerometerSetRange,
)
from microbit_protocol.exceptions import CommunicationClosed
from microbit_protocol.commands import MicrobitCommand
from microbit_protocol.peer import MicrobitPeer
from typing import Callable, Union, Literal, Optional
from tkinter.font import Font
from tkinter import (
    Frame,
    ttk,
    Scale,
    Label,
    Spinbox,
    Button,
    IntVar,
    Misc,
    Event,
)

GESTURES_BUTTONS: dict[str, str] = {
    "up": "1",
    "down": "2",
    "left": "3",
    "right": "4",
    "face up": "5",
    "face down": "6",
    "freefall": "7",
    "3g": "8",
    "6g": "9",
    "8g": "0",
    "shake": ")",
}
SLIDERS_BUTTONS: dict[str, str] = {
    "X_increase": "Right",
    "X_decrease": "Left",
    "Y_increase": "Down",
    "Y_decrease": "Up",
    "Z_increase": "Shift_L",
    "Z_decrease": "Control_L",
}
SLIDERS_SPEED = 2000
JOYSTICK_MODE = True


class MicrobitAccelerometer(ttk.Notebook):

    GESTURES: tuple[Gesture, ...] = (
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
    )

    def __init__(self, master: Misc, width: int, height: int) -> None:
        """Initialises self to a new MicrobitAccelerometer.

        Args:
            master (Misc): The master widget.
            width (int): The width of the widget.
            height (int): The height of the widget.
        """
        assert width > 0
        assert height > 0

        ttk.Notebook.__init__(self, master, height=round(0.95 * height), width=width)

        self.__current_gesture: Union[Gesture, Literal[""]] = ""
        self.__peer: Optional[MicrobitPeer] = None
        self.__max_value = 2000
        self.__x = 0
        self.__y = 0
        self.__z = 0

        self.__add_sliders_frame(width)
        self.__add_gestures_frame()

    @property
    def peer(self) -> Optional[MicrobitPeer]:
        """Return the microbit peer.

        Returns:
            Optional[MicrobitPeer]: The microbit peer.
        """
        return self.__peer

    @peer.setter
    def peer(self, value: Optional[MicrobitPeer]) -> None:
        """Set the microbit peer.

        Args:
            value (Optional[MicrobitPeer]): The microbit peer.
        """
        if self.__peer is not None:
            self.__peer.remove_listener(self.__execute)

        if value is not None:
            value.add_listener(self.__execute)

        self.__peer = value
        self.__sync_x()
        self.__sync_y()
        self.__sync_z()
        self.__sync_current_gesture()

    @property
    def max_value(self) -> int:
        """Gets the max value.

        Returns:
            int: The max value.
        """
        return self.__max_value

    def set_x(self, value: int) -> None:
        """Set the x value

        Args:
            value (int): The value between -self.max_value and self.max_value
        """
        assert -self.__max_value <= value and value <= self.__max_value

        should_sync = self.__x != value
        self.__x = value
        if should_sync:
            self.__sync_x()

    def get_x(self) -> int:
        """Get the x value

        Returns:
            int: The x value between -self.max_value and self.max_value
        """
        return self.__x

    def set_y(self, value: int) -> None:
        """Set the y value

        Args:
            value (int): The value between -self.max_value and self.max_value
        """
        assert -self.__max_value <= value and value <= self.__max_value

        should_sync = self.__y != value
        self.__y = value
        if should_sync:
            self.__sync_y()

    def get_y(self):
        """Get the y value

        Returns:
            int: The y value between -self.max_value and self.max_value
        """
        return self.__y

    def set_z(self, value: int) -> None:
        """Set the z value

        Args:
            value (int): The value between -self.max_value and self.max_value
        """
        assert -self.__max_value <= value and value <= self.__max_value

        should_sync = self.__z != value
        self.__z = value
        if should_sync:
            self.__sync_z()

    def get_z(self) -> int:
        """Get the z value

        Returns:
            int: The z value between -self.max_value and self.max_value
        """
        return self.__z

    def do_gesture(self, gesture: Gesture) -> None:
        """Do a gesture

        Args:
            gesture (Gesture): The gesture to do
        """
        self.__current_gesture = gesture
        self.__sync_current_gesture()

    def stop_gesture(self) -> None:
        """Stop the current gesture"""
        self.__current_gesture = ""
        self.__sync_current_gesture()

    def current_gesture(self) -> Union[Gesture, Literal[""]]:
        """Get the current gesture

        Returns:
            Union[Gesture, Literal[""]: The current gesture
        """
        return self.__current_gesture

    def __add_sliders_frame(self, width: int) -> None:
        """Adds the sliders frame to the notebook.

        Args:
            width (int): The width of the widget.
        """
        sliders_frame = Frame(self)
        sliders_frame.place()

        self.add(sliders_frame, text="Sliders")

        slider_width = round(width * 0.2)
        sliders_frame.rowconfigure(0, weight=1)
        sliders_frame.columnconfigure(0, pad=slider_width // 2)
        sliders_frame.columnconfigure(1, pad=slider_width // 2)
        sliders_frame.columnconfigure(2, pad=slider_width // 2)

        x_frame, self.__x_spinbox, self.__x_scale = self.__create_slider(
            master=sliders_frame,
            width=slider_width,
            name="X",
            value_callback=lambda value: self.set_x(value),
        )
        y_frame, self.__y_spinbox, self.__y_scale = self.__create_slider(
            master=sliders_frame,
            width=slider_width,
            name="Y",
            value_callback=lambda value: self.set_y(value),
        )
        z_frame, self.__z_spinbox, self.__z_scale = self.__create_slider(
            master=sliders_frame,
            width=slider_width,
            name="Z",
            value_callback=lambda value: self.set_z(value),
        )

        self.__set_max_value(2)

        x_frame.grid(row=0, column=0, sticky="ns")
        y_frame.grid(row=0, column=1, sticky="ns")
        z_frame.grid(row=0, column=2, sticky="ns")

    def __create_slider(
        self,
        master: Misc,
        width: int,
        name: str,
        value_callback: Callable[[int], None],
    ) -> tuple[Frame, Spinbox, Scale]:
        """Adds a slider to the master widget.

        Args:
            master (Misc): The master widget.
            width (int): The width of the widget.
            name (str): The name of the slider.
            value_callback (Callable[[int], None]): The callback function to call when the slider is changed.

        Returns:
            tuple[Frame, Spinbox, Scale]: The slider frame, the slider spinbox and the slider.
        """
        slider_frame = Frame(master, width=width, bg="")
        slider_frame.rowconfigure(2, weight=1)

        int_value = IntVar(slider_frame, 0)
        int_value.trace_add(
            "write", lambda var, index, mode: value_callback(int_value.get())
        )

        label = Label(slider_frame, text=name, font=Font(size=width // 5))
        label.grid(row=0, column=0)

        spinbox = Spinbox(
            slider_frame,
            from_=-self.__max_value,
            to=self.__max_value,
            textvariable=int_value,
            width=5,
            font=Font(size=width // 5),
        )
        spinbox.grid(row=1, column=0)

        scale = Scale(
            slider_frame,
            from_=-self.__max_value,
            to=self.__max_value,
            showvalue=False,
            width=width,
            variable=int_value,
        )

        scale.bind("<Double-Button-1>", lambda _: int_value.set(0))
        scale.grid(row=2, column=0, sticky="ns")

        if (increase := SLIDERS_BUTTONS.get(f"{name}_increase")) is not None:
            master.bind_all(
                f"<KeyPress-{increase}>",
                lambda _: int_value.set(min(2000, int_value.get() + SLIDERS_SPEED)),
            )
            if JOYSTICK_MODE:
                master.bind_all(f"<KeyRelease-{increase}>", lambda _: int_value.set(0))

        if (decrease := SLIDERS_BUTTONS.get(f"{name}_decrease")) is not None:
            master.bind_all(
                f"<KeyPress-{decrease}>",
                lambda _: int_value.set(max(-2000, int_value.get() - SLIDERS_SPEED)),
            )
            if JOYSTICK_MODE:
                master.bind_all(f"<KeyRelease-{decrease}>", lambda _: int_value.set(0))

        return slider_frame, spinbox, scale

    def __add_gestures_frame(self) -> None:
        """Adds the gestures frame to the notebook."""
        gestures_frame = Frame(self)
        gestures_frame.place()
        self.add(gestures_frame, text="Gestures")

        def getCallback(gesture: Gesture) -> Callable[[], None]:
            return lambda: self.do_gesture(gesture)

        def getCommand(gesture: Gesture) -> Callable[[Event], None]:
            return lambda _: self.do_gesture(gesture)

        gesture_id = 0

        for gesture_id, gesture in enumerate(self.GESTURES):
            self.__add_gesture(
                gestures_frame,
                10,
                3,
                gesture_id // 2,
                gesture_id % 2,
                gesture,
                getCallback(gesture),
            )
            if (gesture_button := GESTURES_BUTTONS.get(gesture)) is not None:
                self.bind_all(f"<KeyPress-{gesture_button}>", getCommand(gesture))
                self.bind_all(
                    f"<KeyRelease-{gesture_button}>",
                    lambda _: self.stop_gesture(),
                )

        self.__add_gesture(
            gestures_frame,
            10,
            3,
            gesture_id // 2,
            gesture_id % 2,
            "Stop gesture",
            lambda: self.stop_gesture(),
        )

    @staticmethod
    def __add_gesture(
        master: Misc,
        width: int,
        height: int,
        row: int,
        column: int,
        name: str,
        value_callback: Callable[[], None],
    ) -> None:
        """Adds a gesture button to the master widget.

        Args:
            master (Misc): The master widget.
            width (int): The width of the widget.
            height (int): The height of the widget.
            row (int): The row of the widget.
            column (int): The column of the widget.
            name (str): The name of the gesture.
            value_callback (Callable[[], None]): The callback function to call when the gesture is done.
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

    def __execute(self, command: MicrobitCommand) -> None:
        """Execute the given command.

        Args:
            command (MicrobitCommand): The command to execute.
        """
        if isinstance(command, MicrobitAccelerometerSetRange):
            self.__set_max_value(command.value)

    def __set_max_value(self, value: int) -> None:
        """Set the max value of the sliders.

        Args:
            value (int): The range.
        """
        self.__max_value = value * 2000
        half_value = self.__max_value // 2

        self.__x_spinbox.configure(from_=-half_value, to=half_value)
        self.__x_scale.configure(from_=half_value, to=-half_value)
        self.__y_spinbox.configure(from_=-half_value, to=half_value)
        self.__y_scale.configure(from_=-half_value, to=half_value)
        self.__z_spinbox.configure(from_=-half_value, to=half_value)
        self.__z_scale.configure(from_=half_value, to=-half_value)

    def __sync_x(self) -> None:
        """Sync the accelerometer's x value."""
        if self.__peer is not None:
            try:
                self.__peer.send_command(MicrobitAccelerometerGetX(x=self.__x))
            except CommunicationClosed:
                self.__peer = None

    def __sync_y(self) -> None:
        """Sync the accelerometer's y value."""
        if self.__peer is not None:
            try:
                self.__peer.send_command(MicrobitAccelerometerGetY(y=self.__y))
            except CommunicationClosed:
                self.__peer = None

    def __sync_z(self) -> None:
        """Sync the accelerometer's z value."""
        if self.__peer is not None:
            try:
                self.__peer.send_command(MicrobitAccelerometerGetZ(z=self.__z))
            except CommunicationClosed:
                self.__peer = None

    def __sync_current_gesture(self) -> None:
        """Sync the accelerometer's current_gesture value."""
        if self.__peer is not None:
            try:
                self.__peer.send_command(
                    MicrobitAccelerometerCurrentGesture(
                        current_gesture=self.__current_gesture
                    )
                )
            except CommunicationClosed:
                self.__peer = None
