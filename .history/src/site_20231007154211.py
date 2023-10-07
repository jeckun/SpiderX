import os
import time
import copy
import random
import threading
from DrissionPage import SessionPage

from src.lib.base import config, get_star_end, split_list, wait, index, get_group, mkdirs
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
    
    def get_list(self):
        eles=self.page.eles(CONFIG['article_list'])
        if not eles:
            return
        self.lists += self.tag_a_list(eles)

    def tag_a_list(self, eles):
        for ls in eles:
            ele=ls.ele('tag:a')
            if ele:
                yield (ele.text, ele.link)

    # 获取下载列表
    def collect_list(self, start, end):
        id = threading.current_thread().ident
        print("%d# is running." % id)
        self.get(CONFIG['host']+CONFIG['start_page'] % start)
        for i in range(start, end+1):
            self.get_list()
            self.next()
            print("%d# collect page %d." % (id, i))
            time.sleep(10)
        print("%d# is stoped." % id)
    

    # 检查下载任务
    def check_list(self):
        id = threading.current_thread().ident
        print("%d# start check list. | %d need check." % (id, len(self.lists)))
        # 检查数据库中是否有记录
        database=SqliteDB(CONFIG['db_name'])
        sql = "select name, savepath from story_download_list;"
        db_collected_list = database.query_by_sql(sql)
        db_name_list = [n[0] for n in db_collected_list]
        for item in self.lists:
            n = index(item[0],db_name_list)
            if n == -1:
                self.storys.append(Story(name=item[0],url=item[1]))
            else:
                self.storys.append(Story(name=item[0],url=item[1],savepath=db_collected_list[n][1]))
        pass
        # 检查文件是否存在，如果存在就不需要重复下载
        chkstory = copy.deepcopy(self.storys)
        self.storys=[]
        for item in chkstory:
            filename = item.savepath
            if not filename or not os.path.exists(filename):
                self.storys.append(item)
        print("%d# check list end.  |  %d need download." % (id, len(self.storys)))
    
    def get_articles(self, start, end):
        for item in self.storys[start: end]:
            self.get_article_info(item)

    # 获取详情页
    def get_article_info(self, story):
        id = threading.current_thread().ident
        self.get(story.url)
        # 解析文章信息
        story.author= self.page.ele(CONFIG['article_author']).ele('tag:a').text
        story.publish= self.page.ele(CONFIG['publish']).text
        story.category= self.page.ele(CONFIG['category_tags']).text
        story.labels= self.get_lebals(self.page.ele(CONFIG['label_tags']))
        story.content= self.get_article_content(CONFIG['article_content'])
        story.series= self.check_series(story, self.page.eles(CONFIG['article_series']))
        story.savepath= self.get_filename(story)
        print(f"{id}#", 'Collected article info. ', story.name)

    # 检查是否为系列故事
    def check_series(self, story, series):
        if series:
            seri = series[0].eles('tag:a') 
            gpname = get_group(story.name, seri[0].text)
            return {gpname: dict([(a.text, a.link) for a in seri])} 
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

    # 检查关联文章
    def get_article_series(self, story):
        seri = list(story.series)[0]
        if story.series[seri]:
            for name, url in story.series[seri].items():
                filename = os.path.join(BASE_DIR,CONFIG['save_path'],seri,name+'.txt')
                if os.path.exists(filename):
                    continue
                else:
                    # 关联文章重复检查
                    seri_list=[n.name for n in self.series]
                    if name not in seri_list:
                        # 关联文章不存在，需要下载
                        self.series.append(Story(name=name,url=url))

    
    # 整理标签
    def get_lebals(self, lab):
        if lab:
            return [t.text for t in lab.eles('tag:a')]
        else:
            return []

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
    def download(self, pages):

        max_lines = int(CONFIG['max_lines']) 
        max_lines = max_lines if max_lines < pages[1] else pages[1]
        thd = []
        s_e = []
        step=round((pages[1]-pages[0]+1)/max_lines)
        s_e += get_star_end(pages[0], pages[1], step)

        # 启动多线程，下载采集清单
        for i in range(len(s_e)):
            thd.append(threading.Thread(target=self.collect_list, args=(s_e[i][0] , s_e[i][1])))
            thd[i].start()
            time.sleep(1)
            # 防止启动过多线程
            wait(max_linex=max_lines)
    
        # 检查任务列表
        self.check_list()
        if len(self.storys)==0:
            return

        # 多线程采集详情页        
        thd = []
        s_e = []
        step=round(len(self.storys)/max_lines)
        s_e += split_list(self.storys, step)
        for i in range(len(s_e)):
            thd.append(threading.Thread(target=self.get_articles, args=(s_e[i][0] , s_e[i][1])))
            thd[i].start()
            time.sleep(1)
            # 防止启动过多线程
            wait(max_linex=max_lines)

        # 检查是否有关联文章
        for item in self.storys:
            if item.series:
                self.get_article_series(item)

        # 多线程下载关联文章
        for item in self.series:
            self.get_article_info(item)
        self.storys += self.series

        # 保存文章
        for item in self.storys:
            self.save(item.savepath, item.content)

        # 更新下载记录
        self.save_to_db()