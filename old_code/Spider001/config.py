import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
