import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QMyEdit(QWidget):
    '''
    组合控件
    说明 + 编辑框 + 单位 + 确认修改按钮
    '''

    qclicked = pyqtSignal()

    def __init__(self, name="", value=0.0, unit="", precision=1, parent=None):
        super(QMyEdit, self).__init__()
        self.parent = parent

        self.label_name = QLabel()
        self.edit_value = QLineEdit()
        self.label_unit = QLabel()
        self.btn_change = QPushButton("修改")

        self.precision = 1
        self.value = 0.0

        self.setupUi()
        self.setConnect()

        self.setName(name)
        self.setValue(value)
        self.setUnit(unit)
        self.setPrecision(precision)

    ''' 私有方法 '''
    def setupUi(self):
        # [1] 初始化
        self.label_name.setFont(QFont("MicroSoft Yahei", 9))
        self.label_name.setFixedSize(90, 20)
        self.label_name.setAlignment(Qt.AlignRight)

        self.edit_value.setFont(QFont("MicroSoft Yahei", 9))
        self.edit_value.setValidator(QDoubleValidator(-1, 0, self.precision))
        self.edit_value.setAlignment(Qt.AlignRight)

        self.label_unit.setFont(QFont("MicroSoft Yahei", 9))
        self.label_unit.setFixedSize(40, 20)
        self.label_unit.setAlignment(Qt.AlignLeft)

        # [2] 布局
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_1.addWidget(self.label_name)
        layout_1.addSpacing(10)
        layout_1.addWidget(self.edit_value)
        layout_1.addSpacing(10)
        layout_1.addWidget(self.label_unit)
        layout_1.addWidget(self.btn_change)

        self.setLayout(layout_1)

        # [3] 载入样式表
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/qmyedit.qss"
        with open(filepath, "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())

        # [4] 窗口属性
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFixedSize(260, 20)

    def setConnect(self):
        self.btn_change.clicked.connect(self.on_btn_change)

    ''' 公开方法 '''
    def setName(self, name):
        if self.label_name.text() != name:
            self.label_name.setText(name)
            self.update()

    def setValue(self, value):
        self.value = value
        if self.edit_value.text() == "":
            self.edit_value.setText(str(round(value, self.precision)))
            self.update()
        else:
            if round(float(self.edit_value.text()), self.precision) != value:
                self.edit_value.setText(float2str(self.value, self.precision))
                self.update()

    def setUnit(self, unit):
        if self.label_unit.text() != unit:
            self.label_unit.setText(unit)
            self.update()

    def setPrecision(self, precision):
        if self.precision != precision:
            if self.edit_value.text() == "":
                self.precision = precision
                self.edit_value.setValidator(QDoubleValidator(-1, 0, self.precision))
                self.update()
            else:
                self.precision = precision
                self.edit_value.setValidator(
                    QDoubleValidator(-1, 0, self.precision))
                self.edit_value.setText(float2str(self.value, self.precision))
                self.update()

    def getName(self):
        return self.label_name.text()

    def getValue(self):
        if self.edit_value.text() == "":
            return 0
        else:
            return round(float(self.edit_value.text()), self.precision)

    def getUnit(self):
        return self.label_unit.text()

    ''' 槽函数 私有 '''
    def on_btn_change(self):
        self.qclicked.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMyEdit("xx", 50.364, "u")
    w.show()
    app.exec()
