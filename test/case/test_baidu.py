# -*- coding: utf-8 -*-
""" a test module """
from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

sys.path.append('F:\\test_FF\\utils')
from log import logger
from config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from file_reader import ExcelReader
from HTMLTestRunner import HTMLTestRunner

# sys.path.append("F:\\test_FF\\test\\page")
sys.path.append("..\\page")
from baidu_result_page import BaiDuMainPage, BaiDuResultPage


class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')
    excel = DATA_PATH + '/baidu.xls'

    def setUp(self):
        self.driver = BaiDuMainPage(browser_type='chrome').get(self.URL, maximize_window=False)

    def tearDown(self):
        self.driver.quit()

    def test_search(self):
        self.driver.search()


if __name__ == '__main__':
    unittest.main()
