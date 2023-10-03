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

    def __str__(self):
        return '|'.join([self.__story_name, self.__story_author, self.__publish_date, self.__category, ':'.join(self.__labels), self.__story_url])


class Book():
    config={}
    storys=[]
    page=None
    def __init__(self, config: dict):
        self.config=config
        self.page=Spider()

    # 开始下载文章
    def download(self, x, y):
        # 获取下载文章列表
        for p in range(x,y+1):
            print("download page:", p)
            self.get_story_card(p)
    
        # 校验是否已经下载

        # 获取剩余需要下载文章的信息

        # 下载并存储文章正文

        # 更新数据库

        # 完成下载


    # 获得文章列表
    def get_story_card(self, page_n):
        url = self.config['host']+self.config['next_page'] % page_n
        self.page.get(url)
        story_cards=self.page.find_elements(self.config['card_path'])
        # 提取故事卡片信息
        for card in story_cards:
            st=Story(
                name=card.ele(self.config['story_title']).ele('tag:a').text,
                url=card.ele(self.config['story_title']).ele('tag:a').link,
                author=card.ele(self.config['author']).ele('tag:a').text,
                publish=card.ele(self.config['publish_date']).text,
                category=card.ele(self.config['category_tags']).text,
                label=self.get_lebals(card.eles(self.config['label_tags'])),
            )
            self.storys.append(st)

    # 整理标签
    def get_lebals(self, tags=None):
        tgs=[]
        for i in range(len(tags)):
            tgs.append(tags[i].ele('tag:a').text)
        return tgs
