# -*- coding: utf-8 -*-

""" a test module """
"""终端环境"""
# from time import sleep
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import sys

# sys.path.append('F:\\test_FF\\utils')
# from log import logger
# from config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
# from file_reader import ExcelReader
# from HTMLTestRunner import HTMLTestRunner
#
# # sys.path.append("F:\\test_FF\\test\\page")
# sys.path.append("..\\page")
# from water_main_page import WaterMainPage

"""终端环境"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys
sys.path.append('F:\\test_FF_number2\\utils')
from log import logger
from config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from file_reader import ExcelReader
from HTMLTestRunner import HTMLTestRunner
sys.path.append("F:\\test_FF_number2\\test\\page")
from water_main_page import WaterMainPage


class TestWater(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.driver = WaterMainPage(browser_type='chrome').get(self.URL, maximize_window=True)

    def tearDown(self):
        self.driver.quit()

    def test_water_login(self):
        self.driver.slide_verification_login()
        


if __name__ == '__main__':
    unittest.main()
