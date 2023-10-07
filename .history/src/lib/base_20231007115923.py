import os
import chardet
import time
import threading
import configparser

# 检查文件编码
def check_encode(filename):
    file = open(filename, 'rb')
    data = file.read()
    encode = chardet.detect(data)
    file.close()
    en = 'gbk' if encode['encoding']=='GB2312' else encode['encoding']
    return 'utf-8' if en==None else en

# 分段读取文件
# 调用方法：
# for block in openfile(filename):
#        print(block)
def read_file_block(filename, block=1024):
    with open(filename, 'r', buffering=4096, encoding=check_encode(filename)) as f:
        size = f.seek(0, os.SEEK_END)
        f.seek(0)
        while f.tell()<size:
            yield f.read(2048)

# 读取配置文件
def config(filename):
    rst = {}
    cf = configparser.ConfigParser()
    cf.read(filename,encoding="utf-8")
    for item in cf.sections():
        rst.update(dict(cf.items(item)))
    return rst

# 创建目录
def mkdirs(path):
    it = ''
    if os.path.isdir(path):
        return
    for i, item in enumerate(path.split('\\')):
        it += item + '\\'
        if i>=1:
            ph = os.path.join(it)
            if os.path.isdir(ph):
                pass
            else:
                os.mkdir(ph)
    return

def get_group(x: str, y: str):
    lw = ['.',' ','！','：','，','…','!','@','/','\\','#','$','%','^','&','*','`','\'','\"',',','|']
    if len(x) > len(y):
        a, b = list(x), list(y)
    else:
        a, b = list(y), list(x)
    for i, c in enumerate(b):
        if b[i] == a[i] and b[i] not in lw:
            pass
        else:
            return ''.join(b[:i])
    return ''.join(b)

def wait(max_linex):
    while True:        # 检测子线程是否执行完毕，执行完成再启动新的子线程
        if len(threading.enumerate()) <= max_linex :
            break
        time.sleep(10)

def split_list(obj: list, step: int):
    x = 0
    for i in range(0,len(obj),step):
        x += step
        x = x if len(obj) > x else len(obj)
        if i < x:
            yield obj[i:x]


def get_star_end(s, e, t):
    for i in range(s,e+1,t):
        if i+t > e:
            yield i, e
        else:
            yield i, t + i -1

def index(item, list: list):
    try:
        index = list.index(item)
        return index
    except Exception as e:
        return -1