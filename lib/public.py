#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time:2020-8-25

"""
这里是一些公共函数库
"""

import os
import re


# 获得文件扩展名
def file_extension(path):
    return os.path.splitext(path)[1]


# 获得文件名
def file_name(path):
    return os.path.splitext(path)[0]


# 验证url是否以http/https开头
def url_verification(url):
    return re.match(r'^(?:http)s?://\w*', url)


# 验证字符串是否以，指定标记开头
def start_with(tag, str):
    return re.match(r'^' + tag + r'\w*', str)
