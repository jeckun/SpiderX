#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
这里是一些公共函数库
"""

import os
import re
import threading
from Spider001.config import BASE_DIR


# 获得文件扩展名
def file_extension(path):
    return os.path.splitext(path)[1]


# 获得文件名
def file_name(path):
    return os.path.splitext(path)[0]


# 检查存储目录
def check_save_path(title):
    path = os.path.join(BASE_DIR, title)
    if not os.path.isdir(path):
        os.makedirs(path)
    os.chdir(path)


# 验证url是否以http/https开头
def url_verification(url):
    return re.match(r'^(?:http)s?://\w*', url)


# 验证字符串是否以，指定标记开头
def start_with(tag, str):
    return re.match(r'^' + tag + r'\w*', str)


# 获取字符串第一个单词
def first_word(string):
    return string.split(' ', 1)[0]


# 多线程方式执行一个列表的任务
def thread_run(fun, task_list, args=None):
    '''
    开启多线程执行任务
    :param fun: 这是需要执行下载的函数名称，不需要带括号和参数。
    :param task_list:  这个参数必须是一个列表，
    只有两列，第一列需要下载的对象的名字，也就是保存是否的文件名。
    第二列是下载的网址。
    :param args:  这个参数是执行下载的函数的参数。
    :return:
    举例： thread_run(save_file, catalog_list, selector)
    '''
    thread_list = []

    # 创建线程
    for i in task_list:
        filename = i[0] + '.txt'
        url = i[1]
        thd = threading.Thread(target=fun,
                               args=(filename, url, args))
        # target参数为线程开始执行的入口
        # args参数为执行函数的参数列表，是一个元组结构
        # 可以通过这个带入线程需要接受的参数列表。
        thread_list.append(thd)

    # 启动线程
    for thd in thread_list:
        # 设定子线程为守护线程
        # 使用setDaemon(True)，设置子线程为守护线程时，主线程一旦执行结束，
        # 则全部线程全部被终止执行，
        thd.setDaemon(True)
        thd.start()

    # 阻塞主线程到子线程执行结束
    for thd in thread_list:
        # join所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，
        # 一直等待其他的子线程执行结束之后，主线程在终止。
        thd.join()

    return
