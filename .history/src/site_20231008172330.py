import os
import time
import copy
import random
import threading
from DrissionPage import SessionPage

from src.lib.base import config, get_star_end, split_list, \
    multi_thread, \
    wait, wait_all, index, get_group, mkdirs
from src.model import SqliteDB
from src.books import Story

BASE_DIR = os.path.abspath(os.path.curdir)

CONFIG =config('config.ini')

class Site():
    title=''
    host=''
    lists=[]
    storys=[]
    series=[]
    def __init__(self):
        self.title=CONFIG['site_title']
        self.host=CONFIG['host']
        self.page=SessionPage()

    def __str__(self):
        return self.title
    
    def get(self, url):
        self.page.get(url)

    def next(self):
        return self.page.get(self.page.ele(CONFIG['next_page']).link)
    
    def get_list(self, tag: str):
        eles=self.page.eles(tag)
        if eles:
            return [Story(a.ele('tag:a').text, a.ele('tag:a').link) for a in eles]
        else:
            return []

    # def tag_a_list(self, eles):
    #     for ls in eles:
    #         ele=ls.ele('tag:a')
    #         if ele:
    #             yield (ele.text, ele.link)

    # 获取下载列表
    def collect_list(self, start, end):
        id = threading.current_thread().ident
        print("%d# is running." % id)
        self.get(CONFIG['host']+CONFIG['start_page'] % start)
        for i in range(start, end+1):
            self.storys += self.get_list(CONFIG['article_list'])
            self.next()
            print("%d# collect list page %d." % (id, i))
            time.sleep(10)
        print("%d# is stoped." % id)
    

    # 检查下载任务
    # def check_list(self):
    #     id = threading.current_thread().ident
    #     for item in self.lists:
    #         self.storys.append(Story(name=item[0],url=item[1]))
    
    def get_storys(self, start, end):
        for item in self.storys[start: end]:
            self.get_article_info(item)

    def get_series(self, start, end):
        for story in self.storys:
            self.get_article_series(story)
        for item in self.series[start: end]:
            self.get_article_info(item)

    # 获取详情页
    def get_article_info(self, story):
        id = threading.current_thread().ident
        print(f"{id}#", 'article:', story.name)
        try:
            self.get(story.url)
            # 解析文章信息
            story.author= self.page.ele(CONFIG['article_author']).ele('tag:a').text
            story.publish= self.page.ele(CONFIG['publish']).text
            story.category= self.page.ele(CONFIG['category_tags']).text
            story.labels= self.get_lebals(self.page.ele(CONFIG['label_tags']))
            story.content= self.get_article_content(CONFIG['article_content'])
            story.series= self.get_series_list(story, CONFIG['article_series'])
            story.savepath= self.get_filename(story)
        except Exception as e:
            print('get article info error:', story.name)

    # 判断是否为系列故事
    def get_series_list(self, story, tag: str):
        series = self.get_list(tag)
        if series:
            seri = series[0].name
            gpname = get_group(story.name, seri)
            return {gpname: dict([(a.name, a.url) for a in series])} 
        else:
            gpname = get_group(story.name, story.name)
            return {gpname: {}}


    def get_filename(self, story):
        filename=''
        if story.series and list(story.series)[0]:
            filename=os.path.join(BASE_DIR,CONFIG['save_path'],list(story.series)[0],story.name+'.txt')
        else:
            filename=os.path.join(BASE_DIR,CONFIG['save_path'],story.name+'.txt')
        return filename

    # 获取详情页
    def get_article_content(self, xpath):
        content=''
        for p in self.page.s_eles(f'xpath:{ xpath }'):
            content += p.text + '\r\n\r\n'
        return content

    # 整理标签
    def get_lebals(self, lab):
        if lab:
            return [t.text for t in lab.eles('tag:a')]
        else:
            return []

    # 检查关联文章
    def get_article_series(self, story):
        story_list=[n.name for n in self.storys]
        serie_list=[n.name for n in self.series]
        db=SqliteDB()
        rst=db.query_by_sql("select name from story_download_list;")
        db_list = [r[0] for r in rst]
        seri = list(story.series)[0]
        if story.series[seri]:
            for name, url in story.series[seri].items():
                if name not in serie_list and name not in story_list and name not in db_list:
                    # 关联文章不存在，需要下载
                    self.series.append(Story(name=name,url=url))

    # 保存文章
    def save(self, filename, content):
        try:
            mkdirs(os.path.dirname(filename))
            with open(filename, 'w', 2048, encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(e)
    
    # 保存文章信息到数据库
    def save_to_db(self):
        db=SqliteDB(CONFIG['db_name'])
        # 检查数据表
        if not db.check_table_exists("story_download_list"):
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
            db.create_table(sql)

        # 插入数据
        print('Start save to db.')
        for story in self.storys:
            id = ''.join([str(i) for i in random.sample(range(100, 900), 6)])
            labs = ','.join(story.labels) if story.labels else ''
            seri = list(story.series)[0] if story.series else ''

            # 插入前检查是否已有记录，有的跳过
            if db.query_by_filter('story_download_list',f'name="{story.name}"'):
                print(f'recode exists: {story.name}')
                continue
            
            # 没有记录的插入
            sql = "insert into story_download_list(id, name, url, author, publish, " \
                + "category, labels, savepath, series) values " \
                + "('%s','%s','%s','%s','%s'," \
                + "'%s','%s','%s','%s');"
            db.execute(sql % (id,story.name,story.url,story.author,story.publish, \
                story.category,labs,story.savepath,seri))
            db.commit()
        print(f'Recode saved all.')

    
    # 多线程同时下载
    def download(self, pages, multi=False):

        max_lines = int(CONFIG['max_lines']) if int(CONFIG['max_lines']) < pages[1] else pages[1]

        if multi:
            # 获取任务列表
            print('Collect article list...')
            multi_thread(self.collect_list, get_star_end, pages[0], pages[1], max_lines)
            # 多线程采集详情页
            print('Collect article detail...')
            multi_thread(self.get_storys, split_list, 0, len(self.storys), max_lines)
            # 多线程下载关联文章
            print('Collect series article...')
            multi_thread(self.get_series, split_list, 0, len(self.storys), max_lines)
            pass
        else:
            # 获取任务列表
            print('Collect article list...')
            self.collect_list(pages[0], pages[1])
            # 采集详情页
            print('Collect article detail...')
            self.get_storys(0, len(self.storys))
            # 采集关联文章
            print('Collect series article...')
            self.get_series(0, len(self.storys))
            pass

        self.storys += self.series
        self.series=[]

        # 保存文章
        for item in self.storys:
            if item.savepath and item.content:
                self.save(item.savepath, item.content)

        # 更新下载记录
        self.save_to_db()