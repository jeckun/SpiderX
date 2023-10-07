

class Site():
    title=''
    host=''
    lists=[]
    def __init__(self, config:{}):
        self.title=config('site_title')
        self.host=config('host')
    def __str__(self):
        return self.title
    