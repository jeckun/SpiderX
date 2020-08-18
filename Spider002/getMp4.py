#!/usr/bin/python

# -*- coding: UTF-8 -*-

import os
import re
import requests


def get(path, url):

    url_name = []  # url name

    if not os.path.exists(path):
        os.makedirs(path)

    # 获取源码

    hd = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    }

    html = requests.get(url, headers=hd).text

    url_content = re.compile(r'(<div class="header span6"><a href=".*?">.*?</a></div>)', re.S)  # 编译

    url_contents = re.findall(url_content, html)  # 匹配

    for i in url_contents:

        # 匹配视频

        url_reg = r'<a href="(.*?)">(.*?)</a>'  # 视频地址

        url_items = re.findall(url_reg, i)

        if url_items:  # 找到匹配视频数据
            if url_items[0][0][0:1]=='/':

                url = 'https://ninghao.net' + url_items[0][0]

                html = requests.get(url, headers=hd).text  # 取播放页

                url_reg = r'<source src="(.*?)" type="video/mp4">'
                mp4_url = re.findall(url_reg, html)  # 找到mp4的地址

                if mp4_url:   # 判断是否找到
                    print(len(url_name) + 1, [url_items[0][1], mp4_url[0]])
                    url_name.append([url_items[0][1], mp4_url[0]])

    for i, m in zip(range(len(url_name)), url_name):  # i[1]=url i[0]=name

        file = path + '/' + str(i+1)+' '+m[0]+'.mp4'
        if file.count('/')>1:  # 检查文件名中是否含有"/"
            file = file[:file.find('/') + 1 + file[file.find('/')+1:].find('/')] + '&' + file[file.find('/') + 2 + file[file.find('/')+1:].find('/'):]
        if os.path.exists(file):
            continue
        print(i+1, file, m[1])
        with open(file, "wb") as f:
            # 保存视频
            f.write(requests.get(url=m[1], headers=hd,stream=True, verify=False).content)


if __name__ == "__main__":

    get('JavaScript 基础', 'https://hao.cn/course/1235')
