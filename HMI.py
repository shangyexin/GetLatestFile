#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : yasin
# @time   : 2018/1/15 14:42
# @File   : HMI.py

import sys
from PyQt5.QtWidgets import *
from mainWindow import *



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())