
header = {
    'authority': 'www.cnblogs.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 '
                  'Safari/537.36',
    'accept': 'text/css,*/*;q=0.1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'style',
    'referer': 'https://www.cnblogs.com/',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

bookInf = {
    'url': 'https://www.17k.com/book/2389507.html',
    'title': 'body > div.Main > div.bLeft > div.BookInfo > div.Info.Sign > h1 > a',
    'author': 'body > div.Main.List > div.Author > a',
    'time': '#bookInfo > dt > em',
    'state': 'body > div.Main > div.bLeft > div.BookInfo > div.Info.Sign > div.label > a:nth-child(1) > span',
    'number': 'body > div.Main > div.bLeft > div.BookInfo > div.Info.Sign > div.BookData > p:nth-child(3) > em',
    'introduction': '#bookInfo > dd > div:nth-child(1) > p > a',
    'cover': '#bookCover > a > img',
    'catalog': 'body > div.Main > div.bLeft > div.BookInfo > div.Props > dl > dt > a',
    'catalog_list': 'body > div.Main.List > dl:nth-child(5) > dd > a',
    'chapter': '#readArea > div.readAreaBox.content',
}

script = {
    'openHome': bookInf['url'],
    'getText': {
        '_title': bookInf['title'],
        # '_author': bookInf['author'],
        '_time': bookInf['time'],
        '_state': bookInf['state'],
        '_number': bookInf['number'],
        '_introduction': bookInf['introduction'],
    },
    'getImg': {
        '_cover': bookInf['cover'],
    },
    'getHref': {
        '_catalog': 'body > div.Main > div.bLeft > div.BookInfo > div.Props > dl > dt > a',
    },
    'openCatalog': '打开章节目录',
    'getChapter': bookInf['chapter'],
}
