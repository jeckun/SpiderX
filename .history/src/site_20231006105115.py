

class Site():
    title=''
    host=''
    def __init__(self, title, host):
        self.title=title
        self.host=host
    def __str__(self):
        return self.title
    