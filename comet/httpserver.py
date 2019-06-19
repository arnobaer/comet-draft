import os
import threading
import random
import time

from bottle import response, route, post
from bottle import static_file
from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import TEMPLATE_PATH
from bottle import run

from . import utilities
from . import __version__

class HttpServer:
    """HTTP server for comet applications."""

    default_host = 'localhost'
    default_port = 8080
    default_server = 'paste'

    assets_path = utilities.make_path('assets')
    views_path = utilities.make_path('views')

    def __init__(self, app):
        self.__app = app
        # Append path for views
        TEMPLATE_PATH.append(self.views_path)

        @route('/')
        @view('index')
        def index():
            return dict(
                title=self.app.name,
                version=__version__,
                app=self.app,
            )

        @route('/assets/<filename>')
        def assets(filename):
            return static_file(filename, root=self.assets_path)

        @post('/api/start')
        def start():
            app.start()

        @post('/api/stop')
        def stop():
            app.stop()

        @route('/api/status')
        def status():
            return dict(running=app.running, state=app.current_state or 'halted', samples=random.random())

    @property
    def app(self):
        return self.__app

    def run(self, **kwargs):
        """Runs the HTTP server."""
        kwargs['host'] = kwargs.get('host', self.default_host)
        kwargs['port'] = kwargs.get('port', self.default_port)
        kwargs['server'] = kwargs.get('server', self.default_server)
        thread = threading.Thread(target=self.__app.run)
        thread.start()
        run(**kwargs)
        print("\nshutting down, please wait...")
        self.__app.shutdown()
        thread.join()
