from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage
from DataRecorder import Recorder

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    def __init__(self, thread_no=THREADNO):
        self.thread_no = thread_no
        self.page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()

    def get(self, url):
        return self.page.get(url)

    def find_elements_by_xpath(self, xpath: str):
        return self.page.s_eles(f'xpath:{xpath}')
    
    def find_elements_by_tag(self, tag:str):
        return self.page.eles(f'tag:{tag}')

    def find_elements_by_attr(self, attr:str):
        return self.page.eles(f'@attr={attr}')

    def find_elements_by_class(self, cls:str):
        return self.page.eles(f'@class={cls}')