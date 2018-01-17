#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : yasin
# @time   : 2018/1/15 14:42
# @File   : mainWindow.py

import sys, os, shutil, logging
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication)
from PyQt5.QtCore import QThread
from Ui_mainWindow import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )

class MainWindow(QMainWindow, Ui_MainWindow):
    src_folder_path = None
    dst_folder_path = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.file_quit.triggered.connect(self.close)
        self.ui.help_abut.triggered.connect(self.on_help_about_clicked)

        self.ui.set_src_button.clicked.connect(self.set_src_button_cliked)
        self.ui.set_des_button.clicked.connect(self.set_dst_button_cliked)
        self.ui.start_button.clicked.connect(self.start_button_cliked)

    #‘关于’菜单
    def on_help_about_clicked(self):
        info = 'About'
        print(info)
        self.ui.textBrowser.append(info)

    #‘设置源文件夹’按钮
    def set_src_button_cliked(self):
        # self.output_log('click set src folder button')
        self.src_folder_path = QFileDialog.getExistingDirectory(self, '选取文件夹', '/home')
        if self.src_folder_path:
            self.output_log('设置源文件成功')
            src_str_prefix = '源文件夹： '
            src_str = src_str_prefix + self.src_folder_path
            self.ui.src_floder_label.setText(src_str)
        else:
            self.output_log('未设置目标文件夹')

    #‘设置目标文件夹’按钮
    def set_dst_button_cliked(self):
        #self.output_log('click set dest folder button')
        self.dst_folder_path = QFileDialog.getExistingDirectory(self, '选取文件夹', '/home')
        if self.dst_folder_path:
            self.output_log('设置目标文件成功')
            dst_str_prefix = '目标文件夹： '
            dst_str = dst_str_prefix + self.dst_folder_path
            self.ui.dst_floder_label.setText(dst_str)
        else:
            self.output_log('未设置目标文件夹')

    #‘开始’按钮
    def start_button_cliked(self):
        #print('start button cliked')
        if(self.src_folder_path == None):
            self.output_log('源文件未设置!')
            # TODO
        elif(self.dst_folder_path == None):
            self.output_log('目标文件夹未设置!')
            #TODO
        else:
            #start_copy(self.src_folder_path, self.dst_folder_path)
            start_thread = function(self)
            start_thread.start()
           # start_thread.run()
            start_thread.start_copy(self.src_folder_path, self.dst_folder_path)
            #start_thread.exec_()

    #输出log到GUI文本框
    def output_log(self, str):
        self.ui.textBrowser.append(str)

class function(QThread):
    def __init__(self, parent=None):
        super(function, self).__init__(parent)

    def run(self):
        print('this is a thread')

    # 检查源文件夹
    def check_src_dir(self, project_dir):
            logging.debug('project dir set by user is %s' % project_dir)
            if os.path.exists(project_dir):
                logging.debug('project dir set by user is existed!')
                return True
            else:
                logging.error('project dir set by user is not existed!')
                return False

    # 检查目标文件夹
    def check_dst_dir(self, des_file_dir):
         if os.path.exists(des_file_dir):
            if os.path.isdir(des_file_dir):
                logging.info('%s is already existed,do not need create!' % des_file_dir)
            else:
                logging.error('%s is not a directory' % des_file_dir)
                return False
         else:
            logging.debug('%s is not existed' % des_file_dir)
            os.makedirs(des_file_dir)
            logging.debug('create %s success!' % des_file_dir)
            return True

    # 获取项目文件夹内最新文件夹
    def get_latest_dir(self, project_dir):
        lists = os.listdir(project_dir)  # 列出目录的下所有文件和文件夹保存到lists
        logging.debug(list)
        lists.sort(key=lambda fn: os.path.getmtime(project_dir + "\\" + fn))  # 按时间排序
        directory_latest = os.path.join(project_dir, lists[-1])  # 获取最新的文件保存到directory_latest
        logging.debug(directory_latest)
        return directory_latest

    # 下载文件夹
    def download_file(self, src_dir, des_dir):
        path, dir = os.path.split(src_dir)
        dest_dir_abs = des_dir + os.path.sep + dir  # 目标文件绝对路径
        logging.debug('dest_dir is %s' % dest_dir_abs)
        if os.path.exists(dest_dir_abs):
            logging.warning('%s is already existed, do not need update!' % dest_dir_abs)
            return
        else:
            shutil.copytree(src_dir, dest_dir_abs)  # 复制文件

    def start_copy(self, src_dir, dst_dir):
        print('Welcome to use update package download tool!')

        if (self.check_src_dir(src_dir) == True):
            pass
        else:
            pass
        if (self.check_dst_dir(dst_dir) == True):
            pass
        else:
            pass

        latest_dir = self.get_latest_dir(src_dir)  # 获取项目文件夹内最新文件夹
        self.download_file(latest_dir, dst_dir)  # 复制最新文件夹到目标目录

        logging.debug('Everything is ok, goodbye!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())