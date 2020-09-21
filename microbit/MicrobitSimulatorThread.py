from threading import Thread, main_thread
from _thread import interrupt_main
from time import sleep
from .MicrobitSimulator import MicrobitSimulator

class __MicrobitSimulatorThread(Thread):
    def __init__(self):
        super().__init__(name='MicrobitSimulator')
        self.__mcbsim = None

    def run(self):
        self.__mcbsim = MicrobitSimulator()
        self.__mcbsim.mainloop()
        if main_thread().isAlive():
            interrupt_main()

    def getMcbsim(self):
        while self.__mcbsim == None and self.isAlive():
            self.join(0.1)
        return self.__mcbsim