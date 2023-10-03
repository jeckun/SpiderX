import os
import copy
from datetime import date
from src.spider import Spider
from src.lib.base import mkdirs, get_group
from pathlib import Path

# BASE_DIR = os.path.abspath(os.path.pardir)
BASE_DIR = os.path.abspath(os.path.curdir)

class Story:
    url=''
    name=''
    author=''
    publish_date=''
    category=''
    labels=None
    content=''
    group=''      # 是否为系列文章

    def __init__(self, name, url, author=None, publish=None, category=None, label=None, story_content=None):
        self.url=url
        self.name=name
        self.author=author
        self.publish_date=publish
        self.category=category
        self.labels=label
        self.content=story_content

    def __str__(self):
        return '|'.join([self.name, self.author, self.publish_date, self.category, ':'.join(self.labels), self.url])


class Book():
    config={}
    storys=[]
    series={}
    page=None
    def __init__(self, config: dict):
        self.config=config
        self.spider=Spider()

    # 开始下载文章
    def download(self, x, y):
        # 获取下载文章列表
        for p in range(x,y+1):
            print("download page:", p)
            self.get_story_card(p)
        print(f'Found {len(self.storys)} articles.')

        # 检测是否系列小说，如果是的，则加入候选下载列表
        for ck in self.storys:
            if ck.group and list(ck.group)[0]:
                series_name=list(ck.group)[0]
                series = ck.group[series_name]
                for key in sr.keys():
                    ck_cp=copy.deepcopy(ck)
                    ck_cp.name=key
                    ck_cp.url=sr[key]
                    ck_cp.group={series_name:{}}
                    self.storys.append(ck_cp)


        # 校验是否已经下载
        for ck in self.storys:
            # 检测是否系列小说，如果是的放入系列目录中
            if ck.group and list(ck.group)[0]:
                filename=os.path.join(BASE_DIR,self.config['book_path'],list(ck.group)[0],ck.name+'.txt')
                self.series.update(ck.group[list(ck.group)[0]])
            else:
                filename=os.path.join(BASE_DIR,self.config['book_path'],ck.name+'.txt')

            if os.path.exists(filename):
                # 如果存在，就跳过
                print('file exsist.', filename)
            else:
                # 保存文件
                print('file save to :', filename)
                mkdirs(os.path.dirname(filename))
                self.save(filename, ck.content)
        
        # 下载系列文章
        for key in list(self.series):
            pass

        # 获取剩余需要下载文章的信息

        # 下载并存储文章正文

        # 更新数据库

        # 完成下载


    # 获得文章列表
    def get_story_card(self, page_n):
        url = self.config['host']+self.config['next_page'] % page_n
        self.spider.get(url)
        story_cards=self.spider.find_elements_by_xpath(self.config['card_path'])
        # 提取故事卡片信息
        for card in story_cards:
            url=card.ele(self.config['story_title']).ele('tag:a').link
            st=Story(
                name=card.ele(self.config['story_title']).ele('tag:a').text,
                url=url,
                author=card.ele(self.config['author']).ele('tag:a').text,
                publish=card.ele(self.config['publish_date']).text,
                category=card.ele(self.config['category_tags']).text,
                label=self.get_lebals(card.eles(self.config['label_tags']))
            )
            # 获取详情页
            self.spider.get(url)
            story_content = self.spider.find_elements_by_xpath(self.config['story_content'])
            st.content = self.content_convert(story_content)
            st.group = self.check_group(st, self.spider.page.eles(self.config['series']))
            self.storys.append(st)

    def content_convert(self, story):
        content=''
        for p in story:
            content += p.text + '\r\n\r\n'
        return content
    
    # 检查是否为系列故事
    def check_group(self, story, group):
        if group:
            gpname = get_group(story.name, group[0].ele('tag:a').text)
            return {gpname: dict([(a.ele('tag:a').text, a.ele('tag:a').link) for a in group])} 
        else:
            return {}
    
    # 整理标签
    def get_lebals(self, tags=None):
        tgs=[]
        for i in range(len(tags)):
            tgs.append(tags[i].ele('tag:a').text)
        return tgs

    # 保存文章
    def save(self, filename,content):
        with open(filename, 'w', 2048, encoding='utf-8') as f:
            f.write(content)