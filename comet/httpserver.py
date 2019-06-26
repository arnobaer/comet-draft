import os
import threading
import random
import time

from bottle import response, route, post
from bottle import static_file
from bottle import run

from . import utilities
from . import __version__

class HttpServer:
    """HTTP server for comet applications."""

    default_host = 'localhost'
    default_port = 8080
    default_server = 'paste'

    assets_path = utilities.make_path('assets/dist')

    def __init__(self, app):
        self.__app = app

        @route('/')
        @route('/<filename>')
        def assets(filename=None):
            return static_file(filename or 'index.html', root=self.assets_path)

        @post('/api/start')
        def start():
            app.start()

        @post('/api/stop')
        def stop():
            app.stop()

        @post('/api/pause')
        def pause():
            if app.state.lower() == 'paused':
                app.unpause()
            else:
                app.pause()

        @route('/api/status')
        def status():
            return dict(running=app.state=='running', state=app.state, samples=random.random())

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
        self.__app.quit()
        thread.join()
