import os
import sys
import json

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/QMyPlugin")

from qio import *

class IODebug(QWidget):

    qsendmsg_out_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(IODebug, self).__init__()
        self.parent = parent

        self.layout_1 = QHBoxLayout()
        self.layout_2_1 = QVBoxLayout()
        self.layout_2_2 = QVBoxLayout()

        self.dict_io = {}

        self.INPUT = [None] * 10
        self.OUTPUT = [None] * 10
        self.list_outmsg = [None] * 10

        self.setupUi()
        self.setConnect()

    ''' 私有方法 '''
    def setupUi(self):
        # [1] 读配置到字典
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/io.json"
        with open(filepath, 'r', encoding = "utf-8") as file:
            self.dict_io = json.load(file)

        # [2] 初始化控件
        self.setInput()
        self.setOutput()

        # [3] 布局
        self.layout_1.addLayout(self.layout_2_1)
        self.layout_1.addSpacing(100)
        self.layout_1.addLayout(self.layout_2_2)
        self.layout_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.setLayout(self.layout_1)

        # [4] 初始化发送消息
        self.setOutMsg()

    def setInput(self):
        label_title = QLabel("通用输入:")
        label_title.setFont(QFont("MicroSoft Yahei", 15, QFont.Bold))

        self.layout_2_1.addWidget(label_title)
        self.layout_2_1.addSpacing(10)

        for key in self.dict_io["Input"].keys():
            name = self.dict_io["Input"][key]["name"]
            status = self.dict_io["Input"][key]["status"]
            visible = self.dict_io["Input"][key]["visible"]
            self.INPUT[int(key)] = QInputLabel(name, status)
            self.INPUT[int(key)].setObjectName("INPUT" + key)
            self.INPUT[int(key)].setVisible(visible)
            self.layout_2_1.addWidget(self.INPUT[int(key)])

        self.layout_2_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def setOutput(self):
        label_title = QLabel("通用输出:")
        label_title.setFont(QFont("MicroSoft Yahei", 15, QFont.Bold))

        self.layout_2_2.addWidget(label_title)
        self.layout_2_2.addSpacing(10)

        for key in self.dict_io["Output"].keys():
            name = self.dict_io["Output"][key]["name"]
            status = self.dict_io["Output"][key]["status"]
            visible = self.dict_io["Output"][key]["visible"]
            self.OUTPUT[int(key)] = QOutputButton(name, status)
            self.OUTPUT[int(key)].setObjectName("OUTPUT" + key)
            self.OUTPUT[int(key)].setVisible(visible)
            self.layout_2_2.addWidget(self.OUTPUT[int(key)])

        self.layout_2_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def setOutMsg(self):
        for key in self.dict_io["OutMsg"].keys():
            self.list_outmsg[int(key)] = self.dict_io["OutMsg"][key]

    def setConnect(self):
        for i in range(10):
            self.OUTPUT[i].qclicked.connect(self.on_btn_output)

    ''' 槽函数 内部 '''
    def on_btn_output(self):
        outName = QOutputButton().sender().objectName()
        for i in range(10):
            if outName == "OUTPUT" + str(i):
                self.qsendmsg_out_clicked.emit(self.list_outmsg[i])
            
    ''' 槽函数 外部'''
    def on_set_in_status(self, index, status):
        self.INPUT[index].setStatus(status)

    def on_set_out_status(self, index, status):
        self.OUTPUT[index].setStatus(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = IODebug()
    w.show()
    app.exec()
