import os
import sys
import time
import threading

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/QMyPlugin")

from QMyPlugin.qex import *
from QMyPlugin.qnavigationbar import *

from login import *
from operation import *
from iodebug import *
from comdebug import *
from comshow import *

class MainWindow(QMainWindow):

    qappend_sendmsg = pyqtSignal(str)
    qappend_rcvmsg = pyqtSignal(str)
    qappend_runmsg = pyqtSignal(str)

    qset_in_status = pyqtSignal(int, int)
    qset_out_status = pyqtSignal(int, int)

    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.parent = parent

        # 控件
        self.action_file_new     = QAction("新建\t Ctrl + N", self)
        self.action_file_open    = QAction("打开\t Ctrl + O", self)
        self.action_file_save    = QAction("保存\t Ctrl + S", self)
        self.action_file_saveAll = QAction("全部保存\t Ctrl + Shift + S", self)
        self.action_file_quit    = QAction("退出\t Ctrl + Q", self)

        self.action_login_login  = QAction("登陆\t Ctrl + L", self)

        self.action_help_help    = QAction("帮助\t F1", self)
        self.action_help_about   = QAction("关于\t Ctrl + F1", self)
        self.action_help_aboutQt = QAction("关于Qt\t Ctrl + Shift + F1", self)

        self.label_status_login = QLabel("用户: 未登录 ")
        self.label_status_time = QLabel()

        # 串口
        self.serial = QSerialPort()
        self.list_rcvdata = []

        # 线程
        self.close_thread_dispose = True
        self.mutex = threading.Lock()

        # 窗口
        self.w_central = QWidget()
        self.vnavigationbar = QVNavigationBar(["操作界面", "I/O", "通讯调试", "通讯显示"])
        self.stackedWidget = QStackedWidget()
        self.w_login = Login()
        self.w_operation = Operation()
        self.w_iodebug = IODebug()
        self.w_comdebug = ComDebug()
        self.w_comshow = ComShow()

        self.setupUi()
        self.setConnect()
        self.writeLog("上位机已启动")
        if self.setSerial() == True:
            self.setThread()

    def __del__(self):
        # try:
        #     self.close_thread_dispose = True
        #     self.TDisposeMsg.join()
        #     print("thread_dispose_msg: close Success")
        # except:
        #     print("thread_addend_text: close Failed")
        pass

    ''' 保护方法 '''
    def closeEvent(self, event):
        ret = QMessageBox.information(self, "提示", "您确认退出么？", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
            self.writeSettings()
            self.writeLog("上位机已关闭\n\n")

            try:
                self.close_thread_dispose = True
                self.TDisposeMsg.join()
                print("thread_dispose_msg: close Success")
            except:
                print("thread_dispose_msg: close Failed")

    ''' 私有方法 '''
    def writeSettings(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/settings.ini"
        if not QFileInfo(filepath).isFile():
            return
        else:
            setting = QSettings(filepath, QSettings.IniFormat)
            setting.beginGroup("MainWindow")
            setting.setValue("size", self.size())
            setting.setValue("pos", self.pos())
            setting.endGroup()

    def readSettings(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/settings.ini"
        if not QFileInfo(filepath).isFile():
            self.setGeometry(QApplication.desktop().availableGeometry().adjusted(50, 50, -50, -50))
        else:
            setting = QSettings(filepath, QSettings.IniFormat)
            self.resize(setting.value("MainWindow/size"))
            self.move(setting.value("MainWindow/pos"))

    def writeLog(self, str):
        str_filepath = os.path.dirname(os.path.abspath(__file__)) + "/data/log/{date}.txt".format(date = GetCurrentDate())
        str_write = GetCurrentTime() + "   " + str + "\n";

        file = QFile(str_filepath)
        file.open(QIODevice.WriteOnly | QIODevice.Text | QIODevice.Append)
        file.write(str_write.encode())  # 写UTF-8格式中文无乱码
        # input = QTextStream(file)
        # input << str_write
        file.close()

    def setupUi(self):
        self.setQMenuBar()
        self.setQStatusBar()
        self.readSettings()

        # 初始化导航
        self.vnavigationbar.setBackColor("#303947")
        self.vnavigationbar.setForeColor("#E4EBF3")
        self.vnavigationbar.setSelectedForeColor("#000000")
        self.vnavigationbar.setWidth(120)
        self.vnavigationbar.setRowHeight(40)

        # 初始化控件
        self.stackedWidget.insertWidget(0, self.w_operation)
        self.stackedWidget.insertWidget(1, self.w_iodebug)
        self.stackedWidget.insertWidget(2, self.w_comdebug)
        self.stackedWidget.insertWidget(3, self.w_comshow)

        # 布局
        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(0)
        layout_1.addWidget(self.vnavigationbar)
        layout_1.addWidget(self.stackedWidget)

        self.w_central.setLayout(layout_1)
        self.setCentralWidget(self.w_central)

    def setQMenuBar(self):
        self.action_file_new.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))        
        self.action_file_open.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        self.action_file_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        self.action_file_saveAll.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S))
        self.action_file_quit.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))

        self.action_login_login.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))

        self.action_help_help.setShortcut(QKeySequence(Qt.Key_F1))
        self.action_help_about.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F1))
        self.action_help_aboutQt.setShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_F1))

        list_action_file = [self.action_file_new, self.action_file_open, self.action_file_save, self.action_file_saveAll, self.action_file_quit]
        list_action_login = [self.action_login_login]
        list_action_help = [self.action_help_help, self.action_help_about, self.action_help_aboutQt]

        menu_file = self.menuBar().addMenu("文件(&F)")
        menu_login = self.menuBar().addMenu("登陆(&L)")
        menu_help = self.menuBar().addMenu("帮助(&H)")

        menu_file.addActions(list_action_file)
        menu_login.addActions(list_action_login)
        menu_help.addActions(list_action_help)

    def setQStatusBar(self):
        self.label_status_login.setFont(QFont("MicroSoft Yahei", 9))

        self.label_status_time.setFont(QFont("MicroSoft Yahei", 9))
        
        self.statusBar().setStyleSheet("background-color: #007ACC; ")
        self.statusBar().addPermanentWidget(self.label_status_login)
        self.statusBar().addPermanentWidget(self.label_status_time)

        timer_date = QTimer(self)
        timer_date.start(1000)
        timer_date.timeout.connect(self.on_status_time)

    def setConnect(self):
        # Action
        self.action_file_quit.triggered.connect(self.close)
        self.action_help_help.triggered.connect(self.on_action_help_help)
        self.action_help_about.triggered.connect(self.on_action_help_about)
        self.action_help_aboutQt.triggered.connect(self.on_action_help_aboutQt)
        self.action_login_login.triggered.connect(self.on_action_login_login)

        # Navigation
        self.vnavigationbar.qcurrentItemChanged.connect(self.stackedWidget.setCurrentIndex)

        # Serial
        self.serial.readyRead.connect(self.on_serial_receive)

        '''以下为外部信号连接该类的槽'''
        # Login Signal
        self.w_login.qloginChanged.connect(self.on_login_changed)

        self.w_iodebug.qsendmsg_out_clicked.connect(self.on_send_msg)

        self.w_operation.qsendmsg_btn_clicked.connect(self.on_send_msg)
        self.w_operation.qsendmsg_edit_clicked.connect(self.on_send_msg)

        '''以下为该类信号连接外部的槽'''
        self.qset_in_status.connect(self.w_iodebug.on_set_in_status)
        self.qset_out_status.connect(self.w_iodebug.on_set_out_status)

        self.qappend_sendmsg.connect(self.w_comshow.on_append_sendmsg)
        self.qappend_rcvmsg.connect(self.w_comshow.on_append_rcvmsg)

        self.qappend_runmsg.connect(self.w_operation.on_append_runmsg)

    def setSerial(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/settings.ini"
        if not QFileInfo(filepath).isFile(): 
            return False

        setting = QSettings(filepath, QSettings.IniFormat)
        self.serial.setPortName(setting.value("SerialPort/portName"))
        if not self.serial.open(QIODevice.ReadWrite):
            return False
        
        self.serial.setBaudRate(int(setting.value("SerialPort/baudRate")))
        self.serial.setDataBits(GetDatabits(setting.value("SerialPort/dataBits")))
        self.serial.setParity(GetParity(setting.value("SerialPort/parity")))
        self.serial.setStopBits(GetStopBits(setting.value("SerialPort/stopBits")))
        self.serial.setFlowControl(GetFlowControl(setting.value("SerialPort/flowCtrl")))

        return True

    def setThread(self):
        self.close_thread_dispose = False
        self.TDisposeMsg = threading.Thread(target = MainWindow.thread_dispose_msg, args=(self, ))
        self.TDisposeMsg.start()

    def thread_dispose_msg(self):
        while self.close_thread_dispose == False:
            if len(self.list_rcvdata) > 0:
                # [1] 获取并移除首部元素
                self.mutex.acquire()
                str_msg = self.list_rcvdata.pop(0)
                self.mutex.release()

                # [2] 处理消息
                try:
                    list_msg = str_msg.split(',')
                    if list_msg[0] == "CMD_IN":
                        self.qset_in_status.emit(int(list_msg[1]), int(list_msg[2]))
                    elif list_msg[0] == "CMD_OUT":
                        self.qset_out_status.emit(int(list_msg[1]), int(list_msg[2]))
                    elif list_msg[0] == "CMD_DEBUG":
                        self.qappend_runmsg.emit(list_msg[1])
                    else:
                        self.qappend_runmsg.emit("该指令不存在, 请检查")
                except:
                    self.qappend_runmsg.emit("指令解析发生错误")

            time.sleep(0.001)

    ''' 槽函数 内部 '''
    def on_status_time(self):
        self.label_status_time.setText(GetCurrentTime())

    def on_action_help_help(self):
        QMessageBox.about(self, "帮助", "快捷键：\n"
                                        "帮助\t F1\n"
                                        "关于\t Ctrl + F1\n"
                                        "关于Qt\t Ctrl + Shift + F1\n"
                                        "登陆\t Ctrl + L\n"
                                        "退出\t Ctrl + Q\n")

    def on_action_help_about(self):
        QMessageBox.about(self, "关于", "作者:\t 敌敌畏\n"
                                        "邮箱:\t 15927513928@163.com")

    def on_action_help_aboutQt(self):
        QMessageBox.aboutQt(self, "关于Qt")

    def on_action_login_login(self):
        self.w_login.exec()

    def on_serial_receive(self):
        # [1] 接收
        rcvData = self.serial.read(1024)
        str_rcvData = ""  
        
        # 接收数据非空判断
        if rcvData == b'':      
            return

        # 转码是否正常
        try:                   
            str_rcv = rcvData.decode()
        except:
            str_rcv = ""
            self.qappend_runmsg.emit("接收数据时转码错误")
        finally:
            if str_rcv == "":
                return

        # [2] 显示接收
        self.qappend_rcvmsg.emit(str_rcv)
        self.writeLog(str_rcv)

        # [3] 尾添加到列表
        self.mutex.acquire()
        self.list_rcvdata.append(str_rcv)
        self.mutex.release()
        
        print(self.list_rcvdata)

    ''' 槽函数 外部 '''
    def on_login_changed(self, user):
        self.label_status_login.setText(user + ": 已登陆 ")
        if self.w_operation.get_warn_label() == "请登陆":
            self.w_operation.set_warn_label("登陆成功")
        
    def on_send_msg(self, msg):
        # [1] 显示发送
        self.qappend_sendmsg.emit(msg)
        
        # [2] 发送
        self.serial.write(msg.encode())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

