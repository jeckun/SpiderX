# -*- coding: utf-8 -*-
import os
import time
from src.books import Site
from src.spider import Spider
from src.lib.base import config
from threading import Thread


if __name__ == '__main__':

    cfg=config('config.ini')

    print(f"Start download stories from site: {cfg['host']} - {cfg['site_title']}")

    sit = Site(cfg)
    # sit.download(4, 4)

    # 多线程同时处理
    Thread(target=sit.download, args=(1,1, 1)).start()
    time.sleep(random.randint(5, 10))
    Thread(target=sit.download, args=(6,6, 2)).start()

    print(f"Download completed.")
