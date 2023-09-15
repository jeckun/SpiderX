# -*- coding: utf-8 -*-
import os

print('Welcome !')

def openfile(filename):
    content = ''
    with open(filename,'r',encoding='utf-8') as f:
        while True:
            text = f.read(1024)
            if len(text) == 0:
                break
            else:
                content += text
    return content


if __name__ == '__main__':
    filename = '轮奸-和好友香蕉一起被轮姦.txt'
    print(openfile(filename))
