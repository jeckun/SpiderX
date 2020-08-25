#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
webpage: 用于代表网页的元素和对网页的基本操作。
例如获取网页上的某个信息，或者列表。下载图片文件，打开链接等。
"""
import os
import re
import requests
from urllib.parse import urlparse
from Spider001.config import BASE_DIR


class Page(object):
    _hostname = ''
    _title = ''
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
        if name[len(name) - 4: len(name)] == '.txt':
            with open(name, 'w') as file:
                file.write(content)
        elif name[len(name) - 4: len(name)] == '.jpg':
            with open(name, 'wb') as file:
                file.write(content)

    def getText(self, point):
        return self.spider.get_a_text(self, point)

    def getImg(self, point):
        url = self.getfullpath(self.spider.get_img_src(self, point))
        re = requests.get(url, headers=self.spider._headers, timeout=5)
        self.save('Logo.jpg', re.content)

    def getHref(self, point):
        return self.getfullpath(self.spider.get_a_href(self, point))

    def getCatalogList(self, point):
        l = self.spider.get_page_list(self, point)
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
    # _title = ''
    _author = ''
    _time = ''
    _state = ''
    _number = ''
    _introduction = ''  # 介绍
    _cover = ''  # 封面
    _catalog = ''  # 目录
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
            if os.path.isfile(name + '.txt'):
                print('已经下载: %s' % name)
                continue
            else:
                try:
                    self.load(path)
                    self.save(name + '.txt', self.getText(point))
                except Exception as e:
                    print(e)
                    continue
