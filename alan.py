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
                self.app.sig.recv_data.emit(data, "client", False)
                if remote.send(data) <= 0:
                    break

            if remote in readable:
                data = remote.recv(4096)
                logging.debug(f"reading remote data: {data}")
                self.app.sig.recv_data.emit(data, "remote", False)
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

        remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"connecting to remote: {self.remote_ip}:{self.remote_port}")
        remote_conn.connect((self.remote_ip, self.remote_port))

        self._exchange_data(client_conn, remote_conn)


class AlanSignal(QObject):
    handle_error = pyqtSignal(str, str, name='handle_error')
    recv_data = pyqtSignal(bytes, str, bool, name='recv_data')

class AlanApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.client_hexedit = QHexEdit()
        self.remote_hexedit = QHexEdit()
        self.client_data = bytes()
        self.remote_data = bytes()
        self.sig = AlanSignal()

        self.sig.handle_error.connect(self.showerror)
        self.sig.recv_data.connect(self.receive_data)

        self.go_button.clicked.connect(self.tcp_handle)

    def showerror(self, title, message, buttons=QtWidgets.QMessageBox.Ok):
        QtWidgets.QMessageBox.critical(self, title, message, buttons)

    def receive_data(self, data, direction, overwrite=False):
        if direction == "client":
            if overwrite:
                self.client_data = bytes()
            self.client_data += data
            self.client_hexedit.setData(self.client_data)
            self.client_hexedit.show()
        elif direction == "remote":
            if overwrite:
                self.remote_data = bytes()
            self.remote_data += data
            self.remote_hexedit.setData(self.remote_data)
            self.remote_hexedit.show()
        else:
            return

    def started(self):
        self.go_button.setEnabled(False)

    def finished(self):
        self.go_button.setEnabled(True)
        self.client_data = bytes()
        self.remote_data = bytes()
        self.client_hexedit.close()
        self.remote_hexedit.close()

    def tcp_handle(self):
        local_ip = self.listen_ip.toPlainText()
        local_port = int(self.listen_port.toPlainText())
        remote_ip = self.remote_ip.toPlainText()
        remote_port = int(self.remote_port.toPlainText())

        logging.info(f"starting listen thread on {local_ip}:{local_port}")

        self.tcp_server_thread = TCPServer(self, local_ip, local_port, remote_ip, remote_port)
        self.tcp_server_thread.started.connect(self.started)
        self.tcp_server_thread.finished.connect(self.finished)
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
