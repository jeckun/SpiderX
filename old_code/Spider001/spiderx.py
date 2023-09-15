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
from Spider001.config import header
from Spider001.books import Book
from bs4 import BeautifulSoup
from lib.public import url_verification, start_with, \
    file_extension, thread_run, check_save_path
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
        # 检查下载路径，如果不存在就创建一个
        if self.page.title == '':
            raise ValueError('缺少书名！请添加title值。')
        check_save_path(self.page.title)

        print('开始下载: ', self.page.title)
        # 每次启动5个线程，下载5个链接的章节
        n = len(spider_list)
        for i in range(0, n, 5):
            thread_run(self.save_txt_to_file, spider_list[i:i + 5], selector)
            print('下载进度：%.2f%%' % (i/n * 100))
        return

    @staticmethod
    def save_txt_to_file(filename, url, selector):

        if os.path.isfile(filename):
            return

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
            print('下载失败...', e)
            return False

        with open(filename, tag) as f:
            f.write(content)

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
