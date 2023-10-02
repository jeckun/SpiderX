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

class Book(Story):
    __id=''
    __host=''
    __book_name=''
    __book_author=''
    __storys=[]
    def __init__(self, book_xpath: dict):
        self.__host=book_xpath['host']
        self.__book_name_path=book_xpath['book_path']
        self.__author_path=book_xpath['author_path']
        self.__storys.append(Story(book_xpath))
        self.__save_path=book_xpath['save_path']
        self.__catalog_path=book_xpath['catalog_path']
    
    @property
    def book_path(self):
        return os.path.join(BASE_DIR,self.__save_path)
    
    @property
    def book_name(self):
        return self.__book_name

    # 获取基本信息
    def get_base_inf(self, spider: Spider):
        self.__book_name = spider.get_a_text(self.__book_name_path)