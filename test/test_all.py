# -*- coding: utf-8 -*-

""" a test module """
# -*- coding: utf-8 -*-

' a test module '
"""终端环境"""
# import sys
# sys.path.append('..\\utils')
# from HTMLTestRunner import HTMLTestRunner
# from config import description, reporttitle, REPORT_PATH, TEST_PATH
# from mail import Email
# import unittest
# import time
"""pycharm"""
from HTMLTestRunner import HTMLTestRunner
from utils.config import description, reporttitle, REPORT_PATH, TEST_PATH
from utils.mail import Email
import unittest
import time


case_path = TEST_PATH


def create_report():
    test_suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_path,
                                                   pattern='test*.py',
                                                   top_level_dir=None)
    for test in discover:
        for test_case in test:
            test_suit.addTest(test_case)
    now = time.strftime('%Y-%m-%d_%H_%M', time.localtime(time.time()))
    report_dir = REPORT_PATH + '\\%s.html' % now
    re_open = open(report_dir, 'wb')
    runner = HTMLTestRunner(stream=re_open,
                            title=reporttitle,
                            description=description)
    runner.run(test_suit)
    re_open.close()
    e = Email(title='自动化测试报告',
              message='',
              receiver='lvxj@zhongcai.com',
              server='smtp.163.com',
              sender='l610634528@163.com',
              password='lvxj64518881',
              path=report_dir)
    e.mail_send()


create_report()
