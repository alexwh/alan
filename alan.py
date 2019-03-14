#!/usr/bin/env python3
import sys
import logging
import signal
import select
import socket
import click
from socketserver import ThreadingTCPServer, StreamRequestHandler

class TCPProxy(StreamRequestHandler):
    def handle(self):
        logging.info("recieved connection at %s", self.connection.getpeername())
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((self.server.remote_ip, self.server.remote_port))
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

@click.command()
@click.option("--local_ip", default="127.0.0.1", help="local ip to listen on")
@click.option("--local_port", default=10000, help="local port to listen on")
@click.argument("remote_ip")
@click.argument("remote_port", type=int)
def main(remote_ip, remote_port, local_ip, local_port):
    with ThreadingTCPServer((local_ip, local_port), TCPProxy) as server:
        server.remote_ip = remote_ip
        server.remote_port = remote_port
        server.serve_forever()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    main()
