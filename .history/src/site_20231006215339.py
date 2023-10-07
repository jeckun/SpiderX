from DrissionPage import SessionPage
from src.lib.base import config, get_star_end, wait
import threading
import time

CONFIG =config('config.ini')

class Site():
    title=''
    host=''
    lists=[]
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
        print("%d# starting." % id)
        self.get(CONFIG['host']+CONFIG['start_page'] % start)
        for i in range(start, end+1):
            self.get_list()
            self.next()
            print("%d# collect page %d." % (id, i))
            time.sleep(10)
        print("%d# is end." % id)
    

    # 检查下载任务
    def check_list(self):
        # 检查文章是否已经下载
        pass

    # 获取详情页
    def get_article(self, url):
        pass

    # 检查关联文章
    def get_article_series(self, url):
        pass

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
        # self.check_list()

        # 多线程下载详情页
        # self.get_article()

        # 检查是否有关联文章
        # self.get_article_series()

        # 多线程下载关联文章

        # 保存文章

        # 更新下载记录