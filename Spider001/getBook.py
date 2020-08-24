#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-19

"""
Spider: 代表爬虫的行为，包括获取网页，解析网页
page: 代表网页的属性及操作，属性包括域名、网址、网页内容、列表，操作包括保存数据
Book：代表图书的属性及操作，属性包括书名、作者、状态、字数等，操作包括下载图书
Script: 代表的是解析自定义脚本
"""

import os
import re
import sys
import time
import random
import requests
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse
from config import header, bookInf, script

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Spider(object):
    _headers = ''
    _session = requests.Session()

    def __init__(self, headers):
        self._headers = headers
        # 设置重试次数为3次
        self._session.mount('http://', HTTPAdapter(max_retries=3))
        self._session.mount('https://', HTTPAdapter(max_retries=3))

    def load(self, page):
        try:
            response = self._session.get(page._url, headers=self._headers, timeout=5)
            page.content = bs(response.content, "lxml")
            time.sleep(random.randint(1, 10))
            return True
        except requests.exceptions.ConnectionError as e:
            print('连接失败，请检查网络或者因访问过于频繁被屏蔽了...')
            return False

    def getText(self, page, point):
        if point:
            doc = page.content.select(point)
            return doc[0].text
        else:
            return ''

    def getImgSrc(self, page, point):
        if point:
            doc = page.content.select(point)
            return doc[0]['src']
        else:
            return ''

    def getHref(self, page, point):
        if point:
            doc = page.content.select(point)
            return doc[0]['href']
        else:
            return ''

    def getCatalogList(self, page, point):
        return [[l.text.replace('\r', '').replace('\n', '').replace('\t', ''),
                 l['href'][1:]] for l in page.content.select(point)]


class Page(object):
    _hostname = ''
    _url = ''
    content = None
    spider = None

    def __init__(self, href, spider):
        self._url = href
        self._hostname = urlparse(self._url).hostname
        self.spider = spider

    def __str__(self):
        return self._hostname

    def load(self, url=''):
        if url:
            self._url = url
        self.spider.load(self)

    def save(self, name, content):

        path = os.path.join(BASE_DIR, self._title)
        if not os.path.isdir(path):
            os.makedirs(path)
        os.chdir(path)

        print('保存文件:', name)
        if name[len(name)-4: len(name)] == '.txt':
            with open(name+'.txt', 'w') as file:
                file.write(content)
        elif name[len(name)-4: len(name)] == '.jpg':
            with open(name, 'wb') as file:
                file.write(content)

    def getText(self, point):
        return self.spider.getText(self, point)

    def getImg(self, point):
        url = self.getfullpath(self.spider.getImgSrc(self, point))
        re = requests.get(url, headers=self.spider._headers, timeout=5)
        self.save('Logo.jpg', re.content)

    def getHref(self, point):
        return self.getfullpath(self.spider.getHref(self, point))

    def getCatalogList(self, point):
        l = self.spider.getCatalogList(self, point)
        return [[name, self.getfullpath(url)] for name, url in l]

    def getfullpath(self, path):
        if not re.match(r'^http\w*', path):
            if re.match(r'^//\w*', path):
                return 'http:' + path
            elif re.match(r'^/\w*', path):
                return 'http://' + self._hostname + path
            else:
                return 'http://' + self._hostname + '/' + path


class Books(Page):
    _title = ''
    _author = ''
    _time = ''
    _state = ''
    _number = ''
    _introduction = ''   # 介绍
    _cover = ''   # 封面
    _catalog = ''   # 目录
    _catalog_list = None
    _bookinf = None

    def __init__(self, inf, spider):
        super().__init__(inf['url'], spider)
        self._bookinf = inf

    def getCatalogHref(self, point):
        self._catalog = self.getHref(point)

    def getbaseinf(self, baseinf):
        for item in baseinf:
            setattr(self, item, self.getText(baseinf[item]))

    def getCover(self, point):
        self.getImg(point)

    def getCatalog(self):
        self.load(self._catalog)
        self._author = self.getText(self._bookinf['author'])
        self._catalog_list = self.getCatalogList(self._bookinf['catalog_list'])

    def getChapter(self, point):

        print('开始下载章节')
        for name, path in self._catalog_list:
            if os.path.isfile(name+'.txt'):
                print('已经下载: %s' % name)
                continue
            else:
                try:
                    self.load(path)
                    self.save(name+'.txt', self.getText(point))
                except Exception as e:
                    print(e)
                    continue


class Script(object):
    _script = None
    _page = None

    def __init__(self, script=None, page=None):
        self._script = script
        self._page = page

    def run(self):
        self.__runScript__(self._script)

    def __runScript__(self, dicts):
        for i in dicts:
            # print(i, dicts[i])
            if i == 'openHome':
                self._page.load(dicts[i])
            elif i == 'getText':
                self._page.getbaseinf(dicts[i])
            elif i == 'getImg':
                self._page.getCover(dicts[i]['_cover'])
            elif i == 'getHref':
                self._page.getCatalogHref(dicts[i]['_catalog'])
            elif i == 'openCatalog':
                self._page.getCatalog()
            elif i == 'getChapter':
                self._page.getChapter(dicts[i])
            else:
                pass
        return


def main(args):
    sp = Spider(header)
    bk = Books(bookInf, sp)
    sc = Script(script, bk)
    sc.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
