from DrissionPage import SessionPage

CONFIG ={}

class Site():
    title=''
    host=''
    lists=[]
    def __init__(self, conf:{}):
        global CONFIG 
        CONFIG = conf
        self.title=CONFIG['site_title']
        self.host=CONFIG['host']
        self.page=SessionPage()
        self.page.get(self.host)

    def __str__(self):
        return self.title
    
    def next(self):
        return self.page.get(self.page.ele(CONFIG['next_page']).link)
    
    def join_list(self):
        eles=self.page.eles(CONFIG['article_list'])
        self.lists.append([(link.text, link.link) for link in eles])
