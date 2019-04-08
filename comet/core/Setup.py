import os
import yaml

class Setup:

    def __init__(self):
        self.settings = {}

    def load(self, path):
        filename = os.path.join(path, "settings.yml")
        with open(filename, "r") as fp:
            self.settings = yaml.safe_load(fp)
