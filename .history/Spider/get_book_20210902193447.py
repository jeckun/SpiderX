#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Lib import Spider, CONFIG, BASE_DIR, mkdir

# 配置参数
CONFIG['cookies'] = {
    '__utmc': '1',
    '__utmz': '1.1630167702.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '__utma': '1.1750071294.1628755251.1630172759.1630257364.5',
    '__utmt': '1',
    'cdb3_oldtopics': 'D4357825D3823560D7799711D2259909D',
    'cdb3_sid': '1dpYNS',
    '__utmb': '1.12.10.1630257364',
}

CONFIG['headers'] = {
    'authority': 'k5.kcl20190711.rocks',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://k5.kcl20190711.rocks/pw/index.php',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'UM_distinctid=17b8dbc00804b3-05d017a6d07087-35667c03-fa000-17b8dbc0081757; aafaf_cknum=BQEBVlQCBwwGDjE8X11VA1cGAVIEUQIGUw0ICg0FBw9SBwBQBAECUFdQUw4%3D; aafaf_winduser=BQMHXlIHAjFSDQ9WVQhSBFYFDQdWAFAHBllWDg8NVQxXCAIBDVMCA28%3D; aafaf_ck_info=%2F%09; aafaf_threadlog=%2C182%2C60%2C25%2C17%2C; aafaf_readlog=%2C5481496%2C5481494%2C5449519%2C5457411%2C5457408%2C5421040%2C5413513%2C5031743%2C5474592%2C846891%2C; aafaf_ol_offset=4947; aafaf_lastpos=index; aafaf_lastvisit=9444%091630293254%09%2Fpw%2Findex.php%3F; CNZZDATA1261158850=375940777-1630164525-%7C1630286431',
}

CONFIG['site_name']='BT伙计'
CONFIG['channel']='小说'
CONFIG['host'] = 'https://k5.kcl20190711.rocks/pw/'
CONFIG['url'] = 'https://k5.kcl20190711.rocks/pw/thread.php'
CONFIG['min'] = 1
CONFIG['max'] = 100
CONFIG['selector'] = '#ajaxtable tbody tr td:nth-child(2)>h3>a'
CONFIG['params'] = {}
CONFIG['table_id'] = 'ajaxtable'
CONFIG['article_content_css_selector'] = 'div#read_tpc'

# 获取下载列表
def get_list(id=0):
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
