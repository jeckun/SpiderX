import os
from datetime import date
from pathlib import Path
from src.lib.spider import Spider

BASE_DIR = Path(__file__).resolve().parent.parent

class Story:
    __story_url=''
    __story_name=''
    __story_author=''
    __publish_date=''
    __category=''
    __labels=None
    __content=''

    def __init__(self, name, url, author=None, publish=None, category=None, label=None):
        self.__story_url=url
        self.__story_name=name
        self.__story_author=author
        self.__publish_date=publish
        self.__category=category
        self.__labels=label

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
    __info={}
    __storys=[]
    def __init__(self, book_xpath: dict, spider: Spider):
        self.__host=book_xpath['host']
        self.__site_name=book_xpath['site_name']
        self.__save_path=book_xpath['local_save_path']
        self.__info=book_xpath
        self.__sp = spider
    
    @property
    def book_save_path(self):
        return os.path.join(BASE_DIR,self.__save_path)
    
    @property
    def book_name(self):
        return self.__book_name

    # 开始下载文章
    def download(self, x, y):
        # 获取下载文章列表
        for p in range(x,y):
            self.get_story_card(p)
    
        # 校验是否已经下载

        # 获取剩余需要下载文章的信息

        # 下载并存储文章正文

        # 更新数据库

        # 完成下载


    # 获得文章列表
    def get_story_card(self, page_n):
        self.__sp.load_page(self.__host + self.__info['page_url'] % page_n)
        story_cards=self.__sp.get_all_element_path(self.story_card_path)
        # 解析故事卡片信息
        for card in story_cards:
            st=Story(
                name=card,
                url=None,
                author=None,
                publish=None,
                category=None,
                label=None
            )
            pass 

    # 获得文章列表
    def get_story_list(self):
        pass
