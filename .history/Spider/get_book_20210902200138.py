#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Lib import Spider, CONFIG, BASE_DIR, mkdir

# 配置参数
CONFIG['cookies'] = {
    '?': '?',           # 此处放 cookies
}

CONFIG['headers'] = {
    '?': '?',           # 此处放 headers
}

CONFIG['site_name']='网站名，下载的文件会放到同名文件夹下'
CONFIG['channel']='频道名称，以便区分不同的频道'
CONFIG['host'] = '站点的域名，如：https://www.TCL20190711.com/'
CONFIG['url'] = '下载列表的首页链接：如：https://www.TCL20190711.com/pw/thread.php'
CONFIG['min'] = 1    # 下载列表的开始页码
CONFIG['max'] = 100  # 下载列表的截止页码
CONFIG['selector'] = '#ajaxtable tbody tr td:nth-child(2)>h3>a'     # 下载列表的 css_selector
CONFIG['params'] = {}   # 如果URL是带有参数传递，可以使用。也可以不使用，每次直接修改url中参数的字符串
CONFIG['table_id'] = 'ajaxtable'     # 如果下载的列表，在一个table中，并且有Table id，可以使用。否则，直接在get_list函数中写获取代码。
CONFIG['article_content_css_selector'] = 'div#read_tpc'     # 这是点击下载列表中链接后，文章内容的定位 css_selector

# 获取下载列表
def get_list(id=0):
    # “以下代码需要根据下载列表网页结构判断后重写，主要是需要返回一个列表，这个列表包括：频道名、文章名称、文章内容网址【完整的网址】。”
    CONFIG['params'] = (
        ('fid', '17'),
        ('page', id),
    )
    sp.load(CONFIG['url'], CONFIG['params'])

    lis = []
    try:
        table = sp.soup.find("table", {"id" : CONFIG['table_id']})
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            lis += fix(cells)
        return lis
    except Exception as err:
        print('解析表格数据错误：', err)


# 用来处理表格中每一行的数据，从中筛选出需要的文章类型、名称和链接。
def fix(cells):
    # “本函数可有可无，视情况而定。主要是为了解析表格内容，获取到频道名、文章名称和文章下载链接。”
    # “如果重写本函数，则需要将获取到频道名、文章名称和文章下载链接的功能写入get_list函数。”

    ls = []
    if not cells: return ls
    try:
        if len(cells) == 5:
            tag = cells[1].find('a').text
            if len(tag) > 10:
                return ls
            name = cells[1].find('h3').find('a').text[7:].replace('\xa0','').replace(' ','')
            href = CONFIG['host']+cells[1].find('h3').find('a').attrs['href']
            ls.append([tag, name, href])
            print(tag, name, href)
            return ls
        else:
            return ls
    except:
        return ls

# 格式化下载列表，用以缓存
def formart_link_list(formart_obj):
    content = ''
    for line in formart_obj:
        content += line[0] + '\t' + line[1] + '\t' + line[2] + '\n'
    return content

# 加载文件列表
def load_txt_fun(line, formart_obj):
    tag, name, url = line.replace('\n','').split('\t')
    formart_obj.append([tag, name, url])

# 格式化文章内容
def formart_content_fun(content, title, tag):
    try:
        book = '<HTML><HEAD><TITLE>%s %s</TITLE><HEAD><Body>\n' % (tag, title)
        book += '<H2>%s %s</H2>' % (tag, title)
        book += str(content)
        book += '</Body></HTML>'
        return book
    except Exception as err:
        print('解析内容失败...', err)
        return ''


# 启动爬虫
sp = Spider()
sp.run(get_list, formart_link_list, sp.lists, load_txt_fun, formart_content_fun)
