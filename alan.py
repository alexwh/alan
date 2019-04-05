#!/usr/bin/env python3
import sys
import logging
import socket
import select
import signal
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject
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
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self.local_ip, self.local_port))
        except OSError:
            self.app.sig.handle_error.emit("Binding error",
                                           f"Could not bind to local port: {self.local_port}")
            return

        server.listen()
        client_conn, addr = server.accept()
        logging.info("recieved connection at {}:{}".format(*client_conn.getpeername()))

        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"connecting to remote: {self.remote_ip}:{self.remote_port}")
        self.remote_conn.connect((self.remote_ip, self.remote_port))

        self._exchange_data(client_conn, self.remote_conn)
        self.app.hexedit(self.client_data)


class AlanSignal(QObject):
    handle_error = pyqtSignal(str, str, name='handle_error')

class AlanApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.he = QHexEdit()
        self.pushButton.clicked.connect(self.tcp_handle)
        self.sig = AlanSignal()
        self.sig.handle_error.connect(self.showerror)

    def hexedit(self, data):
        self.he.setData(data)
        self.he.show()

    def showerror(self, title, message, buttons=QtWidgets.QMessageBox.Ok):
        QtWidgets.QMessageBox.critical(self, title, message, buttons)

    def tcp_handle(self):
        local_ip = self.listen_ip.toPlainText()
        local_port = int(self.listen_port.toPlainText())
        remote_ip = self.remote_ip.toPlainText()
        remote_port = int(self.remote_port.toPlainText())

        logging.info(f"starting listen thread on {local_ip}:{local_port}")

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
