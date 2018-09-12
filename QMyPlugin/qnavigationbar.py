import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QHNavigationBar(QWidget):
    '''
    导航栏控件 横式
    1. 将 qcurrentItemChanged(int) 信号连接到槽函数
    2. 背景色, 前景色, 选中背景色, 选中前景色可修改 
    '''

    # 自定义信号, 当前选中项改变时发出
    qcurrentItemChanged = pyqtSignal(int)

    def __init__(self, items = [], parent = None):
        super(QHNavigationBar, self).__init__()
        self.parent = parent

        # [1] 初始化全局变量
        self.index = 0
        self.columnWidth  = 80

        self.color_back = "#E4E4E4"
        self.color_fore = "#202020"

        self.color_back_selected = "#2CA7F8"
        self.color_fore_selected = "#FFFFFF"
        
        # [2] 初始化Ui
        self.setupUi()

        # [3] 重载的构造参数
        self.items = items

    ''' 私有方法 '''
    def setupUi(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        self.setFixedHeight(30)

    def paintEvent(self, event):
        event.accept()

        # [1] 反走样
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # [2] 绘制整个背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color_back))
        painter.drawRect(self.rect())

        # [3] 绘制items
        count = 0
        for str in self.items:
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(count * self.columnWidth, 0, self.columnWidth, self.height()))

            if self.index == count:
                painter.setPen(QColor(self.color_fore_selected))
                painter.fillPath(itemPath, QColor(self.color_back_selected))
            else:
                painter.setPen(QColor(self.color_fore))
                painter.fillPath(itemPath, QColor(self.color_back))

            painter.drawText(QRect(count*self.columnWidth, 0, self.columnWidth, self.height()), Qt.AlignVCenter | Qt.AlignHCenter, str)
            count = count + 1

    def mousePressEvent(self, event):
        if event.x() / self.columnWidth < len(self.items):
            self.index = int(event.x() / self.columnWidth)
            self.qcurrentItemChanged.emit(self.index)
            self.update()

    ''' 公开方法 '''
    # 添加Item
    def addItem(self, item):
        self.items.append(item)
        self.update() 

    # 设置控件高度
    def setHeight(self, height):
        if self.height != height:
            self.setFixedHeight(height)
            self.update()

    # 设置列宽
    def setColumnWidth(self, columnWidth):
        if self.columnWidth != columnWidth:
            self.columnWidth = columnWidth
            self.update()

    # 设置背景色
    def setBackColor(self, color):
        if self.color_back != color: 
            self.color_back = color
            self.update()
        
    # 设置前景色
    def setForeColor(self, color):
        if self.color_fore != color: 
            self.color_fore = color
            self.update()
        
    # 设置选中背景色
    def setSelectedBackColor(self, color):
        if self.color_back_selected !=  color: 
            self.color_back_selected = color
            self.update()
        
    # 设置选中前景色
    def setSelectedForeColor(self, color):
        if self.color_fore_selected != color: 
            self.color_fore_selected = color
            self.update()

class QVNavigationBar(QWidget):
    '''
    导航栏控件 竖式
    1. 将 qcurrentItemChanged(int) 信号连接到槽函数
    2. 背景色, 前景色, 选中背景色, 选中前景色可修改 
    '''

    # 自定义信号, 当前选中项改变时发出
    qcurrentItemChanged = pyqtSignal(int)

    def __init__(self, items = [],  parent = None):
        super(QVNavigationBar, self).__init__()
        self.parent = parent

        # [1] 初始化全局变量
        self.index = 0
        self.rowHeight  = 40

        self.color_back = "#E4E4E4"
        self.color_fore = "#202020"

        self.color_back_selected = "#2CA7F8"
        self.color_fore_selected = "#FFFFFF"
        
        # [2] 初始化Ui
        self.setupUi()

        # [3] 重载的构造参数
        self.items = items

    ''' 私有方法 '''
    def setupUi(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        self.setFixedWidth(120)

    def paintEvent(self, event):
        event.accept()

        # [1] 反走样
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # [2] 绘制整个背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color_back))
        painter.drawRect(self.rect())

        # [3] 绘制items
        count = 0
        for str in self.items:
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, count * self.rowHeight, self.width(), self.rowHeight))

            if self.index == count:
                painter.setPen(QColor(self.color_fore_selected))
                painter.fillPath(itemPath, QColor(self.color_back_selected))
            else:
                painter.setPen(QColor(self.color_fore))
                painter.fillPath(itemPath, QColor(self.color_back))

            painter.drawText(QRect(0, count * self.rowHeight, self.width(), self.rowHeight), Qt.AlignVCenter | Qt.AlignHCenter, str)
            count = count + 1

    def mousePressEvent(self, event):
        if event.y() / self.rowHeight < len(self.items):
            self.index = int(event.y() / self.rowHeight)
            self.qcurrentItemChanged.emit(self.index)
            self.update()

    ''' 公开方法 '''
    # 添加Item
    def addItem(self, item):
        self.items.append(item)
        self.update() 

    # 设置控件宽度
    def setWidth(self, width):
        if self.width != width:
            self.setFixedWidth(width)
            self.update()

    # 设置行高
    def setRowHeight(self, rowHeight):
        if self.rowHeight != rowHeight:
            self.rowHeight = rowHeight
            self.update()

    # 设置背景色
    def setBackColor(self, color):
        if self.color_back != color: 
            self.color_back = color
            self.update()
        
    # 设置前景色
    def setForeColor(self, color):
        if self.color_fore != color: 
            self.color_fore = color
            self.update()
        
    # 设置选中背景色
    def setSelectedBackColor(self, color):
        if self.color_back_selected !=  color: 
            self.color_back_selected = color
            self.update()
        
    # 设置选中前景色
    def setSelectedForeColor(self, color):
        if self.color_fore_selected != color: 
            self.color_fore_selected = color
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QVNavigationBar(["ss", "aa"])
    w.show()
    app.exec()