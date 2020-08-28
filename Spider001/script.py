#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
script: 用于进行脚本解析和执行，以及加载脚本，校验脚本。
"""
from lib.public import first_word, url_verification
from Spider001.books import Book


class Script(object):
    def __init__(self, filepath, spider):
        self.filepath = filepath
        self.spider = spider
        self.book = Book()

    def run(self):
        print('Ready go!')
        with open(self.filepath) as f:
            for line1 in f:
                cmd = line1.replace('\n', '')
                self.__parse__(cmd)

    def __parse__(self, cmdline):
        """
        解析命令行，并且执行
        :param cmd: 命令行文本
        :return:
        """
        cmd = first_word(cmdline).lower()
        if hasattr(self.spider, cmd):
            if cmd == 'load':
                url = cmdline[-(len(cmdline)-len(cmd)):].replace(' ','')
                if url_verification(url):
                    setattr(self.spider.page, 'path', url)
                else:
                    url = getattr(self.spider.page, url)
                print('执行:', cmd, url)
                self.spider.load(url)
            if cmd in ('get_a_text', 'get_a_href', 'get_a_list'):
                fun = getattr(self.spider, cmd)
                cmdline = cmdline[-(len(cmdline)-len(cmd)):]
                selector, x = cmdline.split(' to ')
                print('执行:', cmd, selector, 'to', x)
                setattr(self.spider.page, x, fun(selector))
            if cmd == 'download_list':
                fun = getattr(self.spider, cmd)
                cmdline = cmdline[-(len(cmdline)-len(cmd)):]
                selector, x = cmdline.split(' in ')
                print('执行:', cmd, x)
                fun(getattr(self.spider.page, x), selector=selector)
            elif cmd == 'quit':
                print('end.')
        return
