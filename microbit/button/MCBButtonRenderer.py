from .MCBButton import MCBButton
from ..utils import rgb
from tkinter import Canvas

class MCBButtonRenderer(Canvas, MCBButton):
    def __init__(self, master, size, buttonKey=None):
        Canvas.__init__(self, master, width=size, height=size, bg=rgb(150, 150, 150), highlightthickness=0)
        MCBButton.__init__(self)
        # Create round
        self.__round = self.create_oval(size//4, size//4, 3*size//4, 3*size//4, fill='black')
        self.tag_bind(self.__round, '<Button-1>', lambda e: self.press())
        if buttonKey is not None:
            self.bind_all(f'<KeyPress-{buttonKey}>', lambda e: self.press())
        self.tag_bind(self.__round, '<ButtonRelease-1>', lambda e: self.release())
        if buttonKey is not None:
            self.bind_all(f'<KeyRelease-{buttonKey}>', lambda e: self.release())

    def press(self):
        MCBButton.press(self)
        self.itemconfig(self.__round, fill=rgb(30, 30, 30))

    def release(self):
        MCBButton.release(self)
        self.itemconfig(self.__round, fill='black')