# 搜集文章
class Story:
    url=''
    name=''
    author=''
    publish=''
    category=''
    labels=[]
    content=''
    series=None      # 是否为系列文章
    savepath=''   # 存放路径
    download=False

    def __init__(self, name, url, author=None, publish=None, category=None, labels=None, story_content=None, savepath=None):
        self.url=url
        self.name=name
        self.author=author
        self.publish=publish
        self.category=category
        self.labels=labels
        self.content=story_content
        self.savepath=savepath

    def __str__(self):
        return self.name
