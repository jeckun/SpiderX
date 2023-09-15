#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import requests
import time
import random
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = {
    'site_name': '站点名称，下载文件夹名称',
    'channel': '频道名称',
    'headers': '头文件信息',
    'cookies': 'cookies信息',
    'host': '主机名，用于和相对路径组合成为绝对路径',
    'url': '网页加载链接，可以带参数。也可以不带参数。带参数时需要重写run函数',
    'params': '参数变量',
    'selector': '列表的css_selector',
    'min': '开始抓取页面',
    'max': '截止抓取页面，注意：截止时是包含最后一页的。',
    'table_id': '需要采集表格的ID',
    'article_content_css_selector': '文章内容的css_selector',
    'tag_css_selector': '文章内的文件类型css_selector',
}

class Spider(object):
    def __init__(self):
        self._host = CONFIG['host'] 
        self._url = CONFIG['url'] 
        self._headers = CONFIG['headers']
        self._cookies = CONFIG['cookies']
        self.lists = []

    def load(self, url, params):
        try:
            response = requests.get(url, headers=CONFIG['headers'], params=params, 
                cookies=CONFIG['cookies'], verify=True)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.content, "lxml")
                time.sleep(random.randint(0, 5))
                return True
            else:
                return False
        except Exception as err:
            print('打开网页错误:', err)
            return False
    
    # def get_list(self, fun, css_selector):
    #     try:
    #         rst = self.soup.select(css_selector)
    #         if rst:
    #             return fun(rst)
    #     except Exception as err:
    #         print('解析列表错误:', err)
    
    def get_text(self, css_selector):
        try:
            rst = self.soup.select(css_selector)
            if rst:
                return rst[0]
        except Exception as err:
            print('解析文本错误:', err)

    # def get_table(self, fun, table_id):
    #     try:
    #         table = self.soup.find("table", {"id" : table_id})
    #         for row in table.findAll("tr"):
    #             cells = row.findAll("td")
    #             return fun(cells)
    #     except Exception as err:
    #         print('解析表格数据错误：', err)
    
    def save_to_txt(self, formart_fun, formart_obj, filename):
        return self.save_to_file(filename, formart_fun(formart_obj), 'w')

    def save_to_html(self, i, formart_fun, content, filename):
        return self.save_to_file(filename, formart_fun(content, self.lists[i][1], self.lists[i][0]), 'w')

    def save_to_file(self, filename, content, tag):
        try:
            with open(filename, tag) as f:
                f.write(content)
            return True
        except Exception as err:
            print('保存内容失败...', err)
            return False

    def load_from_txt(self, filename, load_txt_fun, formart_obj):
        return self.load_from_file(filename, 'r', load_txt_fun, formart_obj)

    def load_from_html(self, filename, load_txt_fun, formart_obj):
        pass

    def load_from_file(self, filename, tag, load_fun, formart_obj):
        try:
            with open(filename, tag) as f:
                for line in f.readlines():
                    load_fun(line, formart_obj)
            return True
        except Exception as err:
            print('加载文件失败...', err)
            return False


    def run(self, get_list_fun, formart_fun, formart_obj, load_txt_fun, formart_content_fun):
        # 显示摘要
        print('\n站点：\t%s\n' % CONFIG['site_name'])
        print('频道：\t%s\n' % CONFIG['channel'])
        print('网址：\t%s\n' % CONFIG['host'])
        print('下载页面：%d页 ~ %d页\n' % (CONFIG['min'], CONFIG['max']))

        # 获取列表
        print('获取列表:\n')
        for i in range(CONFIG['min'], CONFIG['max']+1):
            # 生成缓存文件名
            mkdir(CONFIG['site_name'])
            mkdir('cache')
            filename=os.path.join(BASE_DIR, 'cache', '%s_%s_%d.txt' % (CONFIG['site_name'],CONFIG['channel'],i))
            # 检查本地是否有缓存，如果有就加载
            if os.path.exists(filename):
                print('从缓存加载第%d页' % i)
                self.load_from_txt(filename, load_txt_fun, formart_obj)
                continue
            # 没有缓存，就从网上下载
            print('从网页加载第%d页' % i)
            ls = get_list_fun(i)

            # 缓存列表
            self.save_to_txt(formart_fun, ls, filename)

            self.lists += ls
        
        # 开始下载文章内容
        print('\n开始下载\n')
        t = len(self.lists)
        fg = False
        for i in range(t):
            # 生成下载文件名
            filename_doc=os.path.join(BASE_DIR, CONFIG['site_name'], self.lists[i][0]+self.lists[i][1].replace('/','')+'.html')
            # 检查是否存在，如果存在跳过，不存在时下载
            if not os.path.exists(filename_doc):
                self.load(self.lists[i][2], {})
                self.save_to_html(i, formart_content_fun, self.get_text(CONFIG['article_content_css_selector']), filename_doc)
                print('%d/%d:\t%s' % (i+1, t, self.lists[i][0]+self.lists[i][1].replace('/','')+'.html'))
        

        print('下载完成')

# ----------- 公共函数 -------------
# 创建目录
def mkdir(dir_name):
    path = os.path.join(BASE_DIR, dir_name)
    if not os.path.isdir(path):
        os.makedirs(path)