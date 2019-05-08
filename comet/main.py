import argparse
import sys, os

import random

from bottle import response, route, run, template, view, static_file
#from bottle import jinja2_view as view

APP_TITLE = 'comet'
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
VIEWS_PATH = os.path.join(os.path.dirname(__file__), 'views')

import bottle
bottle.TEMPLATE_PATH.append(VIEWS_PATH)

from .measurement import Measurement
measurement = Measurement()

from . import __version__

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

@route('/api/info')
def api_info():
    return dict(name=APP_TITLE, version=__version__)

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
