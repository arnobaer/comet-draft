import logging
import threading
import time
import os

from bottle import response, route, post
from bottle import static_file
from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import run

import pyvisa

ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')
VIEWS_PATH = os.path.join(os.path.dirname(__file__), 'views')

from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(VIEWS_PATH)

from . import __version__
from .datasource import FakeDataSource
from .datawriter import DataWriter
# from .measurement import Measurement

from comet.device import DeviceManager

class DataFileWriter(DataWriter):
    def format(self, data):
        columns = ['{:.3f}'.format(time.time())]
        columns.extend(list(map(lambda value: format(value, '>8.3f'), data)))
        return '\t'.join(columns)

class CustomFileWriter(DataWriter):
    def format(self, data):
        return ''.join(map(lambda value: '[{:.1f}]'.format(value), data))

class Measurement(threading.Thread):

    mutex = threading.Lock()

    Running = 'running'
    Halted = 'halted'

    def __init__(self, interval=.25):
        super(Measurement, self).__init__()
        self.interval = interval
        self.state = self.Halted
        self.running = True
        self.data = [] # numpy? well it does not resize well...
        self.source = FakeDataSource()
        self.source.add_handler(DataFileWriter('samples.dat'))
        self.source.add_handler(CustomFileWriter('samples.asc'))
    def stop(self):
        self.running = False
    def run(self):
        t1 = time.time()
        while self.running:
            t2 = time.time()
            if self.state == self.Running and t2 >= (t1 + self.interval):
                self.mutex.acquire()
                data = self.source.read()
                point = [t2]
                point.extend(data)
                self.data.append(point)
                self.mutex.release()
                t1 = time.time()
                td = (t1-t2) * 1000.
                logging.info("\033[33mAcquired data (%.6f ms)\033[0m", td)
            else:
                time.sleep(self.interval / 4.)
        logging.debug("stopping measurement thread...")

class Application:

    def __init__(self, title='comet', backend=None):
        self.title = title
        self.backend = backend or ''
        self.log = []

        rm = pyvisa.ResourceManager('@sim')
        self.__device_manager = DeviceManager(rm)

        self.worker = Measurement()
        self.create_html_api()
        self.create_json_api()

        self.device_manager.create('SMU', 'GPIB::10', {})

    @property
    def device_manager(self):
        return self.__device_manager

    def create_html_api(self):
        @route('/')
        @view('index')
        def index():
            return dict(
                title=self.title,
                version=__version__,
            )

        @route('/assets/<filename>')
        def assets(filename):
            return static_file(filename, root=ASSETS_PATH)

    def create_json_api(self):
        @route('/api/data/<start:int>')
        def api_info(start=0):
            return dict(start=start, data=self.worker.data[start:])

        @route('/api/latest/<count:int>')
        def api_latest(count=1):
            return dict(start=len(self.worker.data)-count, data=self.worker.data[-count:])

        @post('/api/toggle')
        def api_toggle():
            if self.worker.state == self.worker.Running:
                self.worker.state = self.worker.Halted
            else:
                self.worker.state = self.worker.Running
            message = {
                self.worker.Halted: 'stopped',
                self.worker.Running: 'started',
            }[self.worker.state]
            self.append_log(message)

        @post('/api/reset/a')
        def api_reset_a():
            self.worker.source.reset_a()
            self.append_log('reset A')

        @post('/api/reset/b')
        def api_reset_b():
            self.worker.source.reset_b()
            self.append_log('reset B')

        @post('/api/gain')
        def api_gain():
            self.worker.source.gain()
            self.append_log('gain A+B')

        @route('/api/status')
        def api_info():
            return dict(
                name=self.title,
                version=__version__,
                backend=self.backend,
                mode=self.worker.state,
                samples=len(self.worker.data),
            )

        @route('/api/log')
        def api_info():
            return dict(log=self.log)

    def append_log(self, message):
        self.log.append(dict(
            ts=time.time(),
            message=message,
        ))

    def run(self, **kwargs):
        # Start main thread
        self.worker.start()

        # Run web service
        run(**kwargs)

        # Stop main thread
        self.worker.stop()
        self.worker.join()
