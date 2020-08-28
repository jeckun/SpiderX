#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-26

"""
Spider: 用于建立到Web服务器的链接，请求资源，解析数据，执行脚本
"""
import requests
import time
import os
import random
import threading
from Spider001.config import header, BASE_DIR
from Spider001.books import Book
from bs4 import BeautifulSoup
from lib.public import url_verification, start_with, file_extension
from urllib.parse import urlparse


class Spider(object):
    def __init__(self):
        self.response = None
        self.content = None
        self.urlparse = None
        self.page = Book()

    def load(self, url):
        if url_verification(url):
            self.urlparse = urlparse(url)
            self.response = requests.get(url, headers=header, timeout=3)
            self.content = BeautifulSoup(self.response.content, "lxml")
            time.sleep(random.randint(0, 3))
            return self.content

    def download_list(self, spider_list, selector):
        """
        开启多线程下载
        :param spider_list: 需要下载的任务列表
        :return:
        """

        # 检查下载路径，如果不存在就创建一个
        self.check_save_path()

        print('开始下载: ', self.page.title)
        # 每次启动5个线程，下载5个链接的章节
        for i in range(0, len(spider_list), 5):
            self.run(spider_list[i:i + 5], selector)
        return

    def run(self, lst, selector):
        '''
        用线程执行下载任务
        :param lst: 需要执行的任务列表
        :param selector: 需要截取信息的路径
        :return:
        '''

        thread_list = []

        # 创建线程
        for i in lst:
            filename = i[0] + '.txt'
            url = i[1]
            thd = threading.Thread(target=self.save_file,
                                   args=(filename, url, selector))
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

    @staticmethod
    def save_file(filename, url, selector):

        if os.path.isfile(filename):
            print(threading.current_thread().name, ' 已经下载: ', filename)
            return
        else:
            print(threading.current_thread().name, '正在下载：', filename)

        if file_extension(filename) == '.txt':
            tag = 'w'
        elif file_extension(filename) == '.jpg':
            tag = 'wb'
        else:
            tag = 'w'

        try:
            response = requests.get(url, headers=header, timeout=3)
            content = BeautifulSoup(response.content, "lxml")
            content = content.select(selector)[0].text
            time.sleep(random.randint(0, 3))
        except requests.exceptions.ConnectionError as e:
            print(threading.current_thread().name, '连接失败...', e)
            return False

        with open(filename, tag) as f:
            f.write(content)

    def check_save_path(self):
        if self.page.title == '':
            raise ValueError('缺少书名！请添加title值。')
        path = os.path.join(BASE_DIR, self.page.title)
        if not os.path.isdir(path):
            os.makedirs(path)
        os.chdir(path)

    # @staticmethod
    # def save(filename, content):
    #     if os.path.isfile(filename):
    #         print('已经下载: ', filename)
    #         return
    #     else:
    #         print('正在下载：', filename)
    #     if file_extension(filename) == '.txt':
    #         tag = 'w'
    #     elif file_extension(filename) == '.jpg':
    #         tag = 'wb'
    #     else:
    #         tag = 'w'
    #     with open(filename, tag) as f:
    #         f.write(content)

    def quit(self):
        return

    def get_a_text(self, selector):
        return self.content.select(selector)[0].text.replace('\r', '').replace('\n', '').replace('\t', '')

    def get_a_content(self, selector):
        return self.content.select(selector)[0].text

    def get_a_href(self, selector, tag='href'):
        cnt = self.content.select(selector)
        return self.get_full_path(cnt[0][tag].replace(' ', ''))

    def get_img_src(self, selector):
        return self.get_a_href(selector, tag='src')

    def get_a_list(self, selector):
        return [[ls.text.replace('\r', '').replace('\n', '').replace('\t', ''),
                 self.get_full_path(ls['href'][1:])] for ls in self.content.select(selector)]

    def get_full_path(self, path):
        if not url_verification(path):
            if start_with(r'//', path):
                return self.urlparse.scheme + ':' + path
            elif start_with(r'/', path):
                return self.urlparse.scheme + '://' + self.urlparse.netloc + path
            else:
                return self.urlparse.scheme + '://' + self.urlparse.netloc + '/' + path
