from .MCBAccelerometer import MCBAccelerometer
from .Options import *
from tkinter import Frame, ttk, Scale, Label, Spinbox, Button, Grid, IntVar, StringVar
from tkinter.font import Font

class MCBAccelerometerRenderer(ttk.Notebook, MCBAccelerometer):
    def __init__(self, master, width, height):
        ttk.Notebook.__init__(self, master, height=round(0.95*height), width=width)
        MCBAccelerometer.__init__(self)
        # Add sliders
        self.__add_slidersFrame(width)
        self.__add_gesturesFrame()
    
    def __add_slidersFrame(self, width):
        slidersFrame = Frame(self)
        slidersFrame.place()
        self.add(slidersFrame, text='Sliders')
        slider_width = round(width*0.2)
        slidersFrame.rowconfigure(0, weight=1)
        slidersFrame.columnconfigure(0, pad=slider_width//2)
        slidersFrame.columnconfigure(1, pad=slider_width//2)
        slidersFrame.columnconfigure(2, pad=slider_width//2)
        # X slider
        x_slider = self.__add_slider(slidersFrame, slider_width, 'X', lambda value: self.set_x(value), False)
        x_slider.grid(row=0, column=0, sticky='ns')
        # Y slider
        y_slider = self.__add_slider(slidersFrame, slider_width, 'Y', lambda value: self.set_y(value), True)
        y_slider.grid(row=0, column=1, sticky='ns')
        # Z slider
        z_slider = self.__add_slider(slidersFrame, slider_width, 'Z', lambda value: self.set_z(value), False)
        z_slider.grid(row=0, column=2, sticky='ns')

    def __add_slider(self, master, width, name, value_callback, invertSlider):
        sliderFrame = Frame(master, width=width, bg='')
        sliderFrame.rowconfigure(2, weight=1)
        intValue = IntVar(sliderFrame, 0)
        intValue.trace_add('write', lambda var, index, mode: value_callback(intValue.get()))
        label = Label(sliderFrame, text=name, font=Font(size=width//5))
        label.grid(row=0, column=0)
        spinbox = Spinbox(sliderFrame, from_=-2000, to=2000, textvariable=intValue, width=5, font=Font(size=width//5))
        spinbox.grid(row=1, column=0)
        if invertSlider:
            slider = Scale(sliderFrame, from_=-2000, to=2000, showvalue=False, width=width, variable=intValue)
        else:
            slider = Scale(sliderFrame, from_=2000, to=-2000, showvalue=False, width=width, variable=intValue)
        slider.bind('<Double-Button-1>', lambda e: intValue.set(0))
        slider.grid(row=2, column=0, sticky='ns')
        if f'{name}_increase' in SLIDERS_BUTTONS and SLIDERS_BUTTONS[f'{name}_increase'] is not None:
            self.bind_all(f'<KeyPress-{SLIDERS_BUTTONS[f"{name}_increase"]}>', lambda e: intValue.set(min(2000, intValue.get()+SLIDERS_SPEED)))
            if JOYSTICK_MODE:
                self.bind_all(f'<KeyRelease-{SLIDERS_BUTTONS[f"{name}_increase"]}>', lambda e: intValue.set(0))
        if f'{name}_decrease' in SLIDERS_BUTTONS and SLIDERS_BUTTONS[f'{name}_decrease'] is not None:
            self.bind_all(f'<KeyPress-{SLIDERS_BUTTONS[f"{name}_decrease"]}>', lambda e: intValue.set(max(-2000, intValue.get()-SLIDERS_SPEED)))
            if JOYSTICK_MODE:
                self.bind_all(f'<KeyRelease-{SLIDERS_BUTTONS[f"{name}_decrease"]}>', lambda e: intValue.set(0))
        return sliderFrame

    def __add_gesturesFrame(self):
        gesturesFrame = Frame(self)
        gesturesFrame.place()
        self.add(gesturesFrame, text='Gestures')
        def getCallback(gesture):
            return lambda: self.do_gesture(gesture)
        def getCommand(gesture):
            return lambda e: self.do_gesture(gesture)
        gesture_id = 0
        for gesture in MCBAccelerometer.GESTURES:
            self.__add_gesture(gesturesFrame, 10, 3, gesture_id//2, gesture_id%2, gesture, getCallback(gesture))
            if gesture in GESTURES_BUTTONS and GESTURES_BUTTONS[gesture] is not None:
                self.bind_all(f'<KeyPress-{GESTURES_BUTTONS[gesture]}>', getCommand(gesture))
                self.bind_all(f'<KeyRelease-{GESTURES_BUTTONS[gesture]}>', lambda e: self.stop_gesture())
            gesture_id += 1
        self.__add_gesture(gesturesFrame, 10, 3, gesture_id//2, gesture_id%2, 'Stop gesture', lambda: self.stop_gesture())

    def __add_gesture(self, master, width, height, row, column, name, value_callback):
        gesture_button = Button(master, text=name, command=value_callback, padx=5, pady=5, width=width, height=height)
        master.rowconfigure(row, weight=1)
        master.columnconfigure(column, weight=1)
        gesture_button.grid(row=row, column=column)