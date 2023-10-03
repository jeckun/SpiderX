# -*- coding: utf-8 -*-
import os
import configparser
from src.lib.books import Book
from src.lib.spider import Spider


if __name__ == '__main__':

    cf = configparser.ConfigParser()
    cf.read('.config.ini',encoding="utf-8")
    print(cf.sections())
    print(cf.options('site'))
    print(cf.options('path'))
    print(cf.options('article'))
    print(cf.options('thread'))

    print(f"Start download stories from site: {xpath['host']} - {xpath['site_name']}")

    sp = Spider(xpath['host'])
    bk = Book(xpath, sp)
    bk.download(1, 2)

    print(f"Download completed.")
