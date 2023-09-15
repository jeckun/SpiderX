# SpiderX

> 项目目标 :
> 实现通过脚本定期自动下载互联网的各类资源，并记录各类资源的来源及相关信息。


## 相关依赖

python3.11 + DrissionPage + Sqlite

## 使用方法

$ python manager.py <jobs.ls>

## 脚本模板 -- jobs.ls

```python
{
    'site_title': 'XXX博客',
    'host': 'https://www.xxxx.com',
    'jobs': {
        'start': 0,         # 开始页面
        'end': 10,          # 截至页面
        'route': "/page/%d",
        'task_list': "//main/article/headr/h2/a',
    },
    'article_xpath':{
        'title': '',
        'author': '',
        'time': '',
        'type': '',
        'tag': '',
        'content':'//main/article/div/p',
    }
}
```
