from DrissionPage import SessionPage

class Site():
    title=''
    host=''
    lists=[]
    def __init__(self, config:{}):
        self.title=config['site_title']
        self.host=config['host']
        self.page=SessionPage()
        self.page.get(self.host)

    def __str__(self):
        return self.title
    
    def next(self):
        return self.page.get(self.page.ele(config['next_page']).link)
    
    def join_list(self):
        eles=self.page.eles(config['article_list'])
        self.lists.append([(link.text, link.link) for link in eles])
