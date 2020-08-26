#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-26

"""
Spider: 用于建立到Web服务器的链接，请求资源，解析数据，执行脚本
"""
import requests
import time
import random
from Spider001.config import header
from bs4 import BeautifulSoup
from lib.public import url_verification, start_with
from urllib.parse import urlparse


class Spider(object):
    def __init__(self):
        self.response = None
        self.content = None
        self.urlparse = None
        self.page = None

    def load(self, url):
        if url_verification(url):
            self.urlparse = urlparse(url)
            self.response = requests.get(url, headers=header, timeout=3)
            self.content = BeautifulSoup(self.response.content, "lxml")
            time.sleep(random.randint(0, 3))

    def download(self, spider_list):
        """
        开启多线程下载
        :param spider_list: 需要下载的任务列表
        :return:
        """
        print('开始下载...', spider_list)
        return

    def quit(self):
        return

    def get_a_text(self, selector):
        return self.content.select(selector)[0].text.replace('\r', '').replace('\n', '').replace('\t', '')

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
