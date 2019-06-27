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
            return dict(app=dict(status=dict(running=app.state=='running', state=app.state, samples=random.random())))

        @route('/api/settings')
        def settings():
            return dict(app=dict(settings=app.settings))

        @route('/api/params')
        def params():
            params = [param.json() for param in app.params.values()]
            return dict(app=dict(params=params))

        @route('/api/devices')
        def devices():
            devices = [device.name for device in app.devices.values()]
            return dict(app=dict(devices=devices))

        @route('/api/collections')
        def collections():
            collections = [collection.name for collection in app.collections.values()]
            return dict(app=dict(collections=collections))

        @route('/api/procedures')
        def procedures():
            procedures = [procedure.name for procedure in app.procedures.values()]
            return dict(app=dict(procedures=procedures))

        @route('/api/processes')
        def processes():
            processes = [processe.name for processe in app.processes.values()]
            return dict(app=dict(processes=processes))


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
