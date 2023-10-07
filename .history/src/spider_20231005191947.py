import time
import random
from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage
from DataRecorder import Recorder

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    # table=[]
    # current_table=0
    def __init__(self, thread_no=THREADNO):
        self.thread_no = thread_no
        self.page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()

    def get(self, url):
        element=self.page.get(url)
        time.sleep(random.randint(5, 10))
        return element

    def find_elements_by_xpath(self, xpath: str):
        return self.page.s_eles(f'xpath:{xpath}')
    