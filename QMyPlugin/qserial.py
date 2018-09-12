import os
import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *

from qex import *

class QSerial(QWidget):
    '''
    串口调试助手
    可直接在项目中引用
    '''

    def __init__(self, parent = None):
        super(QSerial, self).__init__()
        self.parent = parent

        self.slist_port = []
        self.slist_baud = ["9600", "19200", "38400", "115200"]
        self.slist_data = ["5", "6", "7", "8"]
        self.slist_parity = ["None", "Even", "Odd", "Space", "Mask"]
        self.slist_stop = ["1", "1.5", "2"]
        self.slist_flow = ["None", "Hardware", "Software"]

        self.label_port = QLabel("串 口")
        self.label_baud = QLabel("波特率")
        self.label_data = QLabel("数据位")
        self.label_parity = QLabel("校验位")
        self.label_stop = QLabel("停止位")
        self.label_flow = QLabel("流 控")

        self.combo_port = QComboBox()
        self.combo_baud = QComboBox()
        self.combo_data = QComboBox()
        self.combo_parity = QComboBox()
        self.combo_stop = QComboBox()
        self.combo_flow = QComboBox()

        self.btn_start = QPushButton("启动")
        self.btn_close = QPushButton("关闭")

        self.text_msg = QTextBrowser()
        self.edit_msg = QTextEdit()

        self.check_hex_rcv = QCheckBox("16进制接受")
        self.check_hex_send = QCheckBox("16进制发送")
        self.check_clear = QCheckBox("发送后清空")
        self.btn_send = QPushButton("发送")

        self.serial = QSerialPort()

        self.setupUi()
        self.setConnect()

    ''' 私有方法 '''
    def setupUi(self):
        # [1] 布局
        layout_1 = QVBoxLayout()
        layout_2_1 = QHBoxLayout()
        layout_2_2 = QHBoxLayout()
        layout_2_3 = QHBoxLayout()
        layout_3_1 = QGridLayout()
        layout_3_2 = QVBoxLayout()

        layout_3_1.addWidget(self.label_port, 0, 0)
        layout_3_1.addWidget(self.label_baud, 1, 0)
        layout_3_1.addWidget(self.label_data, 2, 0)
        layout_3_1.addWidget(self.label_parity, 3, 0)
        layout_3_1.addWidget(self.label_stop, 4, 0)
        layout_3_1.addWidget(self.label_flow, 5, 0)
        
        layout_3_1.addWidget(self.combo_port, 0, 1)
        layout_3_1.addWidget(self.combo_baud, 1, 1)
        layout_3_1.addWidget(self.combo_data, 2, 1)
        layout_3_1.addWidget(self.combo_parity, 3, 1)
        layout_3_1.addWidget(self.combo_stop, 4, 1)
        layout_3_1.addWidget(self.combo_flow, 5, 1)
        
        layout_3_2.addWidget(self.check_hex_rcv)
        layout_3_2.addWidget(self.check_hex_send)
        layout_3_2.addWidget(self.check_clear)
        layout_3_2.addWidget(self.btn_send)

        layout_2_1.addLayout(layout_3_1)
        layout_2_1.addWidget(self.btn_start)
        layout_2_1.addWidget(self.btn_close)
        layout_2_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout_2_2.addWidget(self.edit_msg)
        layout_2_2.addLayout(layout_3_2)

        layout_1.addLayout(layout_2_1)
        layout_1.addWidget(self.text_msg)
        layout_1.addLayout(layout_2_2)
        layout_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout_1)

        # [2] 初始化ComboBox
        for item in QSerialPortInfo.availablePorts():
            self.slist_port.append(item.portName())

        self.combo_port.addItems(self.slist_port)
        self.combo_baud.addItems(self.slist_baud)
        self.combo_data.addItems(self.slist_data)
        self.combo_parity.addItems(self.slist_parity)
        self.combo_stop.addItems(self.slist_stop)
        self.combo_flow.addItems(self.slist_flow)

        self.combo_data.setCurrentIndex(3)

        # [3] 初始化按钮状态
        self.btn_close.setEnabled(False)
        self.btn_send.setEnabled(False)

        # [4] 美化
        self.edit_msg.setFixedHeight(100)
        self.text_msg.setFixedHeight(250)
        self.text_msg.setFont(QFont("MicroSoft Yahei", 8))

        # [5] Check
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/qserial.ini"
        if not QFileInfo(filepath).isFile():
            return
        else:
            setting = QSettings(filepath, QSettings.IniFormat)
            self.check_hex_rcv.setChecked(str2bool(setting.value("checked/check_hex_rcv")))
            self.check_hex_send.setChecked(str2bool(setting.value("checked/check_hex_send")))
            self.check_clear.setChecked(str2bool(setting.value("checked/check_clear")))

    def setConnect(self):
        self.btn_start.clicked.connect(self.on_btn_start)
        self.btn_close.clicked.connect(self.on_btn_close)
        self.btn_send.clicked.connect(self.on_btn_send)

        self.check_hex_rcv.clicked.connect(self.on_check_changed)
        self.check_hex_send.clicked.connect(self.on_check_changed)
        self.check_clear.clicked.connect(self.on_check_changed)

        self.serial.readyRead.connect(self.on_serial_receive)

    ''' 槽函数 内部 '''    
    # 启动
    def on_btn_start(self):
        self.serial.setPortName(self.combo_port.currentText())
        
        if self.serial.open(QIODevice.ReadWrite) == False: return
        self.serial.setBaudRate(int(self.combo_baud.currentText()))
        self.serial.setDataBits(GetDatabits(self.combo_data.currentText()))
        self.serial.setParity(GetParity(self.combo_parity.currentText()))
        self.serial.setStopBits(GetStopBits(self.combo_stop.currentText()))
        self.serial.setFlowControl(GetFlowControl(self.combo_flow.currentText()))

        self.btn_start.setEnabled(False)
        self.btn_close.setEnabled(True)
        self.btn_send.setEnabled(True)

    # 关闭
    def on_btn_close(self):
        self.serial.close()
        self.btn_start.setEnabled(True)
        self.btn_close.setEnabled(False)
        self.btn_send.setEnabled(False)

    # 发送
    def on_btn_send(self):
        # [1] 获取编辑框数据
        str_msg = self.edit_msg.toPlainText()
        if str_msg == "": return

        # [2] 发送
        if self.check_hex_send.isChecked():
            bytes_msg = Hexstring2Bytes(str_msg)
            self.serial.write(bytes_msg)
        else:
            bytes_msg = str_msg.encode()
            self.serial.write(bytes_msg)

        # [3] 清空
        if self.check_clear.isChecked():
            self.edit_msg.clear()

    # 接收
    def on_serial_receive(self):
        rcvData = self.serial.read(1024)
        if rcvData == b'': return
        if self.check_hex_rcv.isChecked():
            str_rcvData = Bytes2Hexstring(rcvData)
            self.text_msg.append(GetCurrentTime() + "  " + str_rcvData)
        else:
            str_rcvData = rcvData.decode()
            self.text_msg.append(GetCurrentTime() + "  " + str_rcvData)

    # Check按钮
    def on_check_changed(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/qserial.ini"
        if not QFileInfo(filepath).isFile():
            return
        else:
            setting = QSettings(filepath, QSettings.IniFormat)
            setting.beginGroup("checked")
            setting.setValue("check_hex_rcv", self.check_hex_rcv.isChecked())
            setting.setValue("check_hex_send", self.check_hex_send.isChecked())
            setting.setValue("check_clear", self.check_clear.isChecked())         
            setting.endGroup()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QSerial()
    ex.show()
    app.exec()