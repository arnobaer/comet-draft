import time

class Procedure:

    def __init__(self, app, name):
        super(Procedure, self).__init__()
        self.__app = app
        self.__name = name
        self.__label = None
        self.__progress = 0.0

    @property
    def app(self):
        return self.__app

    @property
    def name(self):
        return self.__name

    @property
    def label(self):
        return self.__name.replace('_', ' ').capitalize()

    @property
    def progress(self):
        """Returns procedure progress in percent."""
        return self.__progress

    @progress.setter
    def progress(self, percent):
        """Set procedure progress in percent."""
        self.__progress = max(0.0, min(100.0, float(percent)))

    def wait(self, delay):
        """Halt and wait for delay."""
        time.sleep(delay)

    def setup(self):
        pass

    def run(self):
        pass
