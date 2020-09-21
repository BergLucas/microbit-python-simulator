from .MCBAccelerometer import MCBAccelerometer
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
        x_slider = self.__add_slider(slidersFrame, slider_width, 'X', lambda value: self.set_x(value))
        x_slider.grid(row=0, column=0, sticky='ns')
        # Y slider
        y_slider = self.__add_slider(slidersFrame, slider_width, 'Y', lambda value: self.set_y(value))
        y_slider.grid(row=0, column=1, sticky='ns')
        # Z slider
        z_slider = self.__add_slider(slidersFrame, slider_width, 'Z', lambda value: self.set_z(value))
        z_slider.grid(row=0, column=2, sticky='ns')

    def __add_slider(self, master, width, name, value_callback):
        sliderFrame = Frame(master, width=width, bg='')
        sliderFrame.rowconfigure(2, weight=1)
        intValue = IntVar(sliderFrame, 0)
        intValue.trace_add('write', lambda var, index, mode: value_callback(intValue.get()))
        label = Label(sliderFrame, text=name, font=Font(size=width//5))
        label.grid(row=0, column=0)
        spinbox = Spinbox(sliderFrame, from_=-2000, to=2000, textvariable=intValue, width=5, font=Font(size=width//5))
        spinbox.grid(row=1, column=0)
        slider = Scale(sliderFrame, from_=2000, to=-2000, showvalue=False, width=width, variable=intValue)
        slider.bind('<Double-Button-1>', lambda e: intValue.set(0))
        slider.grid(row=2, column=0, sticky='ns')
        return sliderFrame

    def __add_gesturesFrame(self):
        gesturesFrame = Frame(self)
        gesturesFrame.place()
        self.add(gesturesFrame, text='Gestures')
        def getCallback(gesture):
            return lambda: self.do_gesture(gesture)
        gesture_id = 0
        for gesture in MCBAccelerometer.GESTURES:
            self.__add_gesture(gesturesFrame, 10, 3, gesture_id//2, gesture_id%2, gesture, getCallback(gesture))
            gesture_id += 1
        self.__add_gesture(gesturesFrame, 10, 3, gesture_id//2, gesture_id%2, 'Stop gesture', lambda: self.stop_gesture())

    def __add_gesture(self, master, width, height, row, column, name, value_callback):
        gesture_button = Button(master, text=name, command=value_callback, padx=5, pady=5, width=width, height=height)
        master.rowconfigure(row, weight=1)
        master.columnconfigure(column, weight=1)
        gesture_button.grid(row=row, column=column)