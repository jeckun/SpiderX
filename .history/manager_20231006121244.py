# -*- coding: utf-8 -*-
import os
import time
import random
from src.site import Site
from threading import Thread, Semaphore

CONFIG =config('config.ini')

# 获取下载列表
def collect_list(start, end):
    site = Site(start)
    for i in range(start, end):
        site.join_list()
        site.next()
        time.sleep(10)



if __name__ == '__main__':


    print(f"Start download stories from site.")

    # 计划下载页数
    pages = [1, 5]
    collect_list(pages[0], pages[1])
    print(len(site.lists))

    # 多线程同时处理
    # semaphore = Semaphore(0)     # 使用信号量跟踪子线程执行情况

    # max_lines = int(cfg['max_lines']) if int(cfg['max_lines']) < pages[1] else pages[1]

    # for i in range(pages[0], pages[1], max_lines):
    #     sit = [Site(cfg,i) for i in range(max_lines)]
    #     thd = []
    #     for x in range(max_lines):
    #         thd.append(Thread(target=sit[x].download, args=(i+x,i+x)))
    #         thd[x].start()
    #         time.sleep(1)
    #     for x in thd:
    #         x.join(10)
    #     semaphore.acquire()  # 等待子线程完成再启动下次循环
    
    print(f"Download completed.")
