import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from qex import *

class QMySlider(QWidget):
    '''
    滑块控件 横式
    1. 名称 + 值 + 单位 + 控制条
    2. 将 qvalueChanged(int) 信号连接到槽函数
    3. 背景色, 前景色, 选中背景色, 选中前景色可修改 
    '''

    qvalueChanged = pyqtSignal(int)

    def __init__(self, name = "", value = 0, unit = "", minValue = 0, maxValue = 100, parent = None):
        super(QMySlider, self).__init__()
        self.parent = parent

        self.label_name = QLabel()
        self.label_value = QLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.unit = ""

        self.setupUi()
        self.setConnect()     
        self.setName(name)
        self.setValue(value)
        self.setUnit(unit)
        self.setRange(minValue, maxValue)
    
    ''' 私有方法 '''
    def setupUi(self):
        # [1] 布局
        layout_1 = QVBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)

        layout_2 = QHBoxLayout()
        layout_2.setContentsMargins(0, 0, 0, 0)
        layout_2.setSpacing(0)

        layout_2.addWidget(self.label_name)
        layout_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_2.addWidget(self.label_value)

        layout_1.addLayout(layout_2)
        layout_1.addWidget(self.slider)

        self.setLayout(layout_1)

        # [2] 载入样式表
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/qmyslider.qss"
        with open(filepath, "r", encoding = "utf-8") as file:
            self.setStyleSheet(file.read())

        # [3] 窗口属性
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFixedWidth(200)

    def setConnect(self):
        self.slider.valueChanged.connect(self.on_valueChanged)

    ''' 公开方法 '''
    # 设置控件名
    def setName(self, name):
        if self.label_name.text() != name:
            self.label_name.setText(name)
            self.update()

    # 设置当前值
    def setValue(self, value):
        if self.slider.value != value and self.slider.maximum() >= value :
            self.slider.setValue(value)
            self.label_value.setText(str(self.slider.value()) + " " + self.unit)
            self.update()

    # 设置单位
    def setUnit(self, unit):
        if self.unit != unit:
            self.unit = unit
            self.label_value.setText(str(self.slider.value()) + " " + self.unit)
            self.update()

    # 设置控件宽度
    def setWidth(self, width):
        if self.width != width:
            self.setFixedWidth(width)
            self.update()

    # 设置范围
    def setRange(self, minValue, maxValue):
        self.slider.setRange(minValue, maxValue)
        self.update()

    # 设置页步进
    def setPageStep(self, pageStep):
        self.slider.setPageStep(pageStep)
        self.update()

    # 获取当前值
    def getCurrentValue(self):
        return self.slider.value()

    ''' 槽函数 私有'''
    def on_valueChanged(self, value):
        self.label_value.setText(str(value) + " " + self.unit)
        self.qvalueChanged.emit(value)        
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMySlider("xx", 50, "u")
    w.show()
    app.exec()