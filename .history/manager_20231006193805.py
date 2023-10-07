# -*- coding: utf-8 -*-
import os
import time
from src.site import Site
from src.lib.base import config
import threading

CONFIG =config('config.ini')

# 获取下载列表
def collect_list(start, end):
    id = threading.current_thread().ident
    print("%d# starting." % id)
    site = Site(start)
    for i in range(start, end):
        site.get_list()
        site.next()
        print("%d# collect page %d." % (id, i))
        time.sleep(10)
    print("%d# is end." % id)



if __name__ == '__main__':

    print(f"Start download stories from site.")

    # 计划下载页数
    pages = [1, 10]
    # collect_list(pages[0], pages[1])
    # print(len(site.lists))

    # 多线程同时处理
    max_lines = int(CONFIG['max_lines']) 
    max_lines = max_lines if int(max_lines) < pages[1] else pages[1]

    thd = []
    step=round((pages[1]-pages[0]+1)/max_lines)
    for i in range(pages[0], pages[1], step):
        thd.append(threading.Thread(target=collect_list, args=(i,i+step)))
        thd[i].start()
        time.sleep(1)
    
    print(f"Download completed.")
