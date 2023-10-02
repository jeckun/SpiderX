# -*- coding: utf-8 -*-
import os
from src.lib.books import Book


if __name__ == '__main__':
    xpath={
        'host':'https://houhuayuan.vip/',
        'book_path':'',
        'story_path':'',
        'author_path':'',
        'publish_date_path':'',
        'category_path':'',
        'label_path':'',
        'save_path':'',
    }

    bk = Book(xpath)
