# -*- coding: utf-8 -*-
import os
from io import TextIOWrapper
from src.lib.base import read_file_block


if __name__ == '__main__':
    filename = './轮奸-和好友香蕉一起被轮姦.txt'
    for block in read_file_block(filename):
        print(block)
