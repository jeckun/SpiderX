from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage
from DataRecorder import Recorder

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    def __init__(self, host, thread_no=THREADNO):
        self.__thread_no = thread_no
        self.__page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()
        # self.get(host)
        # self.recorder=Recorder('data.csv')

    def get(self, url):
        return self.__page.get(url)

    def find_elements(self, xpath: str):
        return self.__page.s_eles(xpath)
    
    def get_all_element_path(self, info_xpath: str):
        return self.__page.s_eles(f'xpath:{info_xpath}')
    
    def get_all_element_tag(self, tag: str):
        return self.__page.eles(tag)

    def get_a_text(self, xpath: str):
        return self.get_all_element_path(xpath)[0].text