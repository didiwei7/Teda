import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/QMyPlugin")
from qex import *

class ComShow(QWidget):

    def __init__(self, parent=None):
        super(ComShow, self).__init__()
        self.parent = parent

        self.label_title1 = QLabel("发送消息记录")
        self.label_title2 = QLabel("接收消息记录")

        self.text_send = QTextBrowser()
        self.text_rcv = QTextBrowser()

        self.label_config = QLabel()
        self.btn_clearSend = QPushButton("清空发送")
        self.btn_clearRcv = QPushButton("清空接收")

        self.setupUi()
        self.setConnect()

    ''' 私有方法 '''
    def setupUi(self):
        self.label_title1.setFont(QFont("MicroSoft Yahei", 15, QFont.Bold))
        self.label_title2.setFont(QFont("MicroSoft Yahei", 15, QFont.Bold))

        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/settings.ini"
        if not QFileInfo(filepath).isFile():
            return
        else:
            setting = QSettings(filepath, QSettings.IniFormat)
            name = setting.value("SerialPort/portName")
            baud = setting.value("SerialPort/baudRate")
            data = setting.value("SerialPort/dataBits")
            parity = setting.value("SerialPort/parity")
            stop = setting.value("SerialPort/stopBits")
            flow = setting.value("SerialPort/flowCtrl")
            str_config = ("串口信息\n"
                          "端口:\t    {n}\n"
                          "波特率:\t    {b}\n"
                          "数据位:\t    {d}\n"
                          "校验位:\t    {p}\n"
                          "停止位:\t    {s}\n"
                          "流控:\t    {f}\n").format(n=name, b=baud, d=data, p=parity, s=stop, f=flow)
            self.label_config.setObjectName("config")
            self.label_config.setFont(QFont("MicroSoft Yahei", 8))
            self.label_config.setText(str_config)

        btn_style = ( "QPushButton { border-radius: 3px;\n"
                            "border: none;\n"
                            "width:  60px;\n"
                            "height: 20px;\n"
                            "background: #78AADC;\n"
                            "color: white;}\n"
                "QPushButton:hover { background: #9AC0CD; }\n"
                "QPushButton:pressed { background: #007ACC; }")
        
        self.btn_clearRcv.setStyleSheet(btn_style)
        self.btn_clearSend.setStyleSheet(btn_style)

        layout_1 = QHBoxLayout()
        layout_2_1 = QVBoxLayout()
        layout_2_2 = QVBoxLayout()
        layout_2_3 = QVBoxLayout()
 
        layout_2_1.addWidget(self.label_title1)
        layout_2_1.addWidget(self.text_send)

        layout_2_2.addWidget(self.label_title2)
        layout_2_2.addWidget(self.text_rcv)

        layout_2_3.addWidget(self.label_config)
        layout_2_3.addWidget(self.btn_clearSend)
        layout_2_3.addWidget(self.btn_clearRcv)
        layout_2_3.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout_1.addLayout(layout_2_1)
        layout_1.addLayout(layout_2_2)
        layout_1.addLayout(layout_2_3)

        self.setLayout(layout_1)

    def setConnect(self):
        self.btn_clearSend.clicked.connect(self.text_send.clear)
        self.btn_clearRcv.clicked.connect(self.text_rcv.clear)

    ''' 槽函数 外部 '''
    def on_append_sendmsg(self, msg):
        str_msg = GetCurrentTime() + "  " + msg
        self.text_send.append(str_msg)
    
    def on_append_rcvmsg(self, msg):
        str_msg = GetCurrentTime() + "  " + msg
        self.text_rcv.append(str_msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ComShow()
    w.show()
    app.exec()