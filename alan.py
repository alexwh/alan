#!/usr/bin/env python3
import sys
import logging
import signal
import select
import socket
from socketserver import ThreadingTCPServer, StreamRequestHandler

class TCPProxy(StreamRequestHandler):
    def handle(self):
        logging.info("recieved connection at %s", self.connection.getpeername())
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect(("127.0.0.1", 10001))
        self.exchange(self.connection, remote)

    def exchange(self, client, remote):
        while True:
            # wait until client or remote is available for read
            readable, _, _ = select.select([client, remote], [], [])

            if client in readable:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break

            if remote in readable:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break


def handle_signal(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)

    with ThreadingTCPServer(('127.0.0.1', 10000), TCPProxy) as server:
        server.serve_forever()
