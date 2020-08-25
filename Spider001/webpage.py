#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
webpage: 用于代表网页的元素和对网页的基本操作。
例如获取网页上的某个信息，或者列表。下载图片文件，打开链接等。
"""
import os

from Spider001.config import bookInf, BASE_DIR
from lib.public import file_extension


class Page(object):
    _host = ''  # 网站主机域名
    _scheme = ''  # 链接协议
    _path = ''  # 网页所在路径
    _title = ''  # 网站主题或者图书的标题
    _url = ''  # 具体网址
    content = None  # 网址内容
    spider = None  # 关联爬虫

    def __init__(self, spider, href):
        self._url = href
        self.spider = spider

    def __str__(self):
        return self._host

    def load(self, url=''):
        if url:
            self._url = url
        self.spider.load(self)

    def save(self, filename, content):
        # 保存内容之前先检查本地是否有缓存的目录
        path = os.path.join(BASE_DIR, self._title)
        if not os.path.isdir(path):
            os.makedirs(path)
        os.chdir(path)

        print('保存文件:', filename)
        if file_extension(filename) == '.txt':
            with open(filename, 'w') as file:
                file.write(content)
        elif file_extension(filename) == '.jpg':
            with open(filename, 'wb') as file:
                file.write(content)

    def get_text(self, point):
        return self.spider.get_a_text(self, point)

    def get_img(self, point):
        url = self.spider.get_full_path(self.spider.get_img_src(self, point))
        self.save('logo.jpg', self.spider.get_page_content(url))

    def get_href(self, point):
        return self.spider.get_full_path(self.spider.get_a_href(self, point))

    def get_catalog_list(self, point):
        l = self.spider.get_page_list(self, point)
        return [[name, self.spider.get_full_path(url)] for name, url in l]


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

    def __init__(self, spider, inf=None):
        if not inf:
            self._bookinf = bookInf
        else:
            self._bookinf = inf
        self.spider = spider
        # super().__init__(spider, self._bookinf['url'])

    def getCatalogHref(self, point):
        self._catalog = self.get_href(point)

    def getbaseinf(self, baseinf):
        for item in baseinf:
            setattr(self, item, self.get_text(baseinf[item]))

    def getCover(self, point):
        self.get_img(point)

    def getCatalog(self):
        self.load(self._catalog)
        self._author = self.get_text(self._bookinf['author'])
        self._catalog_list = self.get_catalog_list(self._bookinf['catalog_list'])

    def getChapter(self, point):

        print('开始下载章节')
        for name, path in self._catalog_list:
            if os.path.isfile(name + '.txt'):
                print('已经下载: %s' % name)
                continue
            else:
                try:
                    self.load(path)
                    self.save(name + '.txt', self.get_text(point))
                except Exception as e:
                    print(e)
                    continue
