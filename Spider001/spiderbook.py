#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-26

"""
SpiderBook: 用于建立到Web服务器的链接，请求资源，解析数据，执行脚本
"""
import requests
import time
import os
import random
from Spider001.config import header
from Spider001.books import Book
from lib.spiderx import Spider
from bs4 import BeautifulSoup
from lib.public import url_verification, start_with, \
    file_extension, thread_run, check_save_path
from urllib.parse import urlparse


class SpiderBook(Spider):
    def __init__(self):
        self.page = Book()

    def download_list(self, spider_list, selector):
        # 检查下载路径，如果不存在就创建一个
        if self.page.title == '':
            raise ValueError('缺少书名！请添加title值。')
        super().download_list(spider_list, selector)



