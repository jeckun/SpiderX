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
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs


class Spider(object):
    _headers = ''
    _session = requests.Session()

    def __init__(self, headers):
        self._headers = headers
        # 设置重试次数为3次
        self._session.mount('http://', HTTPAdapter(max_retries=3))
        self._session.mount('https://', HTTPAdapter(max_retries=3))

    def load(self, page):
        # 打开网页，使用BS4进行解析
        try:
            response = self._session.get(page._url, headers=self._headers, timeout=5)
            page.content = bs(response.content, "lxml")
            time.sleep(random.randint(1, 10))
            return True
        except requests.exceptions.ConnectionError as e:
            print('连接失败，请检查网络或者因访问过于频繁被屏蔽了...', e)
            return False

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
