# -*- coding: utf-8 -*-
import os
import time
from src.site import Site
from src.lib.base import config, wait
import threading

CONFIG =config('config.ini')



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

    # 多线程同时处理
    max_lines = int(CONFIG['max_lines']) 
    max_lines = max_lines if int(max_lines) < pages[1] else pages[1]

    thd = []
    s_e = []
    step=round((pages[1]-pages[0]+1)/max_lines)
    s_e += get_star_end(pages[0], pages[1], step)
    for i in range(len(s_e)):
        site = Site()
        thd.append(threading.Thread(target=site.collect_list, args=(s_e[i][0] , s_e[i][1])))
        thd[i].start()
        time.sleep(1)
        wait(max_linex=max_lines) # 检测子线程是否执行完毕，执行完成再启动新的子线程

    print(f"Download completed.")

