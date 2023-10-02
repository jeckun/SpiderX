# -*- coding: utf-8 -*-
import os
from src.lib.base import check_encode

print('Welcome !')

def openfile(filename):
    # with open(filename,'r',encoding='utf-8',header=None) as f:
    #     return f.readlines()

    with open(filename, 'r', encoding=check_encode(filename)) as f:
        lines = f.readlines()
    
    for line in lines:
        print(line)


if __name__ == '__main__':
    filename = './轮奸-和好友香蕉一起被轮姦.txt'
    print(openfile(filename))
