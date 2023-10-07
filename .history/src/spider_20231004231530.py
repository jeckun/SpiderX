import time
import random
from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage
from DataRecorder import Recorder

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    table=[]
    current_table=0
    def __init__(self, thread_no=THREADNO):
        self.thread_no = thread_no
        self.page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()
        self.page.get('chrome://version/')
        self.table.append(self.page.get_tab())
        self.current_table=len(self.table)-1

    def add_tab(self):
        page = self.page.new_tab('chrome://version/')
        self.table.append(self.page.get_tab(page))
        return self.table[len(table)-1]

    def get(self, url):
        # element=self.page.get(url)
        element=self.table[self.current_table].get(url)
        time.sleep(random.randint(3, 6))
        return element

    def find_elements_by_xpath(self, xpath: str):
        return self.table[self.current_table].s_eles(f'xpath:{xpath}')
    
    # def find_elements_by_tag(self, tag:str):
    #     return self.page.eles(f'tag:{tag}')

    # def find_elements_by_attr(self, attr:str):
    #     return self.page.eles(f'@attr={attr}')

    # def find_elements_by_class(self, cls:str):
    #     return self.page.eles(f'@class={cls}')