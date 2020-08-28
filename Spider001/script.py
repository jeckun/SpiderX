#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
script: 用于进行脚本解析和执行，以及加载脚本，校验脚本。
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
                self._page.get_base_inf(dicts[i])
            elif i == 'getImg':
                self._page.get_cover(dicts[i]['_cover'])
            elif i == 'getHref':
                self._page.get_catalog_href(dicts[i]['_catalog'])
            elif i == 'openCatalog':
                self._page.get_catalog()
            elif i == 'getChapter':
                self._page.get_chapter(dicts[i])
            else:
                pass
        return
