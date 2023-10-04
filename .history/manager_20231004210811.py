# -*- coding: utf-8 -*-
import os
from threading import Thread
from src.books import Site
from src.spider import Spider
from src.lib.base import config


if __name__ == '__main__':

    cfg=config('config.ini')

    print(f"Start download stories from site: {cfg['host']} - {cfg['site_title']}")

    sit = Site(cfg)
    sit.download(3, 3)

    print(f"Download completed.")
