# -*- coding: utf-8 -*-
import os
import time
from src.site import Site


if __name__ == '__main__':

    print(f"Start download stories from site.")

    # 计划下载页数
    pages = [1, 2]
    site = Site()
    site.download(pages)
    
    print(f"Download completed.")
