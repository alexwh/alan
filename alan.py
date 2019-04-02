#!/usr/bin/env python3
import sys
import logging
import socket
import select
import signal
from PyQt5 import QtWidgets
from qhexedit import QHexEdit
from socketserver import ThreadingTCPServer, StreamRequestHandler

import design

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
                self.server.client_data += data
                if remote.send(data) <= 0:
                    break

            if remote in readable:
                data = remote.recv(4096)
                logging.debug(f"reading remote data: {data}")
                self.server.remote_data += data
                if client.send(data) <= 0:
                    break

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.he = QHexEdit()
        self.pushButton.clicked.connect(self.tcp_handle)

    def hexedit(self, data):
        self.he.setData(data)
        self.he.show()

    def tcp_handle(self):
        local_ip = self.listen_ip.toPlainText()
        local_port = int(self.listen_port.toPlainText())
        remote_ip = self.remote_ip.toPlainText()
        remote_port = int(self.remote_port.toPlainText())

        logging.info(f"listening on {local_ip}:{local_port}")
        with ThreadingTCPServer((local_ip, local_port), TCPProxy) as self.server:
            self.server.remote_ip = remote_ip
            self.server.remote_port = remote_port
            self.server.client_data = bytes()
            self.server.remote_data = bytes()
            self.server.handle_request()


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
