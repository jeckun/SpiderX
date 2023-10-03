from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage
from DataRecorder import Recorder

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    def __init__(self, thread_no=THREADNO):
        self.thread_no = thread_no
        self.page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()
        # self.get(host)
        # self.recorder=Recorder('data.csv')

    def get(self, url):
        return self.page.get(url)

    def find_elements(self, xpath: str):
        return self.page.s_eles(f'xpath:{xpath}')
    
    def get_article(self, url:str, xpath:str):
        self.page.get(url)
        cts = self.page.eles(f'{xpath}')
        return [p.text for p in cts]
    # def get_all_element_path(self, info_xpath: str):
    #     return self.__page.s_eles(f'xpath:{info_xpath}')
    
    # def get_all_element_tag(self, tag: str):
    #     return self.__page.eles(tag)

    # def get_a_text(self, xpath: str):
    #     return self.get_all_element_path(xpath)[0].text