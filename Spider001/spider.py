#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-25

"""
Spider: 用于建立到Web服务器的链接，请求资源，解析返回数据
"""


import requests
import random
import time
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs
from Spider001.config import header
from lib.public import url_verification, start_with


class Spider(object):
    _headers = ''
    _urlparse = None
    _session = requests.Session()

    def __init__(self, headers=None):
        if not headers:
            self._headers = header
        else:
            self._headers = headers
        # 设置重试次数为3次
        self._session.mount('http://', HTTPAdapter(max_retries=3))
        self._session.mount('https://', HTTPAdapter(max_retries=3))

    def load(self, page):
        try:
            # 检查网页的地址是否正确
            if not page._url:
                raise ValueError("网址不能为空！")
            self._urlparse = urlparse(page._url)
            if not self._urlparse:
                raise ValueError("网址不合规!")
            else:
                page._scheme = self._urlparse.scheme
                page._host = self._urlparse.netloc
                page._path = self._urlparse.path
            # 打开网页
            # response = self._session.get(page._url, headers=self._headers, timeout=5)
            page.content = bs(self.get_page_content(page._url), "lxml")
            # time.sleep(random.randint(1, 10))
            return True
        except requests.exceptions.ConnectionError as e:
            print('连接失败...', e)
            return False

    def get_page_content(self, url):
        # 打开网页
        response = self._session.get(url, headers=self._headers, timeout=5)
        time.sleep(random.randint(1, 10))
        return response.content

    def get_a_text(self, page, point):
        if point:
            doc = page.content.select(point)
            return doc[0].text.replace('\r', '').replace('\n', '').replace('\t', '')

    def get_img_src(self, page, point):
        if point:
            doc = page.content.select(point)
            return doc[0]['src']
        else:
            return ''

    def get_a_href(self, page, point):
        if point:
            doc = page.content.select(point)
            return doc[0]['href']
        else:
            return ''

    def get_page_list(self, page, point):
        return [[l.text.replace('\r', '').replace('\n', '').replace('\t', ''),
                 l['href'][1:]] for l in page.content.select(point)]

    def get_full_path(self, path):
        if not url_verification(path):
            if start_with(r'//', path):
                return self._urlparse.scheme + ':' + path
            elif start_with(r'/', path):
                return self._urlparse.scheme + '://' + self._urlparse.netloc + path
            else:
                return self._urlparse.scheme + '://' + self._urlparse.netloc + '/' + path