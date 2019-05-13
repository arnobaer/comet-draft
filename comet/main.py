import argparse
import logging
import sys

from . import __version__
from .application import Application

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help="host, default is 0.0.0.0")
    parser.add_argument('--port', default=8080, type=int, help="port, default is 8080")
    parser.add_argument('--backend', default='@py', help="VISA backend, default is @py")
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()

    logging.getLogger().setLevel(logging.DEBUG)

    # Create application
    app = Application(backend=args.backend)

    # Run web service
    app.run(host=args.host, port=args.port, server='paste')

if __name__ == '__main__':
    main()
