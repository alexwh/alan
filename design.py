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
        MainWindow.resize(698, 537)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.go_button = QtWidgets.QPushButton(self.centralWidget)
        self.go_button.setObjectName("go_button")
        self.gridLayout.addWidget(self.go_button, 4, 0, 1, 3)
        self.tabs = QtWidgets.QTabWidget(self.centralWidget)
        self.tabs.setObjectName("tabs")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.settings_tab)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.settings_tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.listen_ip = QtWidgets.QPlainTextEdit(self.settings_tab)
        self.listen_ip.setMaximumSize(QtCore.QSize(150, 32))
        self.listen_ip.setTabChangesFocus(True)
        self.listen_ip.setPlaceholderText("")
        self.listen_ip.setObjectName("listen_ip")
        self.gridLayout_2.addWidget(self.listen_ip, 0, 1, 1, 1)
        self.remote_ip = QtWidgets.QPlainTextEdit(self.settings_tab)
        self.remote_ip.setMaximumSize(QtCore.QSize(150, 32))
        self.remote_ip.setTabChangesFocus(True)
        self.remote_ip.setObjectName("remote_ip")
        self.gridLayout_2.addWidget(self.remote_ip, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.settings_tab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.listen_port = QtWidgets.QPlainTextEdit(self.settings_tab)
        self.listen_port.setMaximumSize(QtCore.QSize(70, 32))
        self.listen_port.setObjectName("listen_port")
        self.gridLayout_2.addWidget(self.listen_port, 0, 2, 1, 1)
        self.remote_port = QtWidgets.QPlainTextEdit(self.settings_tab)
        self.remote_port.setMaximumSize(QtCore.QSize(70, 32))
        self.remote_port.setTabChangesFocus(True)
        self.remote_port.setObjectName("remote_port")
        self.gridLayout_2.addWidget(self.remote_port, 2, 2, 1, 1)
        self.tabs.addTab(self.settings_tab, "")
        self.client_hexedit_tab = QtWidgets.QWidget()
        self.client_hexedit_tab.setObjectName("client_hexedit_tab")
        self.tabs.addTab(self.client_hexedit_tab, "")
        self.remote_hexedit_tab = QtWidgets.QWidget()
        self.remote_hexedit_tab.setObjectName("remote_hexedit_tab")
        self.tabs.addTab(self.remote_hexedit_tab, "")
        self.gridLayout.addWidget(self.tabs, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.go_button.setText(_translate("MainWindow", "go"))
        self.label_2.setText(_translate("MainWindow", "Remote IP"))
        self.listen_ip.setPlainText(_translate("MainWindow", "127.0.0.1"))
        self.remote_ip.setPlainText(_translate("MainWindow", "127.0.0.1"))
        self.label.setText(_translate("MainWindow", "Listen IP"))
        self.listen_port.setPlainText(_translate("MainWindow", "10000"))
        self.remote_port.setPlainText(_translate("MainWindow", "10001"))
        self.tabs.setTabText(self.tabs.indexOf(self.settings_tab), _translate("MainWindow", "Settings"))
        self.tabs.setTabText(self.tabs.indexOf(self.client_hexedit_tab), _translate("MainWindow", "Client Data"))
        self.tabs.setTabText(self.tabs.indexOf(self.remote_hexedit_tab), _translate("MainWindow", "Server Data"))


