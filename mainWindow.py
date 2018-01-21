#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : yasin
# @time   : 2018/1/15 14:42
# @File   : mainWindow.py

import sys, os, shutil, logging, configparser, time
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication, QInputDialog, QMessageBox)
from PyQt5.QtCore import (QThread, pyqtSignal)
from Ui_mainWindow import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )

class MainWindow(QMainWindow, Ui_MainWindow):
    project_name = None
    src_folder_path = None
    dst_folder_path = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.conf = configure()
        self.setFixedSize(600, 500)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #将进度初始化为零
        self.ui.progressBar.setValue(0)

        #从配置文件中读取源文件和目标文件路径并进行显示
        self.read_config_file()

        #设置菜单栏
        self.ui.file_set.triggered.connect(self.file_set_cliked)
        self.ui.file_quit.triggered.connect(self.close)
        self.ui.help_help.triggered.connect(self.on_help_help_clicked)
        self.ui.help_abut.triggered.connect(self.on_help_about_clicked)

        #设置按钮
        self.ui.set_src_button.clicked.connect(self.set_src_button_cliked)
        self.ui.set_des_button.clicked.connect(self.set_dst_button_cliked)
        self.ui.del_old_button.clicked.connect(self.del_old_button_clicked)
        self.ui.start_button.clicked.connect(self.start_button_cliked)

    # 'help' 菜单
    def on_help_help_clicked(self):
        QMessageBox.about(self, '使用说明',
                          '本软件可以将源文件夹中的最新文件夹复制到目标文件夹，'
                          '一般用于一键下载项目中的最新升级包至本地目录')

    #‘关于’菜单
    def on_help_about_clicked(self):
        QMessageBox.about(self, '关于',
                                  'version：0.1'
                                  '\n' 
                                  'author: yasin')

    # '设置' 菜单
    def file_set_cliked(self):
        self.project_name, ok = QInputDialog.getText(self, '设置',
                                        '请输入项目名称:')
        if ok:
            #修改项目名称显示
            self.ui.project_name_label.setText(self.project_name)
            self.output_log('设置项目名称成功')
            # 写入配置文件
            try:
                self.conf.set_project_name(self.project_name)
            except Exception as e:
                logging.debug(e)


    #‘设置源文件夹’按钮
    def set_src_button_cliked(self):
        # self.output_log('click set src folder button')
        self.src_folder_path = QFileDialog.getExistingDirectory(self, '选取文件夹', '/home')
        if self.src_folder_path:
            self.output_log('设置源文件成功')
            src_str_prefix = '源文件夹： '
            src_str = src_str_prefix + self.src_folder_path
            self.ui.src_floder_label.setText(src_str)
            # 写入配置文件
            try:
                self.conf.set_src_folder_path(self.src_folder_path)
            except Exception as e:
                logging.debug(e)
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
            #写入配置文件
            try:
                self.conf.set_dst_folder_path(self.dst_folder_path)
            except Exception as e:
                logging.debug(e)
        else:
            self.output_log('未设置目标文件夹')

    # '删除旧文件'按钮
    def del_old_button_clicked(self):
        self.ui.progressBar.setValue(100)

    #‘开始’按钮
    def start_button_cliked(self):
        #logging.debug('start button cliked')
        if(self.src_folder_path == None or self.src_folder_path == ''):
            self.output_log('源文件未设置!')
            # TODO
        elif(self.dst_folder_path == None or self.dst_folder_path == '' ):
            self.output_log('目标文件夹未设置!')
            #TODO
        else:
            # 把按钮禁用掉
            self.ui.start_button.setDisabled(True)
            # 新建对象，传入参数
            self.start_thread = function(self.src_folder_path, self.dst_folder_path)
            # 连接子线程的进度信号和槽函数
            self.start_thread.progress_signal.connect(self.show_progress)
            # 连接子进程的结束信号和槽函数
            self.start_thread.finish_signal.connect(self.start_copy_end)
            try:
                self.start_thread.start()
            except Exception as e:
                logging.debug(e)

    #进度信号槽函数
    def show_progress(self, progress):
        self.ui.progressBar.setValue(progress)

    #start 按钮结束
    def start_copy_end(self, result):
        logging.debug('receive end signal')
        logging.debug(result)
        if(result == 'dir_name_repetition'):
            try:
                reply = QMessageBox.question(self, '警告',
                                    '目标文件夹已有源文件内的最新目录，您的操作会删除该最新目录，请确认是否删除？',
                                   QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
                if(reply == QMessageBox.Yes):
                    self.output_log('确认删除')
                    real_dir_name = os.path.split(get_latest_object(self.src_folder_path))[1]
                    logging.debug(real_dir_name)
                    dir_to_be_deleted = os.path.join(self.dst_folder_path, real_dir_name)
                    logging.debug('dir to be deleted is %s' % dir_to_be_deleted)
                    #删除目标文件夹中重复最新文件夹
                    try :
                        shutil.rmtree(dir_to_be_deleted)
                        self.output_log('删除成功')
                    except Exception as e:
                        self.output_log('删除失败')
                        logging.error(e)
                else:
                    self.output_log('取消删除')
            except Exception as e:
                logging.error(e)
        elif(result == 'end_with_success'):
            self.ui.progressBar.setValue(100)
            logging.debug(self.dst_folder_path)
           # QFileDialog.directoryEntered(self.dst_folder_path)

            self.output_log('下载完成！')

        # 恢复按钮
        self.ui.start_button.setDisabled(False)

    #输出log到GUI文本框
    def output_log(self, str):
        self.ui.textBrowser.append(str)

    def read_config_file(self):
        #读取项目名称
        self.project_name = self.conf.get_project_name()
        if (self.project_name!=None):
            self.ui.project_name_label.setText(self.project_name)
        else:
            self.ui.project_name_label.setText('默认名称')
        #读取源文件夹路径
        src_str_prefix = '源文件夹： '
        self.src_folder_path = self.conf.get_src_folder_path()
        if (self.src_folder_path != None):
            src_str = src_str_prefix + self.src_folder_path
            self.ui.src_floder_label.setText(src_str)
        # 读取目标文件夹路径
        dst_str_prefix = '目标文件夹： '
        self.dst_folder_path = self.conf.get_dst_folder_path()
        if (self.dst_folder_path != None):
            dst_str = dst_str_prefix + self.dst_folder_path
            self.ui.dst_floder_label.setText(dst_str)

class configure():
    home_path = None
    project_name = None
    src_folder_path = None
    dst_folder_path = None
    config_file_name = 'default.ini'

    def __init__(self):
        self.home_path = os.path.expandvars('%USERPROFILE%')
        os.chdir(self.home_path)
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.config_file_name)
            self.check_config()
            logging.debug(':check config success!')
        except Exception as e:
            logging.debug(e)
            self.create_blank_config_file()

    def create_blank_config_file(self):
        os.chdir(self.home_path)
        # add section / set option & key
        self.conf.add_section("project_name")
        self.conf.set("project_name", "project_name", "")
        self.conf.add_section("folder_path")
        self.conf.set("folder_path", "src_folder_path", "")
        self.conf.set("folder_path", "dst_folder_path", "")
        # write to file
        with open("default.ini", "w+") as f_config:
            self.conf.write(f_config)

    def get_project_name(self):
        return self.project_name

    def set_project_name(self, user_set_project_name):
        os.chdir(self.home_path)

        self.conf.set("project_name", "project_name", user_set_project_name)
        with open("default.ini", "w") as f_config:
            self.conf.write(f_config)

    def get_src_folder_path(self):
        return self.src_folder_path

    #在配置文件中更新源文件夹路径
    def set_src_folder_path(self, user_set_dst_path):
        os.chdir(self.home_path)
        self.conf.set("folder_path", "src_folder_path", user_set_dst_path)
        #写回配置文件
        with open("default.ini", "w") as f_config:
            self.conf.write(f_config)

    def get_dst_folder_path(self):
        return self.dst_folder_path

    # 在配置文件中更新目标文件夹路径
    def set_dst_folder_path(self, user_set_dst_path):
        os.chdir(self.home_path)
        self.conf.set("folder_path", "dst_folder_path", user_set_dst_path)
        # 写回配置文件
        with open("default.ini", "w") as f_config:
            self.conf.write(f_config)

    def check_config(self):
        self.project_name = self.conf.get("project_name","project_name")
        self.src_folder_path = self.conf.get("folder_path", "src_folder_path")
        #logging.debug('self.src_folder_path is ',self.src_folder_path)
        self.dst_folder_path = self.conf.get("folder_path", "dst_folder_path")

