# -*- coding: utf-8 -*-
import os
from io import TextIOWrapper
from src.lib.base import check_encode

def openfile(filename):
    # with open(filename,'r',encoding='utf-8',header=None) as f:
    #     return f.readlines()

    # f=open(filename,'r',2048,'utf-8')
    # while True:
    #     line=f.readline()
    #     if len(line)==0: # Zero length indicates EOF
    #         break
    #     print(line)
    # f.close()

    with open(filename, 'r', buffering=4096, encoding=check_encode(filename)) as f:
        size = f.seek(0, os.SEEK_END)
        f.seek(0)
        while f.tell()<size:
            line = f.read(1000)
            print("%d/%d" % (size, f.tell()), line,'\n\n')


if __name__ == '__main__':
    filename = './轮奸-和好友香蕉一起被轮姦3.txt'
    print(openfile(filename))
