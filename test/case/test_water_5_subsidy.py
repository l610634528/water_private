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
sys.path.append("F:\\test_FF_number2\\test\\page")
from water_main_page import WaterMainPage
from time import sleep


class TestWater(unittest.TestCase):
    URL = Config().get('URL')
    subsidy_service_audit_codes_elements_texts = []
    department_service_audit_codes_elements_texts = []
    general_service_codes_elements_texts = []
    # 查看
    examine = ("//div[@class='el-table__fixed-body-wrapper']//span[.='查看']")

    @classmethod
    def setUpClass(cls):
        cls.driver = WaterMainPage(browser_type='chrome').get(cls.URL, maximize_window=True)

    # 市场部审核
    def test_01_subsidy_audit(self):
        self.driver.slide_verification_marketing_login_all()  # 市场部登录
        subsidy_code_card, self.subsidy_service_audit_codes_elements_texts = self.driver.subsidy_operation()  # 市场部同意
        try:
            self.assertIn(subsidy_code_card, self.subsidy_service_audit_codes_elements_texts,
                          "服务卡号为%s 的补贴申请同意!" % subsidy_code_card)
        except Exception as e:
            print(format(e))
        sleep(3)

    # 综合科初审
    def test_02_general_audit(self):

        department_code_card, self.department_service_audit_codes_elements_texts = self.driver.department_to_audit()  # 市场部同意
        try:
            self.assertIn(department_code_card, self.department_service_audit_codes_elements_texts,
                          "服务卡号为%s 的补贴申请同意!" % department_code_card)
        except Exception as e:
            print(format(e))
        sleep(3)

    # 综合科复审
    def test_03_General_review(self):
        general_code_card, self.general_service_codes_elements_texts = self.driver.General_review()  # 市场部同意
        try:
            self.assertIn(general_code_card, self.general_service_codes_elements_texts,
                          "服务卡号为%s 的补贴申请同意!" % general_code_card)
        except Exception as e:
            print(format(e))
        sleep(3)

    # 生成报表，总监批次表审核通过
    def test_04_major_audit(self):
        self.driver.majordomo_to_audit()
        sleep(3)
        examine = self.driver.find_element(By.XPATH, "/div[@class='el-table__fixed-body-wrapper']//span[.='查看']")
        try:
            self.assertEqual(examine.text, "查看")
        except Exception as e:
            print(format(e))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
