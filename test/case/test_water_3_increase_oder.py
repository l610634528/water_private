"""终端环境"""
import os
import sys


from selenium.webdriver.common.by import By
import unittest
from selenium import webdriver
# from test.common.page import Page
sys.path.append("F:\\test_FF_number2\\utils")

from config import Config, REPORT_PATH
sys.path.append("F:\\test_FF_number2\\test\\page")
from water_main_page import WaterMainPage
import time
from HTMLTestRunner import HTMLTestRunner


class TestWater(unittest.TestCase):
    URL = Config().get('URL')

    @classmethod
    def setUpClass(cls):
        cls.driver = WaterMainPage(browser_type='chrome').get(cls.URL, maximize_window=True)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_1_increat_order(self):
        self.driver.slide_verification_login()
        self.driver.increat_order()
        people_phone_1 = self.driver.water_booking_people_phone
        people_name = self.driver.people_name
        element_people_phone = self.driver.find_element(By.XPATH,
                                                        "//div/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[7]/div").text
        print(element_people_phone)
        print(people_name)

        # 断言判断是否新增成功
        try:
            self.assertEqual(people_phone_1, element_people_phone, "新增订单成功！")
            print("新增订单成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证预约人电话
    def test_2_search_phone(self):
        people_phone_2 = self.driver.water_booking_people_phone
        self.driver.find_element(By.XPATH, "//input[@placeholder='预约人/预约人电话']").send_keys(people_phone_2)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        time.sleep(2)
        element_people_phone_2 = self.driver.find_element(By.XPATH,
                                                          "//div/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[7]/div").text
        print(element_people_phone_2)

        # 断言判断是否查询成功
        try:
            self.assertEqual(people_phone_2, element_people_phone_2, "查询预约人电话成功！")
            print("查新预约人电话成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证预约人姓名
    def test_3_search_name(self):
        self.driver.driver_refresh()
        booking_people_name = self.driver.people_name
        self.driver.find_element(By.XPATH, "//input[@placeholder='预约人/预约人电话']").send_keys(booking_people_name)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        time.sleep(2)
        element_people_name = self.driver.find_element(By.XPATH,
                                                       "//div/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[6]/div").text
        print(element_people_name)

        # 断言判断是否查询成功
        try:
            self.assertEqual(booking_people_name, element_people_name, "查询预约人姓名成功！")
            print("查询预约人姓名成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证预约人类型
    def test_4_search_type(self):
        self.driver.driver_refresh()
        people_type = "业主"
        self.driver.find_element(By.XPATH, "//input[@placeholder='请选择预约人类型']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/ul/li[1]/span").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        element_people_type = self.driver.find_element(By.XPATH,
                                                       "//*[@id='app']/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[8]/div").text

        print(element_people_type)

        # 断言判断是否查询成功
        try:
            self.assertEqual(people_type, element_people_type, "查询预约人类型成功！")
            print("查询预约人类型成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证订单状态
    def test_5_search_order_type(self):
        self.driver.driver_refresh()
        order_type = "待处理"
        self.driver.find_element(By.XPATH, "//input[@placeholder='状态']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/ul/li[1]").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        element_order_type = self.driver.find_element(By.XPATH,
                                                      "//*[@id='app']/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[15]/div/div").text
        print(element_order_type)

        # 断言判断是否查询成功
        try:
            self.assertEqual(order_type, element_order_type, "查询预约人类型成功！")
            print("查询订单为待处理类型成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证业主姓名查询
    def test_6_owner_name(self):
        self.driver.driver_refresh()
        owner_people_name = self.driver.people_name
        self.driver.find_element(By.XPATH, "//input[@placeholder='业主姓名/业主电话']").send_keys(owner_people_name)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        time.sleep(2)
        element_people_name = self.driver.find_element(By.XPATH,
                                                       "//*[@id='app']/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr/td[11]/div").text
        print(element_people_name)

        # 断言判断是否查询成功
        try:
            self.assertEqual(owner_people_name, element_people_name, "查询预约人姓名成功！")
            print("查询业主姓名成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证预约类型查询
    def test_7_types_of_precontract(self):
        self.driver.driver_refresh()
        Types_of_precontract = '电话预约'
        self.driver.find_element(By.XPATH, "//input[@placeholder='请选择预约类型']").click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/ul/li[1]/span").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        time.sleep(2)
        element_types_of_precontract = self.driver.find_element(By.XPATH,
                                                                "//*[@id='app']/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr/td[3]/div").text
        print(element_types_of_precontract)
        # 断言判断是否查询成功
        try:
            self.assertEqual(Types_of_precontract, element_types_of_precontract, "查询预约人姓名成功！")
            print("验证预约类型查询成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))

    # 验证省市区查询
    def test_8_provinces(self):
        self.driver.driver_refresh()
        provinces_address = '北京市北京市东城区'
        self.driver.find_element(By.XPATH, "//input[@placeholder='请选择省']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/ul/li[1]").click()
        self.sleep(1)
        self.driver.find_element(By.XPATH, "//input[@placeholder='请选择市']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[1]/ul/li").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "input[@placeholder='请选择区/县']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[1]/ul/li[1]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='search-form_button']//button[.='查询']").click()
        time.sleep(2)
        element_provinces = self.driver.find_element(By.XPATH, "//*[@id="app"]/div/section/section/section/div[2]/div[1]/div/main/div[3]/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[9]/div").text
        element_provinces_list = element_provinces[0:9]
        print(element_provinces)
         # 断言判断是否查询成功
        try:
            self.assertEqual(provinces_address, element_provinces_list, "验证省市区查询成功！")
            print("验证预约类型查询成功！")
        except Exception as e:
            print('Assertion test fail.', format(e))


if __name__ == '__main__':
    testunit = unittest.TestSuite()  # 定义一个单元测试容器
    testunit.addTest(TestWater('test_1_increat_order'))  # 将测试用例加入到测试容器中
    testunit.addTest(TestWater('test_2_search_phone'))
    testunit.addTest(TestWater('test_3_search_name'))
    testunit.addTest(TestWater('test_4_search_type'))
    testunit.addTest(TestWater('test_5_search_order_type'))
    testunit.addTest(TestWater('test_6_owner_name'))
    testunit.addTest(TestWater('test_7_types_of_precontract'))
    testunit.addTest(TestWater('test_8_provinces'))

    now = time.strftime('%Y-%m-%d_%H_%M', time.localtime(time.time()))
    report_dir = REPORT_PATH + '\\%s.html' % now
    re_open = open(report_dir, 'wb')
    runner = HTMLTestRunner(
        stream=re_open,
        title='Report_title',
        description='Report_description')
    runner.run(testunit)  # 自动进行测试

    # 注意，运行的时候，需要使用python
    # run，不能以unittest运行，否则不能生成测试报告。 原因是
    # pycharm的Run unittest会直接运行用例，不走下面的main函数。
