#!/usr/bin/env python3
import sys
import logging
import socket
import select
import signal
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from qhexedit import QHexEdit

import design

class TCPServer(QThread):
    def __init__(self, app, local_ip, local_port, remote_ip, remote_port):
        QThread.__init__(self)
        self.local_ip = local_ip
        self.local_port = local_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.client_data = bytes()
        self.server_data = bytes()
        self.app = app

    def __del__(self):
        self.wait()

    def _exchange_data(self, client, remote):
        while True:
            # wait until client or remote is available for read
            readable, _, _ = select.select([client, remote], [], [])

            if client in readable:
                data = client.recv(4096)
                logging.debug(f"reading client data: {data}")
                self.client_data += data
                if remote.send(data) <= 0:
                    break

            if remote in readable:
                data = remote.recv(4096)
                logging.debug(f"reading remote data: {data}")
                self.remote_data += data
                if client.send(data) <= 0:
                    break

    def run(self):
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn.bind((self.local_ip, self.local_port))
        self.client_conn.listen()
        conn, addr = self.client_conn.accept()
        logging.info("recieved connection at {}:{}".format(*conn.getpeername()))

        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"connecting to remote: {self.remote_ip}:{self.remote_port}")
        self.remote_conn.connect((self.remote_ip, self.remote_port))

        self._exchange_data(conn, self.remote_conn)
        self.app.hexedit(self.client_data)


class AlanApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
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
        self.tcp_server_thread = TCPServer(self, local_ip, local_port, remote_ip, remote_port)
        self.tcp_server_thread.start()


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    form = AlanApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
