import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QInput(QWidget):
    '''
    IO灯
    1. 信号灯，设置获取状态 
    '''

    def __init__(self, status=0, parent=None):
        super(QInput, self).__init__()
        self.parent = parent

        self.status = 0

        self.setupUi()
        self.setStatus(status)

    ''' 私有方法 '''
    def setupUi(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        event.accept()

        # [1] 反走样
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # [2] 中心坐标移到正中心
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.transparent)

        # [3] 背景填充
        painter.fillRect(-self.width(), -self.height(),
                         self.width() * 2, self.height() * 2, Qt.transparent)

        # [4] 外边框
        radius = 8
        lg1 = QLinearGradient(0, -radius, 0, radius)
        lg1.setColorAt(0, QColor(240, 240, 240))
        lg1.setColorAt(1, QColor(150, 150, 150))
        painter.setBrush(lg1)
        painter.drawEllipse(-radius, -radius, radius << 1, radius << 1)

        # [5] 内边框
        radius -= 2
        lg2 = QLinearGradient(0, -radius, 0, radius)
        lg2.setColorAt(0, QColor(120, 120, 120))
        lg2.setColorAt(1, QColor(160, 160, 160))
        painter.setBrush(lg2)
        painter.drawEllipse(-radius, -radius, radius << 1, radius << 1)

        # [6] 状态
        if self.status == 1:
            radius -= 1
            rg = QRadialGradient(0, 0, radius)
            rg.setColorAt(0,   QColor(0, 245, 0))
            rg.setColorAt(0.6, QColor(0, 210, 0))
            rg.setColorAt(1,   QColor(0, 166, 0))
            painter.setBrush(rg)
            painter.drawEllipse(-radius, -radius, radius << 1, radius << 1)

    ''' 公开方法 '''
    # 设置状态
    def setStatus(self, status):
        if self.status != status:
            self.status = status
            self.update()

    # 获取状态
    def getStatus(self):
        return self.status

    # 设置控件Szie
    def setSize(self, width, height):
        if self.width != width or self.height != height:
            self.setFixedSize(width, height)
            self.update()

class QInputLabel(QWidget):
    '''
    输入灯
    1. 输入灯, 文本 + 灯, 
    2. 设置获取状态 
    '''

    def __init__(self, name="", status=0, parent=None):
        super(QInputLabel, self).__init__()
        self.parent = parent

        self.label_name = QLabel()
        self.label_status = QInput()

        self.setupUi()
        self.setName(name)
        self.setStatus(status)

    ''' 私有方法 '''
    def setupUi(self):
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setStyleSheet("background-color: rgb(230, 230, 230); border-radius:5px;")
            
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(1)
        layout_1.addWidget(self.label_name)
        layout_1.addWidget(self.label_status)
        self.setLayout(layout_1)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFixedSize(150, 20)

    ''' 公开方法 '''
    def setName(self, name):
        if self.label_name.text() != name:
            self.label_name.setText(name)
            self.update()

    def setStatus(self, status):
        if self.label_status.getStatus() != status:
            self.label_status.setStatus(status)
            self.update()

class QOutputButton(QPushButton):

    qclicked = pyqtSignal()

    def __init__(self, name="", status=0, parent=None):
        super(QOutputButton, self).__init__()
        self.parent = parent

        self.status = 0

        self.setupUi()
        self.setConnect()

        self.setName(name)
        self.setStatus(status)

    ''' 私有方法 '''
    def setupUi(self):
        self.setStyleSheet("background-color: #D1D1D1; border-radius: 5px;")

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFixedSize(150, 20)

    def setConnect(self):
        self.clicked.connect(self.on_btn_clicked)

    ''' 公开方法 '''
    def setName(self, name):
        if self.text() != name:
            self.setText(name)
            self.update()

    def setStatus(self, status):
        if self.status != status:
            self.status = status
            if self.status <= 0:
                self.setStyleSheet("background-color: #D1D1D1; border-radius: 5px;")                    
            else:
                self.setStyleSheet("background-color: #5CACEE; border-radius: 5px; color: #eff0f1; ")     
            self.update()

    def getStatus(self):
        return self.status

    ''' 槽函数 内部 '''
    def on_btn_clicked(self):
        self.qclicked.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QOutputButton("xx", 1)
    w.show()
    app.exec()
