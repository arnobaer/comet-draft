import argparse

from .measurement import Measurement

class Application:
    def __init__(self):
        self.worker = Measurement()
    def code(self):
        pass
    def run(self):
        self.worker.start()
        self.worker.join()
