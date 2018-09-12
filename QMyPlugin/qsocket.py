import os
import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

from qex import *

class QSocket(QWidget):
    ''' 
    Socket调试助手 
    '''

    def __init__(self, parent = None):
        super(QSocket, self).__init__()
        self.parent = parent

        self.label_ip = QLabel("IP:")
        self.edit_ip = QLineEdit()

        self.label_port = QLabel("Port：")
        self.edit_port = QLineEdit()

        self.radio_server = QRadioButton("服务器")
        self.radio_client = QRadioButton("客户端")

        self.btn_start = QPushButton("启动")
        self.btn_close = QPushButton("关闭")

        self.text_msg = QTextBrowser()
        self.edit_msg = QTextEdit()

        self.check_hex_rcv = QCheckBox("16进制接受")
        self.check_hex_send = QCheckBox("16进制发送")
        self.check_clear = QCheckBox("发送后清空")
        self.btn_send = QPushButton("发送")

        self.server = QTcpServer()
        self.socket = QTcpSocket()
        self.client = QTcpSocket()

        self.setupUi()
        self.setConnect()

    ''' 私有方法 '''
    def setupUi(self):
        # [1] 布局
        layout_1 = QVBoxLayout()
        layout_2_1 = QHBoxLayout()
        layout_2_2 = QHBoxLayout()
        layout_2_3 = QHBoxLayout()
        layout_3_1 = QVBoxLayout()

        layout_3_1.addWidget(self.check_hex_rcv)
        layout_3_1.addWidget(self.check_hex_send)
        layout_3_1.addWidget(self.check_clear)
        layout_3_1.addWidget(self.btn_send)

        layout_2_1.addWidget(self.label_ip)
        layout_2_1.addWidget(self.edit_ip)
        layout_2_1.addWidget(self.label_port)
        layout_2_1.addWidget(self.edit_port)

        layout_2_2.addWidget(self.radio_server)
        layout_2_2.addWidget(self.radio_client)
        layout_2_2.addWidget(self.btn_start)
        layout_2_2.addWidget(self.btn_close)

        layout_2_3.addWidget(self.edit_msg)
        layout_2_3.addLayout(layout_3_1)

        layout_1.addLayout(layout_2_1)
        layout_1.addLayout(layout_2_2)
        layout_1.addWidget(self.text_msg)
        layout_1.addLayout(layout_2_3)
        layout_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Maximum, QSizePolicy.Expanding))

        self.setLayout(layout_1)

        # [2] 初始化按钮状态
        self.radio_client.setChecked(True)
        self.btn_close.setEnabled(False)
        self.btn_send.setEnabled(False)

        # [3] 获取本地IP
        import socket
        name = socket.getfqdn(socket.gethostname())
        addr = socket.gethostbyname(name)
        self.edit_ip.setText(addr)
        self.edit_port.setText("6666")

        # [4] 美化
        self.edit_msg.setFixedHeight(100)
        self.text_msg.setFixedHeight(300)
        self.text_msg.setFont(QFont("MicroSoft Yahei", 8))

        # [5] Check
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/qsocket.ini"
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

        self.server.newConnection.connect(self.on_server_accept)
        self.client.readyRead.connect(self.on_client_receive)

    ''' 槽函数 内部 '''
    # 启动
    def on_btn_start(self):
        if self.radio_server.isChecked():
            # [1] 开始监听
            self.server.listen(QHostAddress.Any, int(self.edit_port.text()))
            if self.server.isListening():
                # [2] 界面状态更新
                self.btn_start.setEnabled(False)
                self.btn_close.setEnabled(True)
                self.btn_send.setEnabled(True)
                self.radio_client.setCheckable(False)
                self.text_msg.append(GetCurrentTime() + "  服务器已启动")
        
        else:
            # [1] 连接服务器
            self.client.connectToHost(self.edit_ip.text(), int(self.edit_port.text()))
            if self.client.waitForConnected(100):
                # [2] 界面状态更新
                self.btn_start.setEnabled(False)
                self.btn_close.setEnabled(True)
                self.btn_send.setEnabled(True)
                self.radio_server.setCheckable(False)
                self.text_msg.append(GetCurrentTime() + "  客户端已连接上服务器" + self.client.peerName())
            else:
                self.text_msg.append(GetCurrentTime() + "  连接服务器失败")

    # 关闭
    def on_btn_close(self):
        if self.radio_server.isChecked():
            # [1] 服务器关闭
            self.socket.abort()
            self.socket.close()
            self.server.close()

            # [2] 界面状态更新
            self.btn_start.setEnabled(True)
            self.btn_close.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.radio_server.setCheckable(True)
            self.radio_client.setCheckable(True)
            self.text_msg.append(GetCurrentTime() + "  服务器已关闭");

        else:
            # [1] 客户端关闭
            self.client.abort()
            self.client.close()

            # [2] 界面状态更新
            self.btn_start.setEnabled(True)
            self.btn_close.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.radio_server.setCheckable(True)
            self.radio_client.setCheckable(True)
            self.text_msg.append(GetCurrentTime() + "  客户端已断开");

    # 发送
    def on_btn_send(self):
        # [1] 获取编辑框数据
        str_msg = self.edit_msg.toPlainText()
        if str_msg == "": 
            return

        # [2] 类型判断
        if self.radio_server.isChecked():

            # [3] 是否连接
            if self.socket.isValid() == False:
                print("客户端未连接")
                return

            # [4] 发送数据
            if self.check_hex_send.isChecked():
                bytes_msg = Hexstring2Bytes(str_msg)
                self.socket.write(bytes_msg)
            else:
                bytes_msg = str_msg.encode()
                self.socket.write(bytes_msg)
            
            # [5] 是否清空
            if self.check_clear.isChecked():
                self.edit_msg.clear()

        else:
            if self.client.isValid() == False:
                print("客户端未连接")
                return

            if self.check_hex_send.isChecked():
                bytes_msg = Hexstring2Bytes(str_msg)
                self.client.write(bytes_msg)
            else:
                bytes_msg = str_msg.encode()
                self.client.write(bytes_msg)

            if self.check_clear.isChecked():
                self.edit_msg.clear()

    # 服务器 接收客户端连接 
    def on_server_accept(self):
        self.socket.abort()
        self.socket = self.server.nextPendingConnection()
        
        addr = QHostAddress()
        addr.setAddress(self.socket.peerAddress().toIPv4Address())
        str_ip_port = addr.toString() + ":" + str(self.socket.peerPort())
        self.text_msg.append(GetCurrentTime() + "  新用户 " + str_ip_port + " 已加入")
        
        self.socket.readyRead.connect(self.on_server_receive)
        self.socket.disconnected.connect(self.on_server_disconnected)

    # 服务器 接受数据
    def on_server_receive(self):
        rcvData = self.socket.read(1024)
        if self.check_hex_rcv.isChecked():
            str_rcvData = Bytes2Hexstring(rcvData)
            self.text_msg.append(GetCurrentTime() + "  " + str_rcvData)
        else:
            str_rcvData = rcvData.decode()
            self.text_msg.append(GetCurrentTime() + "  " + str_rcvData)

    # 服务器 监视连接断开
    def on_server_disconnected(self):
        addr = QHostAddress()
        addr.setAddress(self.socket.peerAddress().toIPv4Address())
        str_ip_port = addr.toString() + ":" + str(self.socket.peerPort())
        self.text_msg.append(GetCurrentTime() + "  用户 " + str_ip_port + " 已断开")
        self.socket.abort()
        self.socket.close()

    # 客户端 接受数据
    def on_client_receive(self):
        rcvData = self.client.read(1024)
        if self.check_hex_rcv.isChecked():
            str_rcvData = Bytes2Hexstring(rcvData)
            self.text_msg.append(GetCurrentTime() + "  " + str_rcvData)
        else:
            str_rcvData = rcvData.decode()
            self.text_msg.append(GetCurrentTime() + "  " + str_rcvData)

    def on_check_changed(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/qsocket.ini"
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
    w = QSocket()
    w.show()
    app.exec()