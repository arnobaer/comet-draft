import time
from .component import Component

class Procedure(Component):

    def __init__(self, app, name):
        super(Procedure, self).__init__(app, name)
        self.__label = None
        self.__progress = 0.0
        self.__alive = True

    @property
    def label(self):
        return self.__name.replace('_', ' ').capitalize()

    @property
    def progress(self):
        """Returns state progress in percent."""
        return self.__progress

    @progress.setter
    def progress(self, percent):
        """Set state progress in percent."""
        self.__progress = max(0.0, min(100.0, float(percent)))

    def quit(self):
        self.__alive = False

    def wait(self, delay):
        """Halt and wait for delay."""
        time.sleep(delay)

    def configure(self):
        pass

    def run(self):
        pass
