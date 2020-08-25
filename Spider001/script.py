#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
script: 用于进行脚本解析和执行
"""


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
