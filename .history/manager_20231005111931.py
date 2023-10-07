# -*- coding: utf-8 -*-
import os
import time
import random
from src.books import Site
from src.spider import Spider
from src.lib.base import config
from threading import Thread, Semaphore


if __name__ == '__main__':

    cfg=config('config.ini')

    print(f"Start download stories from site: {cfg['host']} - {cfg['site_title']}")

    # 计划下载页数
    pages = [1, 10]

    # 多线程同时处理
    semaphore = Semaphore(0)     # 使用信号量跟踪子线程执行情况

    sit1 = Site(cfg)
    sit2 = Site(cfg)
    sit3 = Site(cfg)

    for i in range(pages[0], pages[1], 3):
        for x in range(1, cfg['max_lines']):
            if i <= pages[1]:
                Thread(target=sit1.download, args=(i+x,i+x, 1+x)).start()
                time.sleep(random.randint(5, 10))
        semaphore.acquire()  # 等待子线程完成再启动下次循环

    
    print(f"Download completed.")