class function(QThread):
    progress = 0
    dir_to_be_deleted = None
    finish_list = str
    #声明一个进度信号，返回int型执行进度
    progress_signal = pyqtSignal(int)
    # 声明一个结束信号，同时返回一str
    finish_signal = pyqtSignal(str)
    # 构造函数里增加形参
    def __init__(self, src_d, dst_d, parent=None):
        super(function, self).__init__(parent)
        # 储存参数
        self.src_folder = src_d
        self.dst_folder = dst_d

    def run(self):
        logging.debug('enter child thread')
        #检查传入的源文件夹和目标文件夹是否正确
        if (self.check_dir(self.src_folder)):
            if(self.check_dir(self.dst_folder)):
                #获取源文件夹中的最新对象
                object_latest = get_latest_object(self.src_folder)
                #最新的对象是文件夹
                if(os.path.isdir(object_latest)):
                    logging.debug('start copy with progress')
                    try:
                        #目标目录没有同名文件
                        if(self.no_dir_name_repetition(object_latest, self.dst_folder)):
                            logging.debug('no the same name ')
                            self.copy_dir_with_proress(object_latest, self.dst_folder)
                            logging.debug('emit success signal')
                            # 结束计算进度线程，显示进度100%
                            self.finish_signal('end_with_success')
                        else:
                            logging.debug('have the same name')
                            self.finish_signal.emit('dir_name_repetition')
                            return
                    except Exception as e:
                        logging.error(e)
                    finally:
                        logging.debug('end copy_dir_with_proress')

                #最新的对象是文件时
                elif(os.path.isfile(object_latest)):
                    pass
                    #TODO
                #源文件夹为空
                elif(len(object_latest == 0)):
                    self.finish_signal.emit('src_dir_is_empty')
                else:
                    self.finish_signal.emit('unknown_error')
            else:
                self.finish_signal.emit('dst_dir_not_correct')
                return

        else:
            self.finish_signal.emit ('src_dir_not_correct')
            return

        self.finish_signal.emit('end_with_success')

    # last_object = self.get_latest_dir(self.src_folder)
    # if(os.path.isdir(last_object)):
    #     pass
    # else:
    #     return

    # 检查文件夹
    def check_dir(self, dir):
            logging.debug('project dir set by user is %s' % dir)
            if os.path.isdir(dir):
                logging.debug('dir set by user is correct!')
                return True
            else:
                logging.error('dir set by user is not correct!')
                return False

    # 检查有无同名文件夹
    def no_dir_name_repetition(self, src_dir, dst_dir):
        real_name = os.path.split(src_dir)[1]
        logging.debug('real_name is %s' % real_name)
        for file_name in os.listdir(dst_dir):
            if(file_name == real_name):
                return False

        return True


    # 拷贝文件夹至文件夹并显示进度
    def copy_dir_with_proress(self, src_dir, dst_dir):
        logging.debug(src_dir)
        logging.debug(dst_dir)
        # 启动计算进度线程
        cal_thread = calculate_progress(src_dir, dst_dir)
        cal_thread.progress_signal.connect(self.set_progress)
        cal_thread.start()

        #复制目录
        try:
            logging.debug('start copytree')
            dir_name = os.path.split(src_dir)[1]
            logging.debug(dir_name)
            abs_dir_path = os.path.join(dst_dir, dir_name)
            logging.debug(abs_dir_path)
            shutil.copytree(src_dir, abs_dir_path)
            logging.debug('end copytree')
            #TODO
            cal_thread.complete()
            cal_thread.wait()
            return
        except Exception as e:
            logging.debug('shuitil error')
            logging.debug(e)
            #TODO
            #弹窗报警


    def copy_file_with_progress(self):
        pass
        #TODO

    def set_progress(self, value):
        self.progress = value
        self.progress_signal.emit(self.progress)


