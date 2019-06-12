"""Bandbox simulation on TCP socket."""

import socketserver
import random, time
import argparse

class BrandboxHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Keep socket alive
        while True:
            temp = random.uniform(22, 26)
            hum = random.uniform(50, 70)
            data = self.request.recv(1024).decode().strip()
            print('::', data.split(), flush=True)
            time.sleep(random.uniform(.05,.5))
            if data == '*IDN?':
                self.request.send("BrandBox v1.0\n".encode())
                continue
            if data.split() == ['GET:ENV', '?']:
                self.request.send("{},{},0,0\n".format(temp, hum).encode())
                continue
            if data.split() == ['GET:TEMP', '?']:
                self.request.send("{}deg\n".format(temp).encode())
                continue
            if data.split() == ['GET:HUM', '?']:
                self.request.send("{}pt\n".format(hum).encode())
                continue
            self.request.send("ERR\n".encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=10000, type=int)
    args = parser.parse_args()

    print("Bandbox simulation...")
    print("serving on port", args.port)

    server = socketserver.ThreadingTCPServer((args.host, args.port), BrandboxHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

    print("Bandbox simulation stopped.")
