# -*- coding: utf-8 -*-
import os
from src.books import Book
from src.spider import Spider
from src.lib.base import config



if __name__ == '__main__':

    cfg=config('config.ini')

    print(f"Start download stories from site: {cfg['host']} - {cfg['site_title']}")

    bks = Book(cfg)
    bks.download(2, 2)

    print(f"Download completed.")
