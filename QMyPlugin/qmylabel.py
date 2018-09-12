import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from qex import *

class QMyLabel(QWidget):
    '''
    组合控件
    说明 + 值显示 + 单位
    '''

    def __init__(self, name = "", value = 0.0, unit = "",precision = 1, parent = None):
        super(QMyLabel, self).__init__()
        self.parent = parent

        self.label_name = QLabel()
        self.label_value = QLabel()
        self.label_unit = QLabel()
        self.precision = 1
        self.value = 0.0

        self.setupUi()
        self.setName(name)
        self.setValue(value)
        self.setUnit(unit)
        self.setPrecision(precision)

    ''' 私有方法 '''
    def setupUi(self):
        self.label_name.setFont(QFont("MicroSoft Yahei", 9))
        self.label_name.setFixedSize(100, 20)
        self.label_name.setAlignment(Qt.AlignRight)

        self.label_value.setFont(QFont("MicroSoft Yahei", 9))
        self.label_value.setFixedSize(70, 20)
        self.label_value.setStyleSheet("color: #78AADC;")
        self.label_value.setAlignment(Qt.AlignRight)

        self.label_unit.setFont(QFont("MicroSoft Yahei", 9))
        self.label_unit.setFixedSize(40, 20)
        self.label_unit.setAlignment(Qt.AlignLeft)

        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_1.addWidget(self.label_name)
        layout_1.addWidget(self.label_value)
        layout_1.addSpacing(10)
        layout_1.addWidget(self.label_unit)

        self.setLayout(layout_1)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFixedSize(220, 20)
        
    ''' 公开方法 '''
    def setName(self, name):
        if self.label_name.text() != name:
            self.label_name.setText(name)
            self.update()

    def setValue(self, value):
        self.value = value
        if self.label_value.text() == "":
            self.label_value.setText(float2str(self.value, self.precision))
            self.update()
        else:
            if round(float(self.label_value.text()), self.precision) != value:
                self.label_value.setText(float2str(self.value, self.precision))
                self.update()

    def setUnit(self, unit):
        if self.label_unit.text() != unit:
            self.label_unit.setText(unit)
            self.update()

    def setPrecision(self, precision):
        if self.precision != precision:
            if self.label_value.text() == "":
                self.precision = precision
                self.update()
            else:       
                self.precision = precision
                self.label_value.setText(float2str(self.value, self.precision))
                self.update()

    def getName(self):
        return self.label_name.text()

    def getValue(self):
        if self.label_value.text() == "": 
            return 0
        else: 
            return round(float(self.label_value.text(), self.precision))

    def getUnit(self):
        return self.label_unit.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMyLabel("当前压力:", 50000.3563, "℃", 3)
    w.show()
    app.exec()