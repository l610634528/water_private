# -*- coding: utf-8 -*-

""" a test module """
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import urllib.request
import cv2
import numpy as np


def show(name):
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


driver = webdriver.Chrome()
url = 'http://test.waterhome.zcabc.com/#/login'


def get_login(driver, url):
    driver.get(url)
    driver.maximize_window()
    elem = driver.find_element_by_xpath('//input[@placeholder="请输入手机号码"]')
    elem.send_keys('15067126937')
    elem = driver.find_element_by_xpath('//input[@placeholder="请输入密码"]')
    elem.send_keys('12345678')
    # elem = driver.find_element_by_xpath('//*[@id="login"]')
    # elem.click()
    sleep(2)
    # driver.switch_to_frame("tcaptcha_iframe")
    return driver


driver = get_login(driver, url)


# 获取验证码中的图片
def get_image(driver):
    article = driver.find_element_by_xpath('//i[@class="fa fa-long-arrow-right common-icon right-arrow"]')
    sleep(2)
    print(1)
    ActionChains(driver).move_to_element(article).perform()
    image1 = driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div/form/div[3]/div/div[2]/div[1]/div[1]/div/img').get_attribute('src')
    image2 = driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div/form/div[3]/div/div[2]/div[1]/div[1]/div/div/img').get_attribute('src')
    req = urllib.request.Request(image1)
    bkg = open('slide_bkg.png', 'wb+')
    bkg.write(urllib.request.urlopen(req).read())
    bkg.close()
    req = urllib.request.Request(image2)
    blk = open('slide_block.png', 'wb+')
    blk.write(urllib.request.urlopen(req).read())
    blk.close()
    return 'slide_bkg.png', 'slide_block.png'


# bkg是大背景图，blk是小模块背景图片
bkg, blk = get_image(driver)


# 计算缺口的位置，由于缺口位置查找偶尔会出现找不准的现象，这里进行判断，如果查找的缺口位置x坐标小于450，我们进行刷新验证码操作，重新计算缺口位置，知道满足条件位置。（设置为450的原因是因为缺口出现位置的x坐标都大于450）
def get_distance(bkg, blk):
    block = cv2.imread(blk, 0)
    template = cv2.imread(bkg, 0)
    cv2.imwrite('template.jpg', template)
    cv2.imwrite('block.jpg', block)
    block = cv2.imread('block.jpg')
    block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
    block = abs(255 - block)
    # imwrite保存图像
    cv2.imwrite('block.jpg', block)
    # imread读取图像
    block = cv2.imread('block.jpg')
    template = cv2.imread('template.jpg')
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
    y, x = np.unravel_index(result.argmax(), result.shape)
    # 这里就是下图中的绿色框框?
    cv2.rectangle(template, (x , y), (x + 77, y + 77), (7, 249, 151), 2)
    # x是缺口坐标
    print('x坐标为：%d' % (x + 5))
    if x < 100:
        # 刷新验证码图片
        elem = driver.find_element_by_xpath('//*[@class="code-reload"]')
        sleep(1)
        elem.click()
        bkg, blk = get_image(driver)
        x, template = get_distance(bkg, blk)
    return x, template


# distance为大图背景中缺陷位置， template为小模块位置？
distance, template = get_distance(bkg, blk)


# 这个是用来模拟人为拖动滑块行为，快到缺口位置时，减缓拖动的速度，服务器就是根据这个来判断是否是人为登录的。
def get_tracks(dis):
    v = 0
    t = 0.3
    # 保存0.3内的位移
    tracks = []
    current = 0
    mid = distance * 4 / 5
    while current <= dis:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        s = v0 * t + 0.5 * a * (t ** 2)
        current += s
        tracks.append(round(s))
        v = v0 + a * t
    return tracks


# 原图的像素是680*390，而网页的是340*195，图像缩小了一倍。
# 经过尝试，发现滑块的固定x坐标为70，这个地方有待加强，这里加20的原因上面已经解释了。
def weizhi():
    double_distance = int(distance / 1.19)
    tracks = get_tracks(double_distance)
    # 由于计算机计算的误差，导致模拟人类行为时，会出现分布移动总和大于真实距离，这里就把这个差添加到tracks中，也就是最后进行一步左移。
    tracks.append(-(sum(tracks) - double_distance))
    return tracks

element = driver.find_element_by_xpath("//i[@class='fa fa-long-arrow-right common-icon right-arrow']")
ActionChains(driver).click_and_hold(on_element=element).perform()
tracks_list = weizhi()
for track in tracks_list:
    ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
sleep(3)
ActionChains(driver).release(on_element=element).perform()
show(template)
