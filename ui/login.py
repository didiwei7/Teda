import os
import sys
import json

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Login(QDialog):

    qloginChanged = pyqtSignal(str)

    def __init__(self, parent = None):
        super(Login, self).__init__()
        self.parent = parent

        self.label_user = QLabel("用户")
        self.label_pass = QLabel("密码")

        self.edit_user = QLineEdit()
        self.edit_pass = QLineEdit()

        self.btn_login = QPushButton("登陆")
        self.btn_sigin = QPushButton("注册")
        self.btn_cancel = QPushButton("取消")

        self.dict_userpass = {}

        self.setupUi()
        self.setConnect()
        self.readSettings()

    ''' 私有方法 '''
    def setupUi(self):
        self.edit_user.setFixedWidth(100)
        self.edit_pass.setFixedWidth(100)
        self.edit_pass.setEchoMode(QLineEdit.Password)

        layout_1 = QVBoxLayout()
        layout_2_1 = QHBoxLayout()
        layout_2_2 = QHBoxLayout()
        layout_2_3 = QHBoxLayout()

        layout_2_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_2_1.addWidget(self.label_user)
        layout_2_1.addWidget(self.edit_user)
        layout_2_1.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout_2_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_2_2.addWidget(self.label_pass)
        layout_2_2.addWidget(self.edit_pass)
        layout_2_2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout_2_3.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_2_3.addWidget(self.btn_login)
        layout_2_3.addWidget(self.btn_sigin)
        layout_2_3.addWidget(self.btn_cancel)
        layout_2_3.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout_1.addSpacing(30)
        layout_1.addLayout(layout_2_1)
        layout_1.addLayout(layout_2_2)
        layout_1.addSpacing(30)
        layout_1.addLayout(layout_2_3)
        layout_1.addSpacing(20)

        self.setStyleSheet( "QPushButton { border-radius: 4px;\n"
                                          "border: none;\n"
                                          "width:  60px;\n"
                                          "height: 20px;\n"
                                          "background: #78AADC;\n"
                                          "color: white;}\n"
                            "QPushButton:hover   { background: #9AC0CD; }\n"
                            "QPushButton:pressed { background: #007ACC; }")

        self.setLayout(layout_1)

    def setConnect(self):
        self.btn_login.clicked.connect(self.on_btn_login)
        self.btn_sigin.clicked.connect(self.on_btn_sigin)
        self.btn_cancel.clicked.connect(self.on_btn_cancel)
    
    def readSettings(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/login.json"
        with open(filepath, 'r', encoding = "utf-8") as file:
            self.dict_userpass = json.load(file)
            print(self.dict_userpass)

    ''' 槽函数 内部 '''
    def on_btn_login(self):
        if not self.edit_user.text() in self.dict_userpass.keys():
            QMessageBox.about(self, "提示", "该用户不存在")
            return
        else:
            if self.dict_userpass[self.edit_user.text()] != self.edit_pass.text():
                QMessageBox.about(self, "提示", "密码错误")
                return
            else:
                self.qloginChanged.emit(self.edit_user.text())
                self.close()

    def on_btn_sigin(self):
        str_user = self.edit_user.text()
        str_pass = self.edit_pass.text()
        str_msg = "预注册用户\n" + "用户\t" + str_user + "\n" + "密码\t" + str_pass

        ret = QMessageBox.information(self, "提示", str_msg, QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.dict_userpass[str_user] = str_pass
            filepath = os.path.dirname(os.path.abspath(__file__)) + "/config/login.json"
            with open(filepath, "w", encoding = "utf-8") as file:
                json.dump(self.dict_userpass, file, ensure_ascii = False)

    def on_btn_cancel(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Login()
    w.show()
    app.exec()