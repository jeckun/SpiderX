#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-7-20
"""
用类的方式实现小说网站的文章爬取，通过爬虫、文章、脚本三个对象来实现，最终希望达到对于
大多数小说类网站，可以通过配置脚本，自动的、定时的到指定网站爬取小说到本地。

爬虫：负责在指定位置爬取指定内容，并且保存到指定位置。
文章：提供文章所在网页，文章结构（标题、作者、发表日期、字数、章节列表、文章内容是否分
页、文章内容）
脚本：提供是下载一篇文章，还是一批文章。
"""

import os
import sys
import time

import requests
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter


class WebPage(object):
    _server = ''
    path = ''
    title = ''
    Page = None
    BookList = None
    ArticleList = None
    Content = ''

    def __init__(self, host=None):
        self._server = host

    def server(self):
        return self._server

    def save(self, filename):
        with open(filename+'.txt', 'w') as f:
            f.write(self.Content)
            f.close()


class Spider(object):
    _page = WebPage
    _server = ''
    _path = ''
    _soup = ''
    _headers = ''
    _session = requests.Session()

    def __init__(self, page):
        self._page = page
        self._server = page.server()
        self._headers = {
            'authority': self._server,
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': '__cfduid=da0ea26ad2366e26201436a2efd72f5b41594285210; UM_distinctid=17332cdbe6c3d0-0c8b190c89c1af-31627404-13c680-17332cdbe6d5ad; PHPSESSID=f6e2k75tki314kapp2k495bri1; hmruser=20200709224719236396; CNZZDATA1277837046=1663175939-1594303324-https%253A%252F%252Fwww.diyibanzhu555.com%252F%7C1595080808; CNZZDATA1277811490=8805732-1594284673-https%253A%252F%252Fnote.youdao.com%252F%7C1595084201; CNZZDATA1270517892=1564485302-1594302259-https%253A%252F%252Fwww.diyibanzhu555.com%252F%7C1595079861',
        }

        self._session.mount('http://', HTTPAdapter(max_retries=3))  # 设置重试次数为3次
        self._session.mount('https://', HTTPAdapter(max_retries=3))

    def open(self, path, page):
        self._path = path
        try:
            response = self._session.get(self._server + path, headers=self._headers, timeout=5)
            page.Page = bs(response.content, "lxml")
            time.sleep(10)
            return True
        except requests.exceptions.ConnectionError as e:
            print('连接失败，请检查网络或者因访问过于频繁被屏蔽了...')
            return False

    def getlist(self, point=None):
        return [[l.text, l['href'][1:]] for l in self._page.Page.select(point)]

    def getdoc(self, point=None):
        doc = self._page.Page.select(point)
        return doc[0].text

    def getcontent(self, page, point=None):
        for i in page.ArticleList:
            print('open', page.title + ' 之 ' + i[0])
            if os.path.exists(page.title + '/' + page.title + '-' + i[0] + '.txt'):
                continue
            if not self.open(i[1], page):
                break
            page.Content += page.title + ' 之 ' + i[0] + '\n\n'
            page.Content += self.getdoc(point)
            page.save('资料/' + page.title + '/' + page.title + '-' + i[0])
            page.Content = ''


class Script(object):
    def __init__(self, script):
        self._cmd = script

    def execute(self):
        for cmd in self._cmd:
            print(cmd[0] + ' : ' + cmd[1])
            if cmd[0] == 'host':
                pg = WebPage(cmd[1])
            elif cmd[0] == 'open':
                sp = Spider(pg)
                if not sp.open(cmd[1], pg):
                    break
            elif cmd[0] == 'getlist':
                pg.BookList = sp.getlist(cmd[1])
            elif cmd[0] == 'circlelist':
                for pg.title, pg.path in pg.BookList:
                    if sp.open(pg.path, pg):
                        if not os.path.exists(pg.title):
                            os.makedirs(pg.title)
                        pg.ArticleList = sp.getlist(cmd[1])
                        sp.getcontent(pg, cmd[2])
        return


def main(args):
    print('main start')

    scp = [['host', 'http://www.tetewx.com/'],
           # ['open', 'all/'],
           # ['getlist', 'div.novellist ul li a'],
           ['open', 'index/1-1.html'],
           ['getlist', 'div#newscontent div.r ul li a'],
           ['circlelist', 'div#list dl dd a.f-green', 'div#bgdiv div#content p'],
           ]

    script = Script(scp)
    script.execute()

    pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
