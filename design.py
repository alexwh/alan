# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(388, 226)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.remote_port = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.remote_port.setMaximumSize(QtCore.QSize(70, 32))
        self.remote_port.setTabChangesFocus(True)
        self.remote_port.setObjectName("remote_port")
        self.gridLayout.addWidget(self.remote_port, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.remote_ip = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.remote_ip.setMaximumSize(QtCore.QSize(150, 32))
        self.remote_ip.setTabChangesFocus(True)
        self.remote_ip.setObjectName("remote_ip")
        self.gridLayout.addWidget(self.remote_ip, 1, 1, 1, 1)
        self.listen_ip = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.listen_ip.setMaximumSize(QtCore.QSize(150, 32))
        self.listen_ip.setTabChangesFocus(True)
        self.listen_ip.setPlaceholderText("")
        self.listen_ip.setObjectName("listen_ip")
        self.gridLayout.addWidget(self.listen_ip, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.go_button = QtWidgets.QPushButton(self.centralWidget)
        self.go_button.setObjectName("go_button")
        self.gridLayout.addWidget(self.go_button, 2, 0, 1, 3)
        self.listen_port = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.listen_port.setMaximumSize(QtCore.QSize(70, 32))
        self.listen_port.setObjectName("listen_port")
        self.gridLayout.addWidget(self.listen_port, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.remote_port.setPlainText(_translate("MainWindow", "10001"))
        self.label_2.setText(_translate("MainWindow", "Remote IP"))
        self.remote_ip.setPlainText(_translate("MainWindow", "127.0.0.1"))
        self.listen_ip.setPlainText(_translate("MainWindow", "127.0.0.1"))
        self.label.setText(_translate("MainWindow", "Listen IP"))
        self.go_button.setText(_translate("MainWindow", "go"))
        self.listen_port.setPlainText(_translate("MainWindow", "10000"))


