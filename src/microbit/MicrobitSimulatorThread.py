from threading import Thread, main_thread
from _thread import interrupt_main
from time import sleep
from .MicrobitSimulator import MicrobitSimulator


class MicrobitSimulatorThread(Thread):
    def __init__(self):
        """Create the MicrobitSimulator thread"""
        super().__init__(name="MicrobitSimulator")
        self.__mcbsim = None

    def run(self):
        """Run the MicrobitSimulator thread"""
        self.__mcbsim = MicrobitSimulator()
        self.__mcbsim.mainloop()
        if main_thread().is_alive():
            interrupt_main()

    def getMcbsim(self) -> MicrobitSimulator:
        """Get the MicrobitSimulator object

        Returns:
        --------
        microbit : The MicrobitSimulator (MicrobitSimulator)
        """
        while self.__mcbsim == None and self.is_alive():
            self.join(0.1)
        return self.__mcbsim
