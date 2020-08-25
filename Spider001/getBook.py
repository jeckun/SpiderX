#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-19

"""
Spider: 代表爬虫的行为，包括获取网页，解析网页
page: 代表网页的属性及操作，属性包括域名、网址、网页内容、列表，操作包括保存数据
Book：代表图书的属性及操作，属性包括书名、作者、状态、字数等，操作包括下载图书
Script: 代表的是解析和执行自定义脚本
header: 是链接目标网站所需要的http头
bookInf： 是目标网站关键节点的位置信息
script： 是需要执行的脚本
"""

import sys

from Spider001.config import header, bookInf, script
from Spider001.spider import Spider
from Spider001.webpage import Books
from Spider001.script import Script


def main(args):
    sp = Spider(header)
    bk = Books(bookInf, sp)
    sc = Script(script, bk)
    sc.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
