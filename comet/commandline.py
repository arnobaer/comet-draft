import os
import argparse

from . import utilities
from . import __version__

class CommandLine:
    """Command line interface for comet applications."""

    def __init__(self, app):
        self.__app = app

    @property
    def app(self):
        return self.__app

    def run(self, args=None, **kwargs):
        # Create argument parser for application parameters
        parser = argparse.ArgumentParser()
        for param in self.app.params.values():
            parser.add_argument('--{}'.format(param.name), metavar=param.unit, type=param.type, default=param.value, required=param.required, help="{} (default {})".format(param.label, param.value))
        args = parser.parse_args(args or sys.argv)
        # Assign command line parameters to application
        for name, arg in args.__dict__.items():
            self.app.params.get(name).value = arg
        try:
            self.app.start()
            self.app.run()
        except KeyboardInterrupt:
            print("\nshutting down, please wait...")
            self.app.shutdown()
