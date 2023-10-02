# -*- coding: utf-8 -*-
import os
from src.lib.books import Book
from src.lib.spider import Spider


if __name__ == '__main__':

    xpath={
        'host':'https://houhuayuan.vip/',           # 网站首页
        'site_name': '蔷薇后花园',                   # 站点名称
        'local_save_path':'books',                  # 本地保存路径
        'page_url': 'page/%d',                      # 翻页链接

        'story_card_path':'//main/article',         # 故事卡片区域
        'story_name':'@class=entry-title',          # 故事名称
        'author_path':'@class=author vcard',        # 故事作者
        'publish_date':'@class=entry-date published',    # 发表日期
        'category_tags':'@rel=category tag',        # 故事类别
        'label_tags':'@class=tags-links',           # 故事标签

        'story_content':'@class=entry-content',         # 故事正文
        'thread_no': 5,          # 下载线程数
    }

    print(f"Start download stories from site: {xpath['host']} - {xpath['site_name']}")

    sp = Spider(xpath['host'])
    bk = Book(xpath, sp)
    bk.download(1, 2)

    print(f"Download completed.")
