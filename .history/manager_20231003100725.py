# -*- coding: utf-8 -*-
import os
from src.lib.books import Book
from src.lib.spider import Spider
from src.lib.base import config


if __name__ == '__main__':

    cfg=config(('SITE', 'PATH', 'ARTICLE', 'THREAD'))

    print(f"Start download stories from site: {cfg['host']} - {cfg['site_title']}")

    sp = Spider(xpath['host'])
    bk = Book(xpath, sp)
    bk.download(1, 2)

    print(f"Download completed.")
