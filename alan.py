#!/usr/bin/env python3
import sys
import logging
import signal
import select
import socket
import click
from socketserver import ThreadingTCPServer, StreamRequestHandler
from PyQt5 import QtWidgets
from qhexedit import QHexEdit

class TCPProxy(StreamRequestHandler):
    def handle(self):
        logging.info("recieved connection at {}:{}".format(*self.connection.getpeername()))
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"connecting to remote: {self.server.remote_ip}:{self.server.remote_port}")
        remote.connect((self.server.remote_ip, self.server.remote_port))
        self.exchange(self.connection, remote)

    def exchange(self, client, remote):
        while True:
            # wait until client or remote is available for read
            readable, _, _ = select.select([client, remote], [], [])

            if client in readable:
                data = client.recv(4096)
                logging.debug(f"reading client data: {data}")
                self.server.data += data
                if remote.send(data) <= 0:
                    break

            if remote in readable:
                data = remote.recv(4096)
                logging.debug(f"reading remote data: {data}")
                self.server.data += data
                if client.send(data) <= 0:
                    break

        if self.server.data:
            app = QtWidgets.QApplication(sys.argv)
            mainWin = QHexEdit()
            mainWin.setData(self.server.data)
            mainWin.setReadOnly(False)
            mainWin.resize(600, 400)
            mainWin.move(300, 300)
            mainWin.show()
            app.exec_()
            self.server.data = bytes()

def handle_signal(sig, frame):
    logging.info("exiting")
    sys.exit(0)

@click.command()
@click.option("--local_ip", default="127.0.0.1", help="local ip to listen on")
@click.option("--local_port", default=10000, help="local port to listen on")
@click.argument("remote_ip")
@click.argument("remote_port", type=int)
def main(remote_ip, remote_port, local_ip, local_port):
    logging.basicConfig(level=logging.DEBUG)

    logging.info(f"listening on {local_ip}:{local_port}")
    with ThreadingTCPServer((local_ip, local_port), TCPProxy) as server:
        server.remote_ip = remote_ip
        server.remote_port = remote_port
        server.data = bytes()
        server.serve_forever()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    main()
