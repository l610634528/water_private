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


class TestWater(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.driver = WaterMainPage(browser_type='chrome').get(self.URL, maximize_window=True)

    def tearDown(self):
        self.driver.quit()

    def test_increat_organization(self):
        self.driver.login()
        self.driver.increat_organization()
        # 断言判断是否新增成功
        # self.driver.test_1()
        element = self.driver.find_element(By.XPATH,
                                           "//div[1]/div/section/section/section/main/div[3]/div/div[3]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div").text
        print(element)
        try:
            self.assertEqual(element, '北京')
            print('新增机构成功！')
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main()
