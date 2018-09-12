import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

from qex import *

class QTrackBar(QWidget):
    '''
    刻度条(带刻度的进度条)
    '''

    def __init__(self, name = "", value = 0.0, unit = "", minValue = 0, maxValue = 200, precisionRuler = 0, precisionTitle = 1, parent = None):
        super(QTrackBar, self).__init__()
        self.parent = parent

        self.name = ""
        self.unit = ""

        self.maxValue = 100
        self.minValue = 0
        self.value = 0.0

        self.precisionRuler = 0     # 小数点保留几位
        self.precisionTitle = 1     

        self.longStep = 10          # 长线条等分步长
        self.shortStep = 1          # 短线条等分步长    
        self.space_top = 20         
        self.space_bottom = 20
        self.space_left = 30
        self.space_right = 30

        self.color_line = QColor(255, 255, 255)
        self.color_title = QColor(0, 255, 0)
        
        self.color_back_start = QColor(100, 100, 100)
        self.color_back_end = QColor(60, 60, 60)
        
        self.color_back_bar = QColor(220, 220, 220)
        self.color_fore_bar = QColor(100, 184, 255)

        self.setupUi()

        self.setName(name)
        self.setValue(value)
        self.setUnit(unit)
        self.setRange(minValue, maxValue)
        self.setPrecisionRuler(precisionRuler)
        self.setPrecisionTitle(precisionTitle)

    ''' 私有方法 '''
    def setupUi(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setFont(QFont("MicroSoft Yahei", 8))
        self.setFixedSize(120, 350)

    def paintEvent(self, event):
        event.accept()

        # 反走样
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        #  绘制背景
        self.drawBack(painter)
        # 绘制标题栏
        self.drawTitle(painter)
        # 绘制标尺
        self.drawRuler(painter)
        # 绘制柱状条背景
        self.drawBarBack(painter)
        # 绘制柱状条前景
        self.drawBarFore(painter)

    def drawBack(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)
        lg = QLinearGradient(QPointF(0, 0), QPointF(0, self.height()))
        lg.setColorAt(0.0, self.color_back_start)
        lg.setColorAt(1.0, self.color_back_end)
        painter.setBrush(lg)
        painter.drawRect(self.rect())
        painter.restore()

    def drawTitle(self, painter):
        painter.save()
        painter.setPen(self.color_title)
        
        point_name = QPointF(10, self.space_top)
        painter.drawText(point_name, self.name)

        str_title = float2str(self.value, self.precisionTitle) + " " + self.unit
        fontWidth = painter.fontMetrics().width(str_title)
        pointValue = QPointF(self.width() - fontWidth - 10, self.space_top)
        painter.drawText(pointValue, str_title)
        painter.restore()

    def drawRuler(self, painter):
        painter.save()
        painter.setPen(QColor(self.color_line))
        initX = self.space_left + 20
        initY = self.space_top + 20

        pointTop = QPointF(initX, initY)
        pointBtm = QPointF(initX, self.height() - self.space_bottom)
        painter.drawLine(pointTop, pointBtm)

        length = self.height() - self.space_bottom - initY
        increment = length / (self.maxValue - self.minValue)

        longLineLength = 10
        shortLineLength = 7

        for num in range(self.maxValue, self.minValue-1, -self.shortStep):
            if num % self.longStep == 0 or num == self.minValue:
                pointLeft = QPointF(initX, initY)
                pointRight = QPointF(initX + longLineLength, initY)
                painter.drawLine(pointLeft, pointRight)

                str_num = float2str(num, self.precisionRuler)
                fontWidth = painter.fontMetrics().width(str_num)
                fontHeight = painter.fontMetrics().height()
                pointText = QPointF(initX - fontWidth - 5, initY + fontHeight / 3)
                painter.drawText(pointText, str_num);
            else:
                if num % (self.longStep / 2) == 0:
                    shortLineLength =7
                else:
                    shortLineLength = 4   

                pointLeft = QPointF(initX, initY)
                pointRight = QPointF(initX + shortLineLength, initY)
                painter.drawLine(pointLeft, pointRight)

            initY += increment * self.shortStep

        painter.restore()

    def drawBarBack(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        initX = self.space_left + 20 + 20
        pointLeftTop = QPointF(initX, self.space_top + 20)
        pointRightBtm = QPointF(self.width() - self.space_right, self.height() - self.space_bottom)
        rectBack = QRectF(pointLeftTop, pointRightBtm)

        painter.setBrush(self.color_back_bar)
        painter.drawRect(rectBack)

        painter.restore()

    def drawBarFore(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        height_back = self.height() - self.space_bottom -self.space_top -20
        
        increment = height_back / (self.maxValue - self.minValue)
        height_select = (self.value - self.minValue) * increment

        pointLeftTop =  QPointF(self.space_left + 20 + 20, self.height() - self.space_bottom - height_select )
        pointRightBtm = QPointF(self.width() - self.space_right, self.height() - self.space_bottom)
        rectFore = QRectF(pointLeftTop, pointRightBtm)

        painter.setBrush(self.color_fore_bar)
        painter.drawRect(rectFore)

        painter.restore()

    '''公开方法'''
    # 设置名称
    def setName(self, name):
        if self.name != name:
            self.name = name
            self.update()

    # 设置值
    def setValue(self, value):
        if value > self.maxValue: return
        if self.value != value:
            self.value = value
            self.update()

    # 设置单位
    def setUnit(self, unit):
        if self.unit != unit:
            self.unit = unit
            self.update()

    # 设置范围
    def setRange(self, minValue, maxValue):
        if minValue >= maxValue: return
        if self.minValue != minValue or self.maxValue != maxValue:
            self.minValue = minValue
            self.maxValue = maxValue
            self.update()

    # 设置最小值
    def setMinValue(self, minValue):
        if minValue >= self.maxValue: return
        if self.minValue != minValue:
            self.minValue = minValue
            self.update()

    # 设置最大值
    def setMaxValue(self, maxValue):
        if maxValue <= self.minValue: return
        if self.maxValue != maxValue:
            self.maxValue = maxValue
            self.update()

    # 设置刻度值文本的小数点位数
    def setPrecisionRuler(self, precision):
        if precision > 3: return
        if self.precisionRuler != precision:
            self.precisionRuler = precision
            self.update()

    # 设置标题值文本的小数点位数
    def setPrecisionTitle(self, precision):
        if precision > 5: return
        if self.precisionTitle != precision:
            self.precisionTitle = precision
            self.update()

    # 设置刻度长步长
    def setLongStep(self, step):
        if self.longStep != step:
            self.longStep = step
            self.update()
        
    # 设置刻度短步长
    def setShortStep(self, step):
        if self.shortStep != step:
            self.shortStep = step
            self.update()

    # 设置刻度值文本颜色
    def setLineColor(self, color):
        if self.color_line != color:
            self.color_line = color
            self.update()

    # 设置标题文本颜色
    def setTitleColor(self, color):
        if self.color_title != color:
            self.color_title = color
            self.update()

    # 设置背景颜色渐变开始
    def setBackColorStart(self, color):
        if self.color_back_start != color:
            self.color_back_start = color
            self.update()

    # 设置背景颜色渐变结束
    def setBackColorEnd(self, color):
        if self.color_back_end != color:
            self.color_back_end = color
            self.update()

    # 设置条状背景颜色
    def setBarBackColor(self, color):
        if self.color_back_bar != color:
            self.color_back_bar = color
            self.update()

    #  设置条状前景颜色
    def setBarForeColor(self, color):
        if self.color_fore_bar != color:
            self.color_fore_bar = color
            self.update()

    # 获取数值
    def getValue(self):
        return self.value

    # 获取最小值
    def getMinValue(self):
        return self.minValue

    # 获取最大值
    def getMaxValue(self):
        return self.maxValue


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QTrackBar("xx", 50.365, "℃")
    w.setLongStep(20)
    w.setShortStep(2)
    w.show()
    app.exec()