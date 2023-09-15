# -*- coding: utf-8 -*-
import os

print('Welcome !')


def read_file(filename):
    content = ""
    with open(filename, 'r', 'utf-8') as f:
         content = f.readlines
    return content


if __name__ == '__main__':
    filename = '轮奸-和好友香蕉一起被轮姦.txt.txt'
    rst = read_file(filename=filename)
    print(rst)

