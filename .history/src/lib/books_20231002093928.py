from datetime import date
import os

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

class Book(Story):
    __id=''
    __book_name=''
    __book_author=''
    __storys=[]
    def __init__(self, book_xpath: dict):
        self.__book_path=book_xpath['book_path']
        self.__author_path=book_xpath['author_path']
        self.__storys.append(Story(book_xpath))
        self.__save_path=book_xpath['save_path']
    
    @property
    def book_path(self):
        return os.path.join()