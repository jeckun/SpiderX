# -*- coding: utf-8 -*-
import os
from src.books import Site
from src.spider import Spider
from src.lib.base import config


if __name__ == '__main__':

    cfg=config('config.ini')

    print(f"Start download stories from site: {cfg['host']} - {cfg['site_title']}")

    sp = Spider()
    sit = Site(cfg, sp)
    sit.download(4, 4)

    print(f"Download completed.")
