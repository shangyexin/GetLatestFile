# Create by yasin   Date:2017-12-26
# -*- coding: UTF-8 -*-

import os
import shutil
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    )

PROJECT_DIR_BY_USER = r'\\192.168.20.4\Project_Release\CN202S-B_Release\LV3\NO_HAMAN'
DEST_DIR = r'F:\download_test'

#从GUI获取项目文件夹
def get_project_dir(project_dir_by_user):
    pass

#设置项目文件夹
def set_project_dir(project_dir):
    logging.debug('project dir set by user is %s' % project_dir)
    if os.path.exists(project_dir):
        logging.debug('project dir set by user is existed!')
        return project_dir
    else:
        logging.error('project dir set by user is not existed!')
        exit()

#设置目标文件夹
def set_dest_dir(des_file_dir):
    if os.path.exists(des_file_dir):
        if os.path.isdir(des_file_dir):
            logging.info('%s is already existed,do not need create!' % des_file_dir)
        else:
            logging.error('%s is not a directory' % des_file_dir)
            exit()
    else:
        logging.debug('%s is not existed' % des_file_dir)
        os.makedirs(des_file_dir)
        logging.debug('create %s success!' % des_file_dir)

# 获取项目文件夹内最新文件夹
def get_latest_dir(project_dir):
    lists = os.listdir(project_dir)                                            #列出目录的下所有文件和文件夹保存到lists
    logging.debug(list)
    lists.sort(key=lambda fn: os.path.getmtime(project_dir + "\\" + fn))     #按时间排序
    directory_latest = os.path.join(project_dir, lists[-1])                   #获取最新的文件保存到directory_latest
    logging.debug(directory_latest)
    return directory_latest

# 下载文件夹
def download_file(src_dir, des_dir):
    path, dir = os.path.split(src_dir)
    dest_dir_abs = des_dir + os.path.sep + dir                          #目标文件绝对路径
    logging.debug('dest_dir is %s' % dest_dir_abs)
    if os.path.exists(dest_dir_abs):
        logging.warning('%s is already existed, do not need update!' % dest_dir_abs)
        return
    else:
        shutil.copytree(src_dir, dest_dir_abs)                           # 复制文件

def main():
    logging.debug('Welcome to use update package download tool!')

    project_dir = set_project_dir(PROJECT_DIR_BY_USER)               #设置项目文件夹
    set_dest_dir(DEST_DIR)                                           #设置目标文件夹

    src_dir = get_latest_dir(project_dir)                            #获取项目文件夹内最新日期文件夹
    download_file(src_dir,DEST_DIR)                                  #下载文件到指定目录

    logging.debug('Everything is ok, goodbye!')


if __name__ == '__main__':
    main()