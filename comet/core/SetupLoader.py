import os

from .. import SETUPS_DIR
from .Setup import Setup

class SetupLoader:

    def __init__(self):
        pass

    def find(self):
        """Returns a list of available setups."""
        setups = []
        for node in os.listdir(SETUPS_DIR):
            path = os.path.join(SETUPS_DIR, node)
            if os.path.isdir(path):
                # Sanity check
                if os.path.isfile(os.path.join(path, "settings.yml")):
                    setups.append(node)
        return setups

    def load(self, name):
        """Load a setup by name. Returns setup instance."""
        setup = Setup()
        setup.load(os.path.join(SETUPS_DIR, name))
        return setup
