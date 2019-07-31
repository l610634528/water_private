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
    subsidy_service_audit_codes_elements_texts = []

    @classmethod
    def setUpClass(cls):
        cls.driver = WaterMainPage(browser_type='chrome').get(cls.URL, maximize_window=True)

    def test_01_subsidy_audit(self):
        self.driver.slide_verification_marketing_login_all()  # 市场部登录
        subsidy_code_card, self.subsidy_service_audit_codes_elements_texts = self.driver.subsidy_operation()  # 市场部同意
        try:
            self.assertIn(subsidy_code_card, self.subsidy_service_audit_codes_elements_texts,
                          "服务卡号为%s 的补贴申请同意!" % subsidy_code_card)
        except Exception as e:
            print(format(e))
        sleep(3)

    def test_02_general_audit(self):

        department_code_card, self.department_service_audit_codes_elements_texts = self.driver.department_to_audit()  # 市场部同意
        try:
            self.assertIn(department_code_card, self.department_service_audit_codes_elements_texts,
                          "服务卡号为%s 的补贴申请同意!" % department_code_card)
        except Exception as e:
            print(format(e))
            sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
