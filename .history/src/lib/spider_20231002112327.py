from threading import Thread, enumerate
from DrissionPage import ChromiumPage, SessionPage

DOWNLOADTYPE = 'S'
THREADNO = 5

class Spider:
    def __init__(self, host, thread_no=THREADNO):
        self.__thread_no = thread_no
        self.__page = SessionPage() if DOWNLOADTYPE == 'S' else ChromiumPage()
        self.load_page(host)

    def load_page(self, url):
        return self.__page.get(url)

    def get_all_element(self, info_xpath: str):
        return page.s_eles(f'xpath:{info_xpath}')

    def get_a_text(self, xpath: str):
        return self.get_all_element(xpath)[0].text