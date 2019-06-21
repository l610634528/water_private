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
from selenium.webdriver.common.by import By
import unittest
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

    def test_2_increat_order(self):
        self.driver.login()
        self.driver.increat_order()
        element_service_code = self.driver.find_element(By.XPATH,
                                                        "//div[1]/div/section/section/section/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[5]/div").text
        print(element_service_code)

        # 断言判断是否新增成功
        try:
            self.assertEqual(self.driver.water_service_code, element_service_code, "新增订单失败！")
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    unittest.main()
