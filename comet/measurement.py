import threading
import time
import random

class Measurement(threading.Thread):
    mutex = threading.Lock()
    def __init__(self, interval=.25):
        super(Measurement, self).__init__()
        self.interval = interval
        self.running = True
        self.data = [] # numpy? well it does not resize well...
    def stop(self):
        self.running = False
    def run(self):
        t = time.time()
        while self.running:
            if time.time() >= (t + self.interval):
                print("\033[33mTaking data...\033[0m", flush=True)
                self.mutex.acquire()
                point = len(self.data), random.random(), random.random()
                self.data.append(point)
                self.mutex.release()
                t = time.time()
        print("stopping measurement thread...")
