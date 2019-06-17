import time

class Procedure:

    def __init__(self, app, name):
        super(Procedure, self).__init__()
        self.__app = app
        self.__name = name

    @property
    def app(self):
        return self.__app

    @property
    def name(self):
        return self.__name

    def wait(self, delay):
        """Halt and wait for delay."""
        time.sleep(delay)

    def setup(self):
        pass

    def run(self):
        pass
