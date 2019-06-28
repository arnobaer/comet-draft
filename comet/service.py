import time
from .component import ControlComponent

class Service(ControlComponent):
    """Service base class, inherit to create custom services.

    Services are executed as threads by the application, property is_alive is
    used to test if the service is beeing executed.
    """

    def __init__(self, app, name):
        super(Service, self).__init__(app, name)
        self.__alive = True
        self.setup()

    @property
    def is_alive(self):
        """Retruns True if service is alive."""
        return self.__alive

    def quit(self):
        """Stops executing service."""
        self.__alive = False

    def setup(self):
        pass

    def configure(self):
        pass

    def run(self):
        pass
