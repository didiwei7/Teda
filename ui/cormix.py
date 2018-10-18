import os
import sys
import time
import threading

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/QMyPlugin")

from QMyPlugin.qnavigationbar import *

from cormix_main import *
from cormix_debug import *

class Cormix(QWidget):

    def __init__(self, parent = None):
        super(Cormix, self).__init__()
        self.parent = parent

        # 窗口
        self.vnavigationbar = QVNavigationBar(["主界面", "调试"])
        self.stackedWidget = QStackedWidget()
        self.w_main = Cormix_Main()
        self.w_debug = Cormix_Debug()

        self.setupUi()
        self.setConnect()

    def setupUi(self):
        # 初始化导航栏
        self.vnavigationbar.setSelectedBackColor("#FFC0CB")
        self.vnavigationbar.setRowHeight(30)
        self.vnavigationbar.setWidth(80)

        self.stackedWidget.insertWidget(0, self.w_main)
        self.stackedWidget.insertWidget(1, self.w_debug)

        # 布局
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_1.addWidget(self.vnavigationbar)
        layout_1.addWidget(self.stackedWidget)
        self.setLayout(layout_1)

    def setConnect(self):
        self.vnavigationbar.qcurrentItemChanged.connect(self.stackedWidget.setCurrentIndex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Cormix()
    w.show()
    app.exec()       