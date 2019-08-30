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
import os
import sys
from selenium.webdriver.common.by import By
from selenium import webdriver
sys.path.append("F:\\test_FF_number2\\test\\common")
sys.path.append("F:\\test_FF_number2\\utils")
from config import Config
sys.path.append("F:\\test_FF_number2\\test\\page")
from water_main_page import WaterMainPage

class TestWater(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.driver = WaterMainPage(browser_type='chrome').get(self.URL, maximize_window=True)

    def tearDown(self):
        self.driver.quit()

    def del_org(self):
        element = self.driver.find_element(By.XPATH,
                                           "//div[1]/div/section/section/section/main/div[3]/div/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div").text

        self.driver.del_organization()
        try:
            self.assertIsNone(element)
            print('删除成功！')
        except Exception as e:
            print('Assertion test fail.', format(e))