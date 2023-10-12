# scrapy.py
# 

import scrapy
import sqlite3
import random
import time
import os

# 创建一个文件夹来保存爬取的内容
if not os.path.exists("temp"):
    os.mkdir("temp")

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

# 创建一个队列来存放待爬取的文章链接
article_links_queue = Queue()

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://zhaoze.pro']
    
    def parse(self, response):
        # 提取文章链接
        article_links = response.xpath('//header[@class="entry-header"]/h2/a/@href').extract()
        
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)
        
        for link in article_links:
            if link not in article_links_queue.queue:
                article_links_queue.put(link)

        # 获取下一页的链接并继续抓取
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        try:
            title = response.xpath("//h1[@class='post-title']/text()").get()
            author = response.xpath("//span[@class='post-meta-item post-author']/a/text()").get()
            date = response.xpath("//time[@class='post-meta-item post-date']/text()").get()
            tags = response.xpath("//a[@rel='tag']/text()").extract()
            link = response.url

            # 获取文章内容
            content = response.xpath("//div[@class='post-content']//text()").extract()
            
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

            # 保存文章内容到文件
            with open(f"Book/{title}.txt", "w", encoding="utf-8") as file:
                file.write(content_full)

        except Exception as e:
            self.log(f"Error while processing article: {str(e)}")

# 启动爬虫
if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'ROBOTSTXT_OBEY': False
    })

    process.crawl(MySpider)
    process.start()

# 关闭数据库连接
conn.close()