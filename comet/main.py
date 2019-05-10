import argparse
import sys

from . import __version__
from .application import Application

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=8080, type=int)
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    # Create application
    app = Application()

    # Run web service
    app.run(host=args.host, port=args.port, server='paste')

if __name__ == '__main__':
    main()
