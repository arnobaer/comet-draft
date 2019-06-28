import os
import threading
import random
import logging
import time

from bottle import response, request
from bottle import route, post
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
        def api_start():
            # Update application parameters
            for name, value in request.forms.items():
                param = app.params.get(name)
                if param:
                    logging.debug("update param '%s' with value '%s'", name, value)
                    param.value = value
            # Start run
            app.start()

        @post('/api/stop')
        def api_stop():
            app.stop()

        @post('/api/pause')
        def api_pause():
            if app.state.lower() == 'paused':
                app.unpause()
            else:
                app.pause()

        @route('/api/status')
        def api_status():
            jobs = [(job.label, job.progress) for job in app.active_jobs]
            return dict(app=dict(status=dict(running=app.state=='running', state=app.state, samples=random.random(), active_jobs=jobs)))

        @route('/api/settings')
        def api_settings():
            return dict(app=dict(settings=app.settings))

        @route('/api/params')
        def api_params():
            params = [param.json() for param in app.params.values()]
            return dict(app=dict(params=params))

        @route('/api/devices')
        def api_devices():
            devices = [device.name for device in app.devices.values()]
            return dict(app=dict(devices=devices))

        @route('/api/collections')
        def api_collections():
            collections = [collection.name for collection in app.collections.values()]
            return dict(app=dict(collections=collections))

        @route('/api/collections/<name>/data')
        @route('/api/collections/<name>/data/offset/<offset>')
        def api_collections(name, offset=0):
            offset = int(offset)
            records = []
            size = 0
            collection = app.collections.get(name)
            if collection:
                size = len(collection) # TODO!
                records = collection.snapshot_from(offset)
            return dict(app=dict(collection=dict(name=name, size=size, offset=offset, records=records)))

        @route('/api/jobs')
        def api_jobs():
            jobs = [job.label for job in app.jobs.values()]
            return dict(app=dict(jobs=jobs))

        @route('/api/services')
        def api_services():
            services = [service.name for service in app.services.values()]
            return dict(app=dict(services=services))


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
