import os
import copy
import random

from threading import Thread
from datetime import date
from src.spider import Spider
from src.model import SqliteDB
from src.lib.base import mkdirs, get_group

BASE_DIR = os.path.abspath(os.path.curdir)

# 搜集文章
class Story:
    url=''
    name=''
    author=''
    publish=''
    category=''
    labels=None
    content=''
    savepath=''   # 存放路径
    series=''      # 是否为系列文章

    def __init__(self, name, url, author=None, publish=None, category=None, label=None, story_content=None):
        self.url=url
        self.name=name
        self.author=author
        self.publish=publish
        self.category=category
        self.labels=label
        self.content=story_content

    def __str__(self):
        return '|'.join([self.name, self.author, self.publish, self.category, ':'.join(self.labels), self.url])


class Site():
    config={}
    storys=[]
    series={}
    def __init__(self, config: dict):
        self.config=config
        self.spider=Spider()
        self.db=SqliteDB(config['db_name'])

    # 开始下载文章
    def download(self, x, y):

        # 获取下载文章列表
        for p in range(x,y+1):
            print("download page:", p)
            self.get_story_card(p)

        # 检测是否系列小说，如果是的，则加入候选下载列表
        for ck in copy.deepcopy(self.storys):
            if ck.series and list(ck.series)[0]:
                series_name=list(ck.series)[0]
                series = ck.series[series_name]
                for key in series.keys():
                    sto=copy.deepcopy(ck)
                    sto.name=key
                    sto.url=series[key]
                    sto.content=''
                    sto.series={series_name:{}}
                    self.storys.append(sto)

        # 校验是否已经下载
        for i, ck in enumerate(self.storys):
            # 检测是否系列小说，如果是的放入系列目录中
            if ck.series and list(ck.series)[0]:
                filename=os.path.join(BASE_DIR,self.config['book_path'],list(ck.series)[0],ck.name+'.txt')
            else:
                filename=os.path.join(BASE_DIR,self.config['book_path'],ck.name+'.txt')

            if os.path.exists(filename):
                # 如果存在，就跳过
                print("%d|%d: " % (i+1, len(self.storys)),'file exsist.', ck.name)
            else:
                # 保存文件
                print("%d|%d: " % (i+1, len(self.storys)),'file save to:', ck.name)
                mkdirs(os.path.dirname(filename))
                if ck.content == '':
                    ck.content=self.get_article_content(ck.url)
                self.save(filename, ck.content)

            # 将文件存放路径改为相对路径
            ck.savepath=filename.replace(BASE_DIR,'.')

        # 更新数据库
        self.save_to_db()


    # 保存文章信息到数据库
    def save_to_db(self):
        # 检查数据表
        if not self.db.check_table_exists("story_download_list"):
            sql = """
            create table story_download_list (
                id       char(100),
                name     char(100), 
                url      char(100),
                author   char(100), 
                publish  char(100), 
                category char(100), 
                labels   char(300),
                savepath char(500), 
                series   char(100)
                );"""
            self.db.create_table(sql)

        # 插入数据
        for sto in self.storys:
            id = ''.join([str(i) for i in random.sample(range(100, 900), 6)])
            labs = ''.join(sto.labels) if sto.labels else ''
            seri = list(sto.series)[0] if sto.series else ''


            # 插入前检查是否已有记录，有的跳过
            rcd = self.db.query_recorder('story_download_list',f'name="{sto.name}"');
            if rcd and rcd[0][0]==1:
                print(f'记录已经存在: {sto.name}')
                next
            
            # 没有记录的插入
            sql = "insert into story_download_list(id, name, url, author, publish, " \
                + "category, labels, savepath, series) values " \
                + "('%s','%s','%s','%s','%s'," \
                + "'%s','%s','%s','%s');"
            self.db.execute(sql % (id,sto.name,sto.url,sto.author,sto.publish,sto.category,labs,sto.savepath,seri))
            self.db.commit()


    # 获得文章列表
    def get_story_card(self, page_n):
        url = self.config['host']+self.config['next_page'] % page_n
        self.spider.get(url)
        story_cards=self.spider.find_elements_by_xpath(self.config['card_path'])
        # 提取故事卡片信息
        for card in story_cards:
            url=card.ele(self.config['story_title']).ele('tag:a').link
            st=Story(
                name=card.ele(self.config['story_title']).ele('tag:a').text,
                url=url,
                author=card.ele(self.config['author']).ele('tag:a').text,
                publish=card.ele(self.config['publish']).text,
                category=card.ele(self.config['category_tags']).text,
                label=self.get_lebals(card.eles(self.config['label_tags']))
            )
            st.content = self.get_article_content(url)
            st.series = self.check_series(st, self.spider.page.eles(self.config['series']))
            self.storys.append(st)
            print('get article info:', st.name)

    # 获取详情页
    def get_article_content(self, url):
        self.spider.get(url)
        story_content = self.spider.find_elements_by_xpath(self.config['story_content'])
        return self.content_convert(story_content)

    def content_convert(self, story):
        content=''
        for p in story:
            content += p.text + '\r\n\r\n'
        return content
    
    # 检查是否为系列故事
    def check_series(self, story, series):
        if series:
            gpname = get_group(story.name, series[0].ele('tag:a').text)
            return {gpname: dict([(a.ele('tag:a').text, a.ele('tag:a').link) for a in series])} 
        else:
            return {}
    
    # 整理标签
    def get_lebals(self, tags=None):
        tgs=[]
        for i in range(len(tags)):
            tgs.append(tags[i].ele('tag:a').text)
        return tgs

    # 保存文章
    def save(self, filename,content):
        with open(filename, 'w', 2048, encoding='utf-8') as f:
            f.write(content)