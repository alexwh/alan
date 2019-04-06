#!/usr/bin/env python3
import sys
import logging
import socket
import select
import signal
import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from qhexedit import QHexEdit

import design

class TCPServer(QThread):
    def __init__(self, app, local_ip, local_port, remote_ip, remote_port):
        super().__init__()
        self.local_ip = local_ip
        self.local_port = local_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.app = app

        self.app.sig.send_data.connect(self.send_data)

    def __del__(self):
        self.wait()

    def _exchange_data(self, client, remote):
        while True:
            # wait until client or remote is available for read
            readable, _, _ = select.select([client, remote], [], [])

            if client in readable:
                data = client.recv(4096)
                if data:
                    logging.debug(f"reading client data: {data}")
                    self.app.sig.recv_data.emit(data, "client")
                else:
                    logging.debug("done with recv in client")
                    break

            if remote in readable:
                data = remote.recv(4096)
                if data:
                    logging.debug(f"reading remote data: {data}")
                    self.app.sig.recv_data.emit(data, "remote")
                else:
                    logging.debug("done with recv in remote")
                    break

    def send_data(self, data, direction):
        if direction == "client":
            sock = self.remote_conn
        elif direction == "remote":
            sock = self.client_conn
        else:
            logging.error("invalid direction in send_data")
            return

        logging.debug(f"sending {data} to {direction}")
        if sock.send(data) <= 0:
            logging.debug(f"error sending to {direction}")
        # while self.app.remote_intercept_checkbox.isChecked():
        #     time.sleep(0.1)

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((self.local_ip, self.local_port))
        except OSError as err:
            self.app.sig.handle_error.emit("Binding error",
                                           f"Could not bind to local port: {self.local_port}\n{err}")
            return

        server.listen()
        self.client_conn, addr = server.accept()
        logging.info("recieved connection at {}:{}".format(*self.client_conn.getpeername()))

        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"connecting to remote: {self.remote_ip}:{self.remote_port}")
        self.remote_conn.connect((self.remote_ip, self.remote_port))

        self._exchange_data(self.client_conn, self.remote_conn)


class AlanSignal(QObject):
    handle_error = pyqtSignal(str, str, name='handle_error')
    recv_data = pyqtSignal(bytes, str, name='recv_data')
    send_data = pyqtSignal(bytes, str, name='send_data')

class AlanApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.client_hexedit = QHexEdit()
        self.remote_hexedit = QHexEdit()
        self.client_hexedit.setOverwriteMode(False)
        self.remote_hexedit.setOverwriteMode(False)
        self.client_hexedit_layout.addWidget(self.client_hexedit)
        self.remote_hexedit_layout.addWidget(self.remote_hexedit)
        self.client_hexedit.dataChanged.connect(self.update_client_data)
        self.remote_hexedit.dataChanged.connect(self.update_remote_data)
        self.tabs.currentChanged.connect(self.tab_changed)

        self.client_data = bytes()
        self.remote_data = bytes()
        self.sig = AlanSignal()

        self.sig.handle_error.connect(self.showerror)
        self.sig.recv_data.connect(self.receive_data)

        self.go_button.clicked.connect(self.tcp_handle)
        self.client_send_button.clicked.connect(self.send_client)
        self.remote_send_button.clicked.connect(self.send_remote)

    def showerror(self, title, message, buttons=QtWidgets.QMessageBox.Ok):
        QtWidgets.QMessageBox.critical(self, title, message, buttons)

    def update_client_data(self):
        self.client_data = self.client_hexedit.data()
        self.tabs.setTabText(self.tabs.indexOf(self.client_hexedit_tab), "Client Data (*)")

    def update_remote_data(self):
        self.remote_data = self.remote_hexedit.data()
        self.tabs.setTabText(self.tabs.indexOf(self.remote_hexedit_tab), "Remote Data (*)")

    def tab_changed(self, index):
        if index == self.tabs.indexOf(self.client_hexedit_tab):
            self.tabs.setTabText(index, "Client Data")
        if index == self.tabs.indexOf(self.remote_hexedit_tab):
            self.tabs.setTabText(index, "Remote Data")

    def receive_data(self, data, direction):
        if direction == "client":
            self.client_data += data
            self.client_hexedit.setData(self.client_data)
        elif direction == "remote":
            self.remote_data += data
            self.remote_hexedit.setData(self.remote_data)
        else:
            return

    def started(self):
        self.client_data = bytes()
        self.remote_data = bytes()
        self.go_button.setEnabled(False)

    def finished(self):
        self.go_button.setEnabled(True)

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

    def send_client(self):
        self.sig.send_data.emit(bytes(self.client_hexedit.data()), "client")

    def send_remote(self):
        self.sig.send_data.emit(bytes(self.remote_hexedit.data()), "remote")


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    form = AlanApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
