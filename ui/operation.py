import os
import sys
import json

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/QMyPlugin")

from QMyPlugin.qex import *
from QMyPlugin.qmyedit import *
from QMyPlugin.qmylabel import *
from QMyPlugin.qflowlayout import *

class Operation(QWidget):

    qsendmsg_btn_clicked = pyqtSignal(str)
    qsendmsg_edit_clicked = pyqtSignal(str)

    def __init__(self, parent = None):
        super(Operation, self).__init__()
        self.parent = parent

        self.group_logo = QGroupBox()
        self.group_warn = QGroupBox()
        self.group_button = QGroupBox()
        self.group_labeledit = QGroupBox()
        self.group_debug = QGroupBox()

        self.label_logo = QLabel()
        self.label_warn = QLabel()
        self.text_run = QTextBrowser()

        self.dict_operation = {}
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/operation.json"
        with open(filepath, 'r', encoding = "utf-8") as file:
            self.dict_operation = json.load(file)
            print(self.dict_operation)

        self.num_btn = list(self.dict_operation["btn"].keys()).__len__()
        self.num_label = list(self.dict_operation["label"].keys()).__len__()
        self.num_edit = list(self.dict_operation["edit"].keys()).__len__()
        self.num_btnmsg = list(self.dict_operation["btnmsg"].keys()).__len__()

        self.btn_com = [None] * self.num_btn
        self.label_com = [None] * self.num_label
        self.edit_com = [None] * self.num_edit
        self.list_btnmsg = [None] * self.num_btnmsg

        self.setBtnMsg()
        self.setupUi()
        self.setConnect()

    ''' 私有方法 '''
    def setupUi(self):
        self.setGroupLogo()
        self.setGroupWarn()
        self.setGroupButton()
        self.setGroupLabelEdit()
        self.setGroupDebug()

        layout_1 = QHBoxLayout()
        layout_2_1 = QVBoxLayout()
        layout_2_2 = QVBoxLayout()

        layout_2_1.addWidget(self.group_logo)
        layout_2_1.addWidget(self.group_warn)
        layout_2_1.addWidget(self.group_button)
        layout_2_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout_2_2.addWidget(self.group_labeledit)
        layout_2_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout_2_2.addWidget(self.group_debug)

        layout_1.addLayout(layout_2_1)
        layout_1.addLayout(layout_2_2)
        self.setLayout(layout_1)

    def setGroupLogo(self):
        self.label_logo.setFixedSize(280, 200)

        filepath = os.path.dirname(os.path.abspath(__file__)) + "/res/logo.png"
        img = QImage(filepath)
        img = img.scaled(self.label_logo.width(), self.label_logo.height())
        self.label_logo.setPixmap(QPixmap.fromImage(img))

        layout_1 = QHBoxLayout()
        layout_1.setContentsMargins(3, 3, 3, 3)
        layout_1.setSpacing(0)
        layout_1.addWidget(self.label_logo)

        self.group_logo.setLayout(layout_1)

    def setGroupWarn(self):
        self.label_warn.setFont(QFont("MicroSoft Yahei", 20, QFont.Bold))
        self.label_warn.setAlignment(Qt.AlignCenter)
        self.label_warn.setText("请登陆")
        self.label_warn.setFixedHeight(100)

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.label_warn)

        self.group_warn.setLayout(layout_1)

    def setGroupButton(self):
        btn_style = ( "QPushButton { border-radius: 3px;\n"
                                    "border: none;\n"
                                    "width:  60px;\n"
                                    "height: 20px;\n"
                                    "background: #78AADC;\n"
                                    "color: white;}\n"
                      "QPushButton:hover { background: #9AC0CD; }\n"
                      "QPushButton:pressed { background: #007ACC; }")
        layout_1 = QHBoxLayout()
        layout_2 = QFlowLayout()
        for key in self.dict_operation["btn"].keys():
            name = self.dict_operation["btn"][key]["name"]
            visible = self.dict_operation["btn"][key]["visible"]
            self.btn_com[int(key)] = QPushButton(name)
            self.btn_com[int(key)].setObjectName("btn_com" + key)
            self.btn_com[int(key)].setVisible(visible)
            layout_2.addWidget(self.btn_com[int(key)])
        
        layout_1.addLayout(layout_2)
        # layout_1.setContentsMargins(5, 5, 5, 5)
        self.group_button.setLayout(layout_1)
        self.group_button.setStyleSheet(btn_style)

    def setGroupLabelEdit(self):
        layout_1 = QHBoxLayout()
        layout_2_1 = QVBoxLayout()
        layout_2_2 = QVBoxLayout()

        layout_2_1.setSpacing(1)
        layout_2_2.setSpacing(1)

        label_title_1 = QLabel("通用显示:")
        label_title_1.setFixedWidth(220)
        label_title_1.setAlignment(Qt.AlignCenter)
        label_title_1.setFont(QFont("MicroSoft Yahei", 15, QFont.Bold))
        layout_2_1.addWidget(label_title_1)
        layout_2_1.addSpacing(5)
        for key in self.dict_operation["label"].keys():
            name = self.dict_operation["label"][key]["name"]
            value = self.dict_operation["label"][key]["value"]
            unit = self.dict_operation["label"][key]["unit"]
            visible = self.dict_operation["label"][key]["visible"]
            self.label_com[int(key)] = QMyLabel(name, value, unit)
            self.label_com[int(key)].setObjectName("label_com" + key)
            self.label_com[int(key)].setVisible(visible)
            layout_2_1.addWidget(self.label_com[int(key)]) 

        label_title_2 = QLabel("通用设置:")
        label_title_2.setFont(QFont("MicroSoft Yahei", 15, QFont.Bold))
        label_title_2.setFixedWidth(260)
        label_title_2.setAlignment(Qt.AlignCenter)
        layout_2_2.addWidget(label_title_2)
        layout_2_2.addSpacing(5)
        for key in self.dict_operation["edit"].keys():
            name = self.dict_operation["edit"][key]["name"]
            value = self.dict_operation["edit"][key]["value"]
            unit = self.dict_operation["edit"][key]["unit"]
            visible = self.dict_operation["edit"][key]["visible"]
            self.edit_com[int(key)] = QMyEdit(name, value, unit)
            self.edit_com[int(key)].setObjectName("edit_com" + key)
            self.edit_com[int(key)].setVisible(visible)
            layout_2_2.addWidget(self.edit_com[int(key)]) 
        
        layout_1.addLayout(layout_2_1)
        layout_1.addLayout(layout_2_2)
        self.group_labeledit.setLayout(layout_1)

    def setGroupDebug(self):
        self.text_run.setFont(QFont("MicroSoft Yahei", 8))

        layout_1 = QHBoxLayout()
        layout_1.addWidget(self.text_run)
        self.group_debug.setLayout(layout_1)

        self.text_run.append(GetCurrentTime() + ":  " + "您还没有登陆,暂时无法为您提供操作权限哦")
        self.text_run.append(GetCurrentTime() + ":  " + "请点击上方目录栏的登陆选项, 或者使用快捷键 Ctrl + L, 进行登陆")

    def setBtnMsg(self):
        for key in self.dict_operation["btnmsg"].keys():
            self.list_btnmsg[int(key)] = self.dict_operation["btnmsg"][key]

    ''' 公开方法 '''
    def get_warn_label(self):
        return self.label_warn.text()

    def set_warn_label(self, str):
        self.label_warn.setText(str)

    ''' 槽函数 外部 '''
    def setConnect(self):
        for i in range(self.num_btn):
            self.btn_com[i].clicked.connect(self.on_btn_com)

        for i in range(self.num_edit):
            self.edit_com[i].qclicked.connect(self.on_edit_com)

    def on_btn_com(self):
        btnName = QPushButton().sender().objectName()
        for i in range(self.num_btn):
            if btnName == "btn_com" + str(i):
                self.qsendmsg_btn_clicked.emit(self.list_btnmsg[i])
                print(self.list_btnmsg[i])

    def on_edit_com(self):
        editName = QMyEdit().sender().objectName()
        for i in range(self.num_edit):
            if editName == "edit_com" + str(i):
                # [1] 保存数据
                value = self.edit_com[i].getValue()
                self.dict_operation["edit"][str(i)]["value"] = value
                filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/operation.json"
                with open(filepath, 'w', encoding = "utf-8") as file:
                    json.dump(self.dict_operation, file, ensure_ascii = False)
                # [2] 发送数据
                str_msg = "CMD_EDIT,{0},{1}".format(i, value)
                self.qsendmsg_edit_clicked.emit(str_msg)
                print(str_msg)

    def on_append_runmsg(self, msg):
        self.text_run.append(GetCurrentTime() + ":  " + msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Operation()
    w.show()
    app.exec()