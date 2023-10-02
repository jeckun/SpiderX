import os
from datetime import date
from pathlib import Path
from src.lib.spider import Spider

BASE_DIR = Path(__file__).resolve().parent.parent

class Story:
    __id=''
    __story_name=''
    __story_author=''
    __publish_date=''
    __story_category=''
    __story_label=[]

    def __init__(self, story_xpath: dict):
        self.__story_path = story_xpath['story_path']
        self.__author_path = story_xpath['author_path']
        self.__publish_date_path = story_xpath['publish_date_path']
        self.__category_path = story_xpath['category_path']
        self.__label_path = story_xpath['label_path']

    @property 
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__story_name
    
    @property
    def author(self):
        return self.__story_author

    @property
    def publish_date(self):
        return self.__publish_date
    
    @property
    def category(self):
        return self.__story_category
    
    @property
    def label(self):
        return self.__story_label

    @property
    def story_path(self):
        return os.path.join(BASE_DIR,self.__save_path,self.__story_path)

class Book():
    __id=''
    __host=''
    __site_name=''
    __base_info={}
    __storys=[]
    def __init__(self, book_xpath: dict, spider: Spider):
        self.__host=book_xpath['host']
        self.__site_name=book_xpath['site_name']
        self.__save_path=book_xpath['local_save_path']
        self.__base_info=book_xpath
        self.__sp = spider
    
    @property
    def book_save_path(self):
        return os.path.join(BASE_DIR,self.__save_path)
    
    @property
    def book_name(self):
        return self.__book_name

    # 开始下载文章
    def download(self, x, y):
        for p in range(x,y):      # 按计划下载指定页数的文章
            # 获取下载文章列表

            # 校验是否已经下载

            # 获取剩余需要下载文章的信息

            # 下载并存储文章正文

            # 更新数据库

            # 完成下载
            pass
    
    # 获得文章列表
    def get_catalog_inf(self):
        return self.__sp.get_all_element_path(self.__catalog_path)

    # 获得文章列表
    def get_story_list(self):
        pass

    # 获得目录信息
    def get_nav_inf(self):
        return self.__sp.get_all_element_path(self.__nav_links_path)
    
    # 获得按元素标签查找
    def get_list(self, tag):
        return self.__sp.get_all_element_tag(tag)