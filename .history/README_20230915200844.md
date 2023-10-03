# SpiderX

> 项目目标 :
> - 通过脚本自动下载互联网的各类资源
> - 灵活自定义记录各类资源的相关信息
> - 支持多线程下载


## 相关依赖

python3.11 + DrissionPage + Sqlite3.0

## 使用方法

$ python manager.py <jobs.json>

## 脚本模板 -- jobs.json

```python
{
    'site_title': 'XXX博客',
    'host': 'https://www.xxxx.com',
    'jobs': {
        'start': 0,         # 开始页面
        'end': 10,          # 截至页面
        'route': "/page/%d",
        'article_list_xpath': "//main/article/headr/h2/a',
    },
    'article_xpath':{
        'title': '',
        'author': '',
        'time': '',
        'type': '',
        'tag': '',
        'content':'//main/article/div/p',
    },
    'download':{
        'save_to_path':'',
    }
}
```
