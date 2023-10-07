# -*- coding: utf-8 -*-
import os
import time
import random
from src.site import Site
from src.lib.base import config
from threading import Thread, Semaphore

CONFIG =config('config.ini')

# 获取下载列表
def collect_list(start, end):
    print("%d# starting." % Thread.get_ident())
    site = Site(start)
    for i in range(start, end):
        site.get_list()
        site.next()
        time.sleep(10)
    print("%d# is end." % Thread.get_ident())



if __name__ == '__main__':


    print(f"Start download stories from site.")

    # 计划下载页数
    pages = [1, 10]
    collect_list(pages[0], pages[1])
    print(len(site.lists))

    # 多线程同时处理

    max_lines = int(CONFIG['max_lines']) if int(CONFIG['max_lines']) < pages[1] else pages[1]

    for i in range(pages[0], pages[1], max_lines):
        thd = []
        for x in range(max_lines):
            thd.append(Thread(target=collect_list, args=(i+x,i+x+rand((pages[1]-pages[0])/max_lines))))
            thd[x].start()
            thd[x].join(3)
    
    print(f"Download completed.")
