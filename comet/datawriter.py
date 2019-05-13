import os

class DataWriter:

    def __init__(self, filename):
        self.filename = filename
        # Reset existign file
        with open(self.filename, "w") as f:
            f.flush()

    def format(self, data):
        """Overload with custom data format."""
        return format(data)

    def append(self, data):
        """Append data to file."""
        with open(self.filename, "a") as f:
            f.write(self.format(data))
            f.write(os.linesep)
