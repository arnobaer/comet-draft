import os
import threading

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
        self.__params = [HtmlParameter(param) for param in self.app.params.values()]
        # Append path for views
        TEMPLATE_PATH.append(self.views_path)

        @route('/')
        @view('index')
        def index():
            return dict(
                title=self.app.name,
                version=__version__,
                params=self.__params,
                app=self.app,
            )

        @route('/assets/<filename>')
        def assets(filename):
            return static_file(filename, root=self.assets_path)


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

class HtmlParameter:

    def __init__(self, param):
        self.param = param

    def render_attrs(self, **kwargs):
        """Serializes HTML attributes."""
        return ' '.join(['{}="{}"'.format(k, v) for k, v in kwargs.items()])

    def render_input(self, param):
        attrs = {}
        attrs['id'] = 'comet_param_{}'.format(param.name)
        attrs['value'] = param.value
        if self.param.type is float:
            attrs['type'] = 'number'
            attrs['step'] = format(1.0 / 10**param.prec)
        elif self.param.type is int:
            attrs['type'] = 'number'
        else:
            attrs['type'] = 'text'
        return '<input {}>'.format(self.render_attrs(**attrs))

    def render(self):
        name = self.param.name
        label = self.param.label
        unit = ' [{}]'.format(self.param.unit) if self.param.unit else ''
        input_elem = self.render_input(self.param)
        template = """<label for="comet_param_{name}">{label}</label><br>{input_elem}{unit}"""
        return template.format(**locals())

    def __str__(self):
        return self.render()
