import os
import sys
import json

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Cormix_Debug(QWidget):

    def __init__(self, parent=None):
        super(Cormix_Debug, self).__init__()
        self.parent = parent

        # from ui_cormix.ui_main import Ui_Main
        # self.ui = Ui_Main()
        # self.ui.setupUi(self)
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/ui_cormix/debug.ui"
        loadUi(filepath, self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Cormix_Debug()
    w.show()
    app.exec()