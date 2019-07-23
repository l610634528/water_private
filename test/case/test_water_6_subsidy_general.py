# -*- coding: utf-8 -*-

""" a test module """
"""终端环境"""
# import unittest
# from selenium import webdriver
# import sys
# sys.path.append("..\\common")
# from page import Page
# sys.path.append("F:\\test_FF\\utils")
# from config import Config
# from water_main_page import WaterMainPage
# from selenium.webdriver.common.by import By

"""pycharm环境"""
import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from test.common.page import Page
from utils.config import Config
from test.page.water_main_page import WaterMainPage
from time import sleep


class TestWater(unittest.TestCase):
    URL = Config().get('URL')


    def setUp(self):
        self.driver = WaterMainPage(browser_type='chrome').get(self.URL, maximize_window=True)

    def test_subsidy_audit(self):
        self.driver.login_general_audit()


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
