# -*- coding: utf-8 -*-
import os
import time
from src.site import Site
from src.lib.base import config, wait
import threading

CONFIG =config('config.ini')

# 获取下载列表
def collect_list(start, end):
    id = threading.current_thread().ident
    print("%d# starting." % id)
    site = Site(start)
    for i in range(start, end+1):
        site.get_list()
        site.next()
        print("%d# collect page %d." % (id, i))
        time.sleep(10)
    print("%d# is end." % id)

def get_star_end(s, e, t):
    for i in range(s,e,t):
        if i+t > e:
            yield i, e
        else:
            yield i, t + i -1


if __name__ == '__main__':

    print(f"Start download stories from site.")

    # 计划下载页数
    pages = [1, 20]
    # collect_list(pages[0], pages[1])
    # print(len(site.lists))

    # 多线程同时处理
    max_lines = int(CONFIG['max_lines']) 
    max_lines = max_lines if int(max_lines) < pages[1] else pages[1]

    thd = []
    s_e = []
    step=round((pages[1]-pages[0]+1)/max_lines)
    s_e += get_star_end(pages[0], pages[1], step)
    for i in range(len(s_e)):
        thd.append(threading.Thread(target=collect_list, args=(s_e[i][0] , s_e[i][1])))
        thd[i].start()
        time.sleep(1)
        wait(max_linex=max_lines) # 检测子线程是否执行完毕，执行完成再启动新的子线程
        # while True:        
        #     if len(threading.enumerate()) <= max_lines:
        #         break
        #     time.sleep(10)

    print(f"Download completed.")

