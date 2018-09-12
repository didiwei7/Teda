import json
import os
import sys
from types import MethodType

from PyQt5.QtCore import *
from PyQt5.QtSerialPort import *
from PyQt5.QtWidgets import *

# 获取当前时间
def GetCurrentTime():
    currentTime = QDateTime.currentDateTime()
    str_currentTime = currentTime.toString("yyyy-MM-dd hh:mm:ss")
    return str_currentTime

# 获取当前日期
def GetCurrentDate():
    currentTime = QDateTime.currentDateTime()
    str_currentDate = currentTime.toString("yyyy-MM-dd")
    return str_currentDate

# "35 30" -> "50"
def Hexstring2Bytes(str):
    ret_bytes = b''
    ret_bytes = ret_bytes.fromhex(str)
    return ret_bytes

# "35 30" -> b'50'
def Hexstring2Asciistring(str):
    bytes = b''
    bytes = bytes.fromhex(str)
    ret_str = bytes.decode()
    return ret_str

# "50" -> "35 30"
def Asciistring2Hexstring(str):
    str_ret = ""
    bytes = str.encode()
    for index in range(len(bytes)):
        str_index = hex(bytes[index])[2:]
        if len(str_index) == 1: 
            str_index = "0" + str_index  
        str_ret += str_index
        str_ret += " "
    str_ret = str_ret.strip().upper()
    return str_ret

# b'50' -> "35 30"
def Bytes2Hexstring(bytes):
    str_ret = ""
    for index in range(len(bytes)):
        str_index = hex(bytes[index])[2:]
        if len(str_index) == 1: 
            str_index = "0" + str_index  
        str_ret += str_index
        str_ret += " "
    str_ret = str_ret.strip().upper()
    return str_ret

# 串口 获取数据位
def GetDatabits(str):
    if str == "5": return QSerialPort.Data5
    elif str == "6": return QSerialPort.Data6
    elif str == "7": return QSerialPort.Data7
    elif str == "8": return QSerialPort.Data8
    else: return QSerialPort.Data8

# 串口 获取校验位
def GetParity(str):
    if str == "None": return QSerialPort.NoParity
    elif str == "Even": return QSerialPort.EvenParity
    elif str == "Odd": return QSerialPort.OddParity
    elif str == "Space": return QSerialPort.SpaceParity
    elif str == "Mask": return QSerialPort.MarkParity
    else: return QSerialPort.NoParity

# 串口 获取停止位
def GetStopBits(str):
    if str == "1": return QSerialPort.OneStop
    elif str == "1.5": return QSerialPort.OneAndHalfStop
    elif str == "2": return QSerialPort.TwoStop
    else: return QSerialPort.OneStop

# 串口 获取流控
def GetFlowControl(str):
    if str == "None": return QSerialPort.NoFlowControl
    elif str == "Hardware": return QSerialPort.HardwareControl
    elif str == "Software": return QSerialPort.SoftwareControl
    else: return QSerialPort.NoFlowControl

def str2bool(str):
    if str == "True" or str == "true":
        return True
    else:
        return False

def float2str(value, precision):
    str_ret = "{arg_value:.{arg_precision}f}".format(arg_value=value, arg_precision=precision)
    return str_ret


# print(Hexstring2Asciistring("35 30"))
# print(Hexstring2Bytes("35 30"))
# print(Bytes2Hexstring(b'50'))
# print(Asciistring2Hexstring("50"))

# bytes = b'\x02'
# print(type(bytes[0] & 0xFF))

# b = "{value:.{precision}f}".format(value=485.15456, precision=2)
# print(b)


# class Person:
#     def dd(self):
#         print("dd")
# def eat(self):
#     print("eat")
# Person.eat = MethodType(eat, Person)
# ss = Person()
# ss.dd()
# ss.eat()
