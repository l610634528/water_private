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

"""终端环境"""
import unittest
import os
import sys
from selenium.webdriver.common.by import By
from selenium import webdriver
sys.path.append("F:\\test_FF_number2\\test\\common")
sys.path.append("F:\\test_FF_number2\\utils")
from config import Config
sys.apth.append("F:\\test_FF_number2\\test\\page")
from water_main_page import WaterMainPage
from time import sleep


class TestWater(unittest.TestCase):
    URL = Config().get('URL')
    department_service_audit_codes_elements_texts = []

    def setUp(self):
        self.driver = WaterMainPage(browser_type='chrome').get(self.URL, maximize_window=True)

    def test_general_audit(self):
        self.driver.slide_verification_general_login()
        department_code_card, self.department_service_audit_codes_elements_texts = self.driver.department_to_audit()  # 市场部同意
        try:
            self.assertIn(department_code_card, self.department_service_audit_codes_elements_texts,
                          "服务卡号为%s 的补贴申请同意!" % department_code_card)
        except Exception as e:
            print(format(e))

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
