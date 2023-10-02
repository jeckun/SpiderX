# -*- coding: utf-8 -*-
import os
from src.lib.books import Book


if __name__ == '__main__':
    xpath={
        'host':'https://houhuayuan.vip/',
        'book_path':'header/div/h1/a',
        'story_path':'',
        'author_path':'',
        'publish_date_path':'',
        'category_path':'//main/article/footer/span[3]/a',  # 类别
        'catalog_path':'//main/article/header/h2/a',   # 目录
        'label_path':'//main/article/footer/span[4]',
        'save_path':'',
    }

    bk = Book(xpath)
    print(bk)
