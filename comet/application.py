import threading
import time
import os

from bottle import response, route, post
from bottle import static_file
from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import run

ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'static')
VIEWS_PATH = os.path.join(os.path.dirname(__file__), 'views')

from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(VIEWS_PATH)

from . import __version__
from .datasource import FakeDataSource
# from .measurement import Measurement

class DataFileWriter:
    def __init__(self, filename):
        self.filename = filename
        # Reset if file exists
        with open(self.filename, "w") as f:
            f.flush()
    def append(self, data):
        with open(self.filename, "a") as f:
            columns = '\t'.join(map(lambda value: format(value, '>8.3f'), data))
            f.write('{:.3f}\t'.format(time.time()))
            f.write(columns)
            f.write(os.linesep)

class CustomFileWriter:
    def __init__(self, filename):
        self.filename = filename
        # Reset if file exists
        with open(self.filename, "w") as f:
            f.flush()
    def append(self, data):
        with open(self.filename, "a") as f:
            line = ''.join(map(lambda value: '[{:.1f}]'.format(value), data))
            f.write(line)
            f.write(os.linesep)

class Measurement(threading.Thread):
    mutex = threading.Lock()
    def __init__(self, interval=.25):
        super(Measurement, self).__init__()
        self.interval = interval
        self.running = True
        self.halted = True
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

class Mode:
        Halted = 'halted'
        Running = 'running'

class Application:

    def __init__(self, title='comet'):
        self.title = title
        self.log = []
        self.init_html()
        self.init_json_api()
        self.worker = Measurement()

    def init_html(self):
        @route('/')
        @view('index')
        def index():
            return dict(title=self.title)

        @route('/assets/<filename>')
        def assets(filename):
            return static_file(filename, root=ASSETS_PATH)

    def init_json_api(self):
        @route('/api/data/<start:int>')
        def api_info(start=0):
            return dict(start=start, data=self.worker.data[start:])

        @route('/api/latest/<count:int>')
        def api_latest(count=1):
            return dict(start=len(self.worker.data)-count, data=self.worker.data[-count:])

        @post('/api/toggle')
        def api_toggle():
            self.worker.halted = not self.worker.halted
            message = {True:'stopped', False:'started'}[self.worker.halted]
            self.append_log(message)

        @post('/api/reset/a')
        def api_reset_a():
            self.worker.source.reset_a()
            self.append_log('reset A')

        @post('/api/reset/b')
        def api_reset_b():
            self.worker.source.reset_b()
            self.append_log('reset B')

        @route('/api/status')
        def api_info():
            mode = {False:Mode.Running, True:Mode.Halted}[self.worker.halted]
            return dict(name=self.title, version=__version__, mode=mode)

        @route('/api/log')
        def api_info():
            return dict(log=self.log)

    def append_log(self, message):
        self.log.append(dict(ts=time.time(), message=message))

    def run(self, **kwargs):
        # Start main thread
        self.worker.start()

        # Run web service
        run(**kwargs)

        # Stop main thread
        self.worker.stop()
        self.worker.join()
