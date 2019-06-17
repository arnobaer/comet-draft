

class Procedure:

    def __init__(self, app, name, continious=False):
        self.__app = app
        self.__name = name
        self.parent = None

    @property
    def app(self):
        return self.__app

    @property
    def name(self):
        return self.__name

    def setup(self):
        pass

    def run(self):
        pass
