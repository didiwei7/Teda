import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/QMyPlugin")

from ui.mainwindow import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()