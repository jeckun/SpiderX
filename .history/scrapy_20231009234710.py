# scrapy.py

import scrapy
import os
import sqlite3
import random
import time

# 创建一个文件夹来保存爬取的内容
if not os.path.exists("Book"):
    os.mkdir("Book")

# 创建或连接到SQLite数据库
conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

# 检查数据库中是否已经存在articles表，如果不存在则创建
cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                  (title TEXT PRIMARY KEY,
                   link TEXT,
                   author TEXT,
                   date TEXT,
                   tags TEXT,
                   content TEXT)''')
conn.commit()

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://zhaoze.pro']
    
    def parse(self, response):
        # 提取文章链接
        article_links = response.xpath('//h2[@class="post-title"]/a/@href').extract()
        
        # 将链接加入队列前进行重复检查
        for link in article_links:
            if link not in article_links_queue.queue:
                article_links_queue.put(link)

        # 获取下一页的链接并继续抓取
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def start_requests(self):
        # 发送初始请求
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

# 定义函数来下载文章内容
def download_article_content(thread_id):
    while not article_links_queue.empty():
        try:
            article_url = article_links_queue.get()
            response = requests.get(article_url)
            if response.status_code == 200:
                tree = html.fromstring(response.text)
                title = tree.xpath("//h1[@class='post-title']/text()")[0]
                content = tree.xpath("//div[@class='post-content']//text()")
                author = tree.xpath("//span[@class='post-meta-item post-author']/a/text()")[0]
                date = tree.xpath("//time[@class='post-meta-item post-date']/text()")[0]
                tags = tree.xpath("//a[@rel='tag']/text()")
                link = article_url

                # 将文章内容合并为一个字符串
                content_full = ''.join(content)

                # 随机等待3到1秒
                wait_time = random.uniform(1, 3)
                time.sleep(wait_time)

                # 将文章信息保存到数据库（去重查询）
                cursor.execute('''INSERT OR IGNORE INTO articles
                                  (title, link, author, date, tags, content)
                                  VALUES (?, ?, ?, ?, ?, ?)''',
                               (title, link, author, date, ', '.join(tags), content_full))
                conn.commit()

        except Exception as e:
            print(f"Error while downloading: {str(e)}")

# 创建一个队列来存放待爬取的文章链接
article_links_queue = Queue()

# 将队列分成三份
article_links = list(article_links_queue.queue)
chunk_size = len(article_links) // 3

# 创建三个线程来下载文章内容，每个线程处理一个分块
threads = []
for i in range(3):
    chunk = article_links[i * chunk_size : (i + 1) * chunk_size]
    thread = threading.Thread(target=download_article_content, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# 关闭数据库连接
conn.close()