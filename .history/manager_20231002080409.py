# -*- coding: utf-8 -*-
import os
from io import TextIOWrapper
from src.lib.base import check_encode

def openfile(filename):
    content=''
    with open(filename, 'r', buffering=4096, encoding=check_encode(filename)) as f:
        size = f.seek(0, os.SEEK_END)
        f.seek(0)
        while f.tell()<size:
            content += f.read(2048)
    return content


if __name__ == '__main__':
    filename = './轮奸-和好友香蕉一起被轮姦3.txt'
    print(openfile(filename))
