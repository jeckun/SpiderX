# scrapy.py
import os
import scrapy
import sqlite3

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
        
        article_links = response.xpath('//header[@class="entry-header"]/h2/a/@href').extract()
        
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        # 获取下一页的链接并继续抓取，最多爬取10页
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page and self.page_number < 10:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        try:
            title = response.xpath('//header[@class="entry-header"]/h1/text()').get()
            author = response.xpath("//a[@class='url fn n']/text()").get()
            date = response.xpath('//footer/span[1]/a/time[1]/text()').get()
            tags = response.xpath('//span[@class="tags-links"]/a/text()').extract()
            link = response.url

            # 获取文章内容
            content = response.xpath("//main/article/div[1]/p/text()").extract()
            
            # 将文章内容合并为一个字符串
            content_full = ''.join(content)

            # 将文章信息保存到数据库（去重查询）
            cursor.execute('''INSERT OR IGNORE INTO articles
                              (title, link, author, date, tags, content)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (title, link, author, date, ', '.join(tags), content_full))
            conn.commit()

            # 保存文章内容到文件
            with open(f"temp/{title}.txt", "w", encoding="utf-8") as file:
                file.write(content_full)

        except Exception as e:
            self.log(f"Error while processing article: {str(e)}")

    def start_requests(self):
        self.page_number = 1  # 设置起始页数为1
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

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