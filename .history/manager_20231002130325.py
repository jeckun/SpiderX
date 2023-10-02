# -*- coding: utf-8 -*-
import os
from src.lib.books import Book
from src.lib.spider import Spider


if __name__ == '__main__':
    xpath={
        'host':'https://houhuayuan.vip/',
        'book_path':'/html/body/div[2]/div[1]/header/div/h1/a',
        'story_path':'',
        'author_path':'',
        'publish_date_path':'',
        'category_path':'//main/article/footer/span[3]/a',  # 类别
        'catalog_path':'//main/article/header/h2/a',   # 目录
        'nav_links_path':'/html/body/div[2]/div[2]/div/main/nav/div', # 导航栏
        'label_path':'//main/article/footer/span[4]',
        'save_path':'',
    }



    sp = Spider(xpath['host'])
    bk = Book(xpath, sp)
    bk.get_base_inf()
    a = bk.get_catalog_inf()
    b = bk.get_nav_inf()
    l = bk.get_list('@class=entry-title')

    print(bk.book_name)