#计算进度线程，实际上不停的获取目标文件夹大小，除以源文件夹大小，返回结果
class calculate_progress(QThread):
    # 声明一个进度信号，返回int型执行进度
    progress_signal = pyqtSignal(int)
    re_src_dir = None
    re_dst_dir = None
    src_dir_size = 0
    dst_dir_size = 0
    complete_flag = False

    def __init__(self, src_dir, dst_dir, parent=None):
        super(calculate_progress, self).__init__(parent)
        # 接收参数
        self.re_src_dir = src_dir
        self.re_dst_dir = dst_dir
        self.src_dir_size = getdirsize(self.re_src_dir)
        logging.debug(self.src_dir_size)
        logging.debug('cal_thread init finished')

    def run(self):
        logging.debug('enter run method')
        try:
            self.loop()
        except Exception as e:
            logging.debug(e)

    def loop(self):
        logging.debug('Enter loop-----------')
        while (self.complete_flag == False):
            self.dst_dir_size= getdirsize(self.re_dst_dir)
            time.sleep(0.5)
            progress = self.dst_dir_size / self.src_dir_size * 100
            logging.debug('progress is %d' % progress)
            self.progress_signal.emit(progress)

    def complete(self):
        self.complete_flag = True

# 获取项目文件夹内最新文件或文件夹
def get_latest_object(project_dir):
    lists = os.listdir(project_dir)  # 列出目录的下所有文件和文件夹保存到lists
    logging.debug(list)
    lists.sort(key=lambda fn: os.path.getmtime(project_dir + "\\" + fn))  # 按时间排序
    object_latest = os.path.join(project_dir, lists[-1])  # 获取最新的文件保存到object_latest
    logging.debug(object_latest)
    return object_latest

# 获取文件夹内所有文件大小
def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())