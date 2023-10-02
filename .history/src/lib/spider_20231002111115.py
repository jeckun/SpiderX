from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    def __init__(self, thread_no: int):
        self.__thread_no = thread_no if thread_no else THREADNO
        self.__page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()

    def load_page(self, url):
        return self.__page.get(url)
    
    def get_all_element(self, info_xpath: str):
        return page.s_eles(f'xpath:{info_xpath}')