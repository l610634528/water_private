# -*- coding: utf-8 -*-

""" a test module """
from telnetlib import EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui

"""终端环境"""
# from browser import Browser
# from time import sleep
"""pycharm环境"""
import os
import sys
sys.path.append("F:\\test_FF_number2\\test\\common")
from browser import Browser
from time import sleep


class Page(Browser):
    # 更多的封装请自己动手...
    def __init__(self, page=None, browser_type='firefox'):
        if page:
            self.driver = page.driver
        else:
            super(Page, self).__init__(browser_type=browser_type)

    def get_driver(self):
        return self.driver

    def find_element(self, *args):
        return self.driver.find_element(*args)

    def find_elements(self, *args):
        return self.driver.find_elements(*args)

    def wait_time(self, seconds=2):
        return sleep(seconds)

    def implicitly_wait_time(self, seconds=10):
        self.driver.implicitly_wait(seconds)

    # 判断元素是否存在
    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element(element)
            return flag
        except:
            flag = False
            return flag

    # 刷新页面判断元素是否存在
    def element_exits(self, element):
        if self.isElementExist(element):
            self.find_element(element).click()
        else:
            self.driver_refresh()
            self.element_exits()

    # 刷新页面
    def driver_refresh(self):
        return self.driver.refresh()

    # 切换frame页面
    def switch_to_frame(self, param):
        self.driver.switch_to.frame(param)

    # 切换alter
    def switch_to_alert(self):
        return self.driver.switch_to.alert

    # 页面前进
    def forward(self):
        return self.driver.forward()

    # 页面后退
    def back(self):
        return self.driver.back()

    # 默认等待元素出现10秒
    def is_visible(self, locator, timeout=10):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    # 元素存在则执行用例xpath
    def implement_xpath(self, locator):
        if self.is_visible(locator):
            self.wait_time()
            self.find_element(By.XPATH, locator).click()
        else:
            print("未找到元素")

    # 元素存在则执行用例css
    def implement_css(self, locator):
        if self.is_visible(locator):
            self.find_element(By.CSS_SELECTOR, locator).click()
        else:
            print("未找到元素")



# if __name__ == '__mian__':
#     h = Page()
#     h.random_match()
