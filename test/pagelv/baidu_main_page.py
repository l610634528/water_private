from selenium.webdriver.common.by import By
import sys

sys.path.append("..\\common")
from page import Page

sys.path.append("F:\\test_FF\\utils")
from file_reader import ExcelReader
from config import Config, DATA_PATH


class BaiDuMainPage(Page):
    URL = Config().get('URL')
    excel = DATA_PATH + '/baidu.xls'
    loc_search_input = (By.ID, 'kw')
    loc_search_button = (By.ID, 'su')

    def element(self, kw):
        """搜索功能"""
        self.find_element(*self.loc_search_input).send_keys(kw)
        self.find_element(*self.loc_search_button).click()

    def search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['search'])
            self.wait_time()
