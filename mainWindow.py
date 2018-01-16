#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : yasin
# @time   : 2018/1/15 14:42
# @File   : mainWindow.py

import sys
from Ui_mainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.file_quit.triggered.connect(self.close)
        self.ui.help_abut.triggered.connect(self.on_help_abut_clicked)
        
        self.ui.set_des_button.clicked.connect(self.set_des_button_cliked)

    def on_help_abut_clicked(self):
        info = 'About'
        print(info)
        self.ui.textBrowser.append(info)

    def set_des_button_cliked(self):
        print('set des button')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())