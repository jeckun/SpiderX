from DrissionPage import SessionPage
from src.lib.base import config, get_star_end
import threading

CONFIG =config('config.ini')

class Site():
    title=''
    host=''
    lists=[]
    def __init__(self):
        self.title=CONFIG['site_title']
        self.host=CONFIG['host']
        self.page=SessionPage()
        self.page.get(self.host)

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
        url = CONFIG['host']+CONFIG['start_page'] % start
        self.page = self.get(url)
        for i in range(start, end+1):
            self.get_list()
            self.next()
            print("%d# collect page %d." % (id, i))
            time.sleep(10)
        print("%d# is end." % id)
    
    # 多线程同时处理
    def download(self, pages):
        max_lines = int(CONFIG['max_lines']) 
        max_lines = max_lines if int(max_lines) < pages[1] else pages[1]

        thd = []
        s_e = []
        step=round((pages[1]-pages[0]+1)/max_lines)
        s_e += get_star_end(pages[0], pages[1], step)
        for i in range(len(s_e)):
            thd.append(threading.Thread(target=self.collect_list, args=(s_e[i][0] , s_e[i][1])))
            thd[i].start()
            time.sleep(1)
            wait(max_linex=max_lines) # 检测子线程是否执行完毕，执行完成再启动新的子线程