

class Procedure:

    def __init__(self, name):
        self.__name = name
        self.parent = None

    @property
    def name(self):
        return self.__name

    def setup(self):
        pass

    def run(self):
        pass
