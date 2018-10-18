# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(800, 600)
        Main.setStyleSheet("background-color: rgb(230, 230, 250);")
        self.label_back = QtWidgets.QLabel(Main)
        self.label_back.setGeometry(QtCore.QRect(0, 100, 550, 330))
        self.label_back.setText("")
        self.label_back.setPixmap(QtGui.QPixmap("cormix_main.bmp"))
        self.label_back.setObjectName("label_back")
        self.label_title = QtWidgets.QLabel(Main)
        self.label_title.setGeometry(QtCore.QRect(280, 20, 240, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: rgb(0, 120, 215);")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.btn_reset = QtWidgets.QPushButton(Main)
        self.btn_reset.setGeometry(QtCore.QRect(630, 170, 100, 40))
        self.btn_reset.setStyleSheet("QPushButton { \n"
                                     "    border-radius: 5px;\n"
                                     "    border: none;\n"
                                     "    width:  100px;\n"
                                     "    font-family: MicroSoft Yahei;\n"
                                     "    font-size: 20px;\n"
                                     "    font-weight:bold;\n"
                                     "    height: 40px;\n"
                                     "    background: #9AC0CD;\n"
                                     "    color: #E6E6FA; }\n"
                                     "QPushButton:hover { background: #007ACC; }\n"
                                     "QPushButton:pressed { background: #CCCCCC; }")
        self.btn_reset.setObjectName("btn_reset")
        self.btn_start = QtWidgets.QPushButton(Main)
        self.btn_start.setGeometry(QtCore.QRect(630, 230, 100, 40))
        self.btn_start.setStyleSheet("QPushButton { \n"
                                     "    border-radius: 5px;\n"
                                     "    border: none;\n"
                                     "    width:  100px;\n"
                                     "    font-family: MicroSoft Yahei;\n"
                                     "    font-size: 20px;\n"
                                     "    font-weight:bold;\n"
                                     "    height: 40px;\n"
                                     "    background: #9AC0CD;\n"
                                     "    color: #E6E6FA; }\n"
                                     "QPushButton:hover { background: #007ACC; }\n"
                                     "QPushButton:pressed { background: #CCCCCC; }")
        self.btn_start.setObjectName("btn_start")
        self.btn_stop = QtWidgets.QPushButton(Main)
        self.btn_stop.setGeometry(QtCore.QRect(630, 290, 100, 40))
        self.btn_stop.setStyleSheet("QPushButton { \n"
                                    "    border-radius: 5px;\n"
                                    "    border: none;\n"
                                    "    width:  100px;\n"
                                    "    font-family: MicroSoft Yahei;\n"
                                    "    font-size: 20px;\n"
                                    "    font-weight:bold;\n"
                                    "    height: 40px;\n"
                                    "    background: #9AC0CD;\n"
                                    "    color: #E6E6FA; }\n"
                                    "QPushButton:hover { background: #007ACC; }\n"
                                    "QPushButton:pressed { background: #CCCCCC; }")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_fill = QtWidgets.QPushButton(Main)
        self.btn_fill.setGeometry(QtCore.QRect(630, 350, 100, 40))
        self.btn_fill.setStyleSheet("QPushButton { \n"
                                    "    border-radius: 5px;\n"
                                    "    border: none;\n"
                                    "    width:  100px;\n"
                                    "    font-family: MicroSoft Yahei;\n"
                                    "    font-size: 20px;\n"
                                    "    font-weight:bold;\n"
                                    "    height: 40px;\n"
                                    "    background: #9AC0CD;\n"
                                    "    color: #E6E6FA; }\n"
                                    "QPushButton:hover { background: #007ACC; }\n"
                                    "QPushButton:pressed { background: #CCCCCC; }")
        self.btn_fill.setObjectName("btn_fill")
        self.btn_clean = QtWidgets.QPushButton(Main)
        self.btn_clean.setGeometry(QtCore.QRect(630, 410, 100, 40))
        self.btn_clean.setStyleSheet("QPushButton { \n"
                                     "    border-radius: 5px;\n"
                                     "    border: none;\n"
                                     "    width:  100px;\n"
                                     "    font-family: MicroSoft Yahei;\n"
                                     "    font-size: 20px;\n"
                                     "    font-weight:bold;\n"
                                     "    height: 40px;\n"
                                     "    background: #9AC0CD;\n"
                                     "    color: #E6E6FA; }\n"
                                     "QPushButton:hover { background: #007ACC; }\n"
                                     "QPushButton:pressed { background: #CCCCCC; }")
        self.btn_clean.setObjectName("btn_clean")
        self.widget = QtWidgets.QWidget(Main)
        self.widget.setGeometry(QtCore.QRect(630, 60, 141, 101))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edit_index = QtWidgets.QLineEdit(self.widget)
        self.edit_index.setObjectName("edit_index")
        self.gridLayout.addWidget(self.edit_index, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_theoryRatio = QtWidgets.QLabel(self.widget)
        self.label_theoryRatio.setObjectName("label_theoryRatio")
        self.gridLayout.addWidget(self.label_theoryRatio, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_actualRatio = QtWidgets.QLabel(self.widget)
        self.label_actualRatio.setObjectName("label_actualRatio")
        self.gridLayout.addWidget(self.label_actualRatio, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_runtime = QtWidgets.QLabel(self.widget)
        self.label_runtime.setObjectName("label_runtime")
        self.gridLayout.addWidget(self.label_runtime, 3, 1, 1, 1)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Form"))
        self.label_title.setText(_translate("Main", "CorMix 运行监控系统"))
        self.btn_reset.setText(_translate("Main", "复位"))
        self.btn_start.setText(_translate("Main", "启动"))
        self.btn_stop.setText(_translate("Main", "停止"))
        self.btn_fill.setText(_translate("Main", "填充"))
        self.btn_clean.setText(_translate("Main", "清洗"))
        self.label.setText(_translate("Main", "配方编号:"))
        self.edit_index.setText(_translate("Main", "1"))
        self.label_2.setText(_translate("Main", "理论配比:"))
        self.label_theoryRatio.setText(_translate("Main", "1 : 1"))
        self.label_3.setText(_translate("Main", "实际配比:"))
        self.label_actualRatio.setText(_translate("Main", "1 : 1"))
        self.label_4.setText(_translate("Main", "运行时间:"))
        self.label_runtime.setText(_translate("Main", "0 min"))


# import cormix_rc
