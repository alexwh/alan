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
        MainWindow.resize(280, 181)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 130, 88, 34))
        self.pushButton.setObjectName("pushButton")
        self.listen_ip = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.listen_ip.setGeometry(QtCore.QRect(20, 30, 171, 31))
        self.listen_ip.setPlaceholderText("")
        self.listen_ip.setObjectName("listen_ip")
        self.remote_ip = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.remote_ip.setGeometry(QtCore.QRect(20, 70, 171, 31))
        self.remote_ip.setObjectName("remote_ip")
        self.listen_port = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.listen_port.setGeometry(QtCore.QRect(200, 30, 71, 31))
        self.listen_port.setObjectName("listen_port")
        self.remote_port = QtWidgets.QPlainTextEdit(self.centralWidget)
        self.remote_port.setGeometry(QtCore.QRect(200, 70, 71, 31))
        self.remote_port.setObjectName("remote_port")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.listen_ip.setPlainText(_translate("MainWindow", "127.0.0.1"))
        self.listen_port.setPlainText(_translate("MainWindow", "10000"))


