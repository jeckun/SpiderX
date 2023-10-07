from DrissionPage import SessionPage

class Site():
    title=''
    host=''
    lists=[]
    def __init__(self, start):
        url = CONFIG['host']+CONFIG['start_page'] % start
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
        if not eles:
            return
        def a_list(eles):
            for ls in eles:
                ele=ls.ele('tag:a')
                if ele:
                    yield (ele.text, ele.link)
        self.lists += a_list(eles)
