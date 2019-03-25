import sys
import os
from PyQt5 import QtWidgets
from qhexedit import QHexEdit

import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
