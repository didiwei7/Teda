import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/QMyPlugin")

from QMyPlugin.qnavigationbar import *
from qsocket import *
from qserial import *

class ComDebug(QWidget):

    def __init__(self, parent=None):
        super(ComDebug, self).__init__()
        self.parent = parent

        self.vnavigationbar = QVNavigationBar(["Socket", "Serial"])
        self.stackedWidget = QStackedWidget()

        self.w_socket = QSocket()
        self.w_serial = QSerial()

        self.setupUi()
        self.setConnect()

    ''' 私有方法 '''
    def setupUi(self):
        self.vnavigationbar.setSelectedBackColor("#FFC0CB");
        self.vnavigationbar.setRowHeight(30);
        self.vnavigationbar.setWidth(80);

        layout_1 = QHBoxLayout()
        layout_2_1 = QHBoxLayout()
        layout_2_2 = QHBoxLayout()
        widget_1 = QWidget()
        widget_2 = QWidget()

        layout_2_1.addWidget(self.w_socket)
        layout_2_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        widget_1.setLayout(layout_2_1)

        layout_2_2.addWidget(self.w_serial)
        layout_2_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        widget_2.setLayout(layout_2_2)

        self.stackedWidget.insertWidget(0, widget_1)
        self.stackedWidget.insertWidget(1, widget_2)

        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_1.addWidget(self.vnavigationbar)
        layout_1.addWidget(self.stackedWidget)

        self.setLayout(layout_1)

    def setConnect(self):
        self.vnavigationbar.qcurrentItemChanged.connect(self.stackedWidget.setCurrentIndex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ComDebug()
    w.show()
    app.exec()