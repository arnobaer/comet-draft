import pyvisa

class Driver:

    def __init__(self, resource, backend):
        self.resource = resource
        self.backend = backend
        self.resoure_manager = pyvisa.ResourceManager(self.backend)
        self.recover()

    def read(self):
        """Read from instrument."""
        return self.instrument.read()

    def write(self, command):
        """Write command to instrument."""
        return self.instrument.write(command)

    def query(self, command):
        """Writes and reads result for command."""
        return self.instrument.query(command)

    def recover(self):
        """Recover lost instrument connection."""
        self.instrument = self.resoure_manager.open_resource(self.resource)
