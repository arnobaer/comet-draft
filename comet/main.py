import argparse
import sys, os

import random

from bottle import response, route, post
from bottle import template, view, static_file
from bottle import run

APP_TITLE = 'comet'
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
VIEWS_PATH = os.path.join(os.path.dirname(__file__), 'views')

import bottle
bottle.TEMPLATE_PATH.append(VIEWS_PATH)

import threading
import time
import random

class FakeDataSource:
    def __init__(self):
        self.reset_bar()
        self.reset_baz()
    def reset_bar(self):
        self.bar = 0.0
        self.bar_gain = +1.0
    def reset_baz(self):
        self.baz = 0.0
        self.baz_gain = +1.0
    def read(self):
        self.bar += random.uniform(.002, .03) * self.bar_gain
        self.baz += random.uniform(.001, .05) * self.baz_gain
        if self.bar > 1.0:
            self.bar_gain = -1.
        if self.bar < 0.0:
            self.bar_gain = +1.
        if self.baz > 1.0:
            self.baz_gain = -1.
        if self.baz < 0.0:
            self.baz_gain = +1.
        return random.random(), random.uniform(.1,.5), self.bar, self.baz

class Measurement(threading.Thread):
    mutex = threading.Lock()
    def __init__(self, interval=.25):
        super(Measurement, self).__init__()
        self.interval = interval
        self.running = True
        self.halted = True
        self.data = [] # numpy? well it does not resize well...
        self.source = FakeDataSource()
    def stop(self):
        self.running = False
    def run(self):
        t1 = time.time()
        while self.running:
            t2 = time.time()
            if not self.halted and t2 >= (t1 + self.interval):
                print("\033[33mTaking data...\033[0m", flush=True)
                self.mutex.acquire()
                data = self.source.read()
                point = [t2]
                point.extend(data)
                self.data.append(point)
                self.mutex.release()
                t1 = time.time()
            else:
                time.sleep(self.interval / 4.)
        print("stopping measurement thread...")

measurement = Measurement()

from . import __version__

class Mode:
    Halted = 'halted'
    Running = 'running'

@route('/')
@view('index')
def index(name='world'):
    return dict(title=APP_TITLE)

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=STATIC_PATH)

@route('/api/data/<start:int>')
def api_info(start=0):
    return dict(start=start, data=measurement.data[start:])

@route('/api/latest/<count:int>')
def api_latest(count=1):
    return dict(start=len(measurement.data)-count, data=measurement.data[-count:])

@post('/api/start_stop')
def api_start_stop():
    measurement.halted = not measurement.halted
    return dict()

@post('/api/reset/bar')
def api_reset_bar():
    measurement.source.reset_bar()
    return dict()

@post('/api/reset/baz')
def api_reset_baz():
    measurement.source.reset_baz()
    return dict()

@route('/api/status')
def api_info():
    mode = Mode.Halted if measurement.halted else Mode.Running
    return dict(name=APP_TITLE, version=__version__, mode=mode)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8080, type=int)
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    measurement.start()

    run(host=args.host, port=args.port, server='paste')

    measurement.stop()
    measurement.join()

if __name__ == '__main__':
    main()
