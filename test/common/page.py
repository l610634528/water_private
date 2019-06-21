# -*- coding: utf-8 -*-

""" a test module """
"""终端环境"""
# from browser import Browser
# from time import sleep
"""pycharm环境"""
from test.common.browser import Browser
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

# if __name__ == '__mian__':
#     h = Page()
#     h.random_match()
