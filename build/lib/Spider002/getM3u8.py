#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: Eric
# time: 2020-8-13

import requests
import os
import random
import time
import m3u8
from config import header

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def file_filter(f):
    if f[-3:] in ['.ts']:
        return True
    else:
        return False


class SpiderVideo(object):
    def __init__(self):
        self.filename = ''
        self.uri = ''
        self.down_path = os.path.join(BASE_DIR, 'iSpider', 'Cache')
        self.final_path = os.path.join(BASE_DIR, 'iSpider', 'Output')
        self.headers = {}

        if not os.path.isdir(self.down_path):
            os.makedirs(self.down_path)
        if not os.path.isdir(self.final_path):
            os.makedirs(self.final_path)

    def get_uri_from_m3u8(self, uri=""):
        try:
            print("正在获取: index.m3u8")
            m3u8Obj = m3u8.load(uri=uri, headers=self.headers, verify_ssl=False)
            print("正在解析...")
            if not m3u8Obj.segments:
                ts_uri = m3u8Obj.playlists[0].absolute_uri
                m3u8Obj = m3u8.load(uri=ts_uri, headers=self.headers, verify_ssl=False)

            with open('index.m3u8', 'wb') as file:
                file.write(requests.get(uri).content)
            print("解析完成!")
        except Exception as e:
            print(e)
            return {}
        return m3u8Obj.segments

    def get_ts_from_m3u8_list(self, uriList):
        count = len(uriList)
        for i in range(0, len(uriList)):
            name = os.path.basename(uriList[i].absolute_uri)
            if os.path.isfile(name):
                print('已经下载: %s' % name)
                continue
            else:
                try:
                    get_time = time.time()
                    # 获取视频片段
                    resp = requests.get(uriList[i].absolute_uri, headers=self.headers)
                    time.sleep(random.randint(1, 3))
                    print('正在下载: %s     进度：%.2f%%      耗时 %d s' %
                          (name, i/count*100, time.time() - get_time))
                except Exception as e:
                    print(e)
                    continue

            with open(name, 'wb') as f:
                f.write(resp.content)

    def merge_ts_to_mp4(self):
        files = os.listdir(self.down_path)
        files.sort()
        files = list(filter(file_filter, files))

        output_file = os.path.join(self.final_path, self.filename + '.mp4')

        with open(output_file, 'wb') as file:
            for tsf in files:
                with open(os.path.join(self.down_path, tsf), 'rb') as ts:
                    for line in ts:
                        file.write(line)
                    print('正在合并: %s' % tsf)
                    file.write(b'\n')
                    os.remove(tsf)

    def run(self, filename, uri, headers):
        print("Start!\n开始下载: %s" % filename)
        self.filename = filename
        self.uri = uri
        self.headers = headers

        # 创建缓存目录
        self.down_path = os.path.join(BASE_DIR, 'iSpider', 'Cache', filename)
        if not os.path.isdir(self.down_path):
            os.makedirs(self.down_path)
        os.chdir(self.down_path)

        start_time = time.time()
        print("正在获取下载列表...")
        uriList = self.get_uri_from_m3u8(uri)
        if not uriList:
            print("下载失败.")
            return

        # 开始下载视频片段
        self.get_ts_from_m3u8_list(uriList)
        print("下载完成！总共耗时 %d s" % (time.time()-start_time))

        print("开始进行合并片段……")
        self.merge_ts_to_mp4()

        print("下载完成： %s " % os.path.join(self.final_path, self.filename + '.mp4'))


if __name__ == '__main__':

    filename = '监狱戦舰 Vol.02 洗脳改造'
    uri = "https://605ziyuan.com/20180527/kqplRkpI/index.m3u8"

    crawler = SpiderVideo()
    crawler.run(filename, uri, header)
