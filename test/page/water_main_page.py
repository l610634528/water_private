"""终端环境"""
# from selenium.webdriver.common.by import By
# import sys
# sys.path.append("..\\common")
# from page import Page
# (..\\test_FF\\utils)
# sys.path.append("F:\\test_FF\\utils")
# from file_reader import ExcelReader
# from generator import *
# from config import Config, DATA_PATH
"""pycharm环境"""
from selenium.webdriver.common.by import By
from test.common.page import Page
from utils.file_reader import ExcelReader
from utils.generator import *
from utils.config import Config, DATA_PATH
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image
from io import BytesIO

# from pip._vendor import requests
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import urllib.request
import cv2
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class WaterMainPage(Page):
    URL = Config().get('URL')
    excel = DATA_PATH + '/water.xlsx'
    loc_account = (By.XPATH, "//input[@placeholder='请输入手机号码']")
    loc_password = (By.XPATH, "//input[@placeholder='请输入密码']")
    loc_button = (By.XPATH, "//button[@class='el-button submit-info el-button--default']")

    # 登录功能
    def element(self, account, password):
        self.find_element(*self.loc_account).clear()
        self.find_element(*self.loc_account).send_keys(account)
        self.find_element(*self.loc_password).clear()
        self.find_element(*self.loc_password).send_keys(password)
        # self.find_element(*self.loc_button).click()

    # 滑动按键
    slide_pic = (By.XPATH, "//i[@class='fa fa-long-arrow-right common-icon right-arrow']")
    back_img = (By.CLASS_NAME, "back-img")
    front_img = (By.CLASS_NAME, "front-img")

    def get_pic(self):
        wait = WebDriverWait(self.get_driver(), 20, 0.5)
        sleep(2)
        article = self.find_element(*self.slide_pic)
        ActionChains(self.driver).move_to_element(article).perform()  # 把鼠标放在滑动键上
        target = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'back-img')))
        template = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'front-img')))
        # target = self.find_element(*self.back_img)  # 背景图
        # template = self.find_element(*self.front_img)  # 滑动图
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 400 / int(size_loc[0])

    def match(self, target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        run = 1
        w, h = template.shape[::-1]
        print(w, h)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            # print(threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            # print(len(loc[1]))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                # print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2
        return loc[1][0]

    def get_tracks(self, distance):
        print(distance)
        distance += 20
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 3 / 5  # 减速阀值
        while current < distance:
            if current < mid:
                a = 2  # 加速度为+2
            else:
                a = -3  # 加速度-3
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))

        back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def crack_slider(self, tracks):
        wait = WebDriverWait(self.get_driver(), 20, 0.5)
        # sleep(1)
        # slider = self.find_element(*self.slide_pic)
        slider = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//i[@class="fa fa-long-arrow-right common-icon right-arrow"]')))
        ActionChains(self.driver).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()

        sleep(0.5)
        # for back_tracks in tracks['back_tracks']:
        #     ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=0).perform()

        ActionChains(self.driver).move_by_offset(xoffset=-4, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=4, yoffset=0).perform()
        sleep(0.5)
        ActionChains(self.driver).release().perform()

    def slide_verification_login(self):
        self.login()
        target = 'target.jpg'
        template = 'template.png'
        self.get_pic()
        distance = self.match(target, template)
        tracks = self.get_tracks((distance + 6.5) * (self.zoom))  # 对位移的缩放计算
        self.crack_slider(tracks)
        sleep(1)
        self.fail_refresh_success_login()

    # 滑动失败提示
    fail_fresh = "//div[@class='el-form-item__error']"

    # 滑动失败，页面刷新重新操作
    def fail_refresh_success_login(self):
        flag = self.isElementExist(self.fail_fresh)
        if flag:
            print("失败刷新页面！")
            self.get_driver().refresh()
            self.slide_verification_login()
        else:
            self.find_element(*self.loc_button).click()
            sleep(1)

    def isElementExist(self, element):
        flag = True
        try:
            self.find_element(By.XPATH, element)
            return flag
        except:
            flag = False
            return flag

    # 全部权限_帐号密码输入
    def login(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['account'], d['password'])
            self.implicitly_wait_time()
            self.wait_time()

    # 市场部权限登录
    def login_marketing_account(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['marketing_account'], d['password'])
            self.implicitly_wait_time()
            self.wait_time()

    def slide_verification_marketing_login(self):
        self.login_marketing_account()
        target = 'target.jpg'
        template = 'template.png'
        self.get_pic()
        distance = self.match(target, template)
        tracks = self.get_tracks((distance + 6.5) * (self.zoom))  # 对位移的缩放计算
        self.crack_slider(tracks)
        sleep(1)
        self.fail_refresh_success_marketing_login()

    def fail_refresh_success_marketing_login(self):
        flag = self.isElementExist(self.fail_fresh)
        if flag:
            print("失败刷新页面！")
            self.get_driver().refresh()
            self.slide_verification_marketing_login()
        else:
            self.find_element(*self.loc_button).click()
            sleep(1)

    # 综合科初审权限登录
    def login_general_audit(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['general_audit'], d['password'])
            self.implicitly_wait_time()
            self.wait_time()

    def slide_verification_general_login(self):
        self.login_general_audit()
        target = 'target.jpg'
        template = 'template.png'
        self.get_pic()
        distance = self.match(target, template)
        tracks = self.get_tracks((distance + 6.5) * (self.zoom))  # 对位移的缩放计算
        self.crack_slider(tracks)
        sleep(1)
        self.fail_refresh_success_general_login()

    def fail_refresh_success_general_login(self):
        flag = self.isElementExist(self.fail_fresh)
        if flag:
            print("失败刷新页面！")
            self.get_driver().refresh()
            self.slide_verification_general_login()
        else:
            self.find_element(*self.loc_button).click()
            sleep(1)

    # 综合科复审权限登录
    def login_general_review_login(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['general_review'], d['password'])
            self.implicitly_wait_time()
            self.wait_time()

    def slide_verification_general_review_login(self):
        self.login_general_review_login()
        target = 'target.jpg'
        template = 'template.png'
        self.get_pic()
        distance = self.match(target, template)
        tracks = self.get_tracks((distance + 6.5) * (self.zoom))  # 对位移的缩放计算
        self.crack_slider(tracks)
        sleep(1)
        self.fail_refresh_success_general_general_review_login()

    def fail_refresh_success_general_general_review_login(self):
        flag = self.isElementExist(self.fail_fresh)
        if flag:
            print("失败刷新页面！")
            self.get_driver().refresh()
            self.slide_verification_general_review_login()
        else:
            self.find_element(*self.loc_button).click()
            sleep(1)

    # 总监确认权限登录
    def login_director_to_confirm_login(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['director_to_confirm'], d['password'])
            self.implicitly_wait_time()
            self.wait_time()

    def slide_verification_director_to_confirm_login(self):
        self.login_director_to_confirm_login()
        target = 'target.jpg'
        template = 'template.png'
        self.get_pic()
        distance = self.match(target, template)
        tracks = self.get_tracks((distance + 6.5) * (self.zoom))  # 对位移的缩放计算
        self.crack_slider(tracks)
        sleep(1)
        self.fail_refresh_success_general_director_to_login()

    def fail_refresh_success_general_director_to_login(self):
        flag = self.isElementExist(self.fail_fresh)
        if flag:
            print("失败刷新页面！")
            self.get_driver().refresh()
            self.slide_verification_director_to_confirm_login()
        else:
            self.find_element(*self.loc_button).click()
            sleep(1)

    # 新增水工单
    loc_increat = (By.XPATH, "//div[@class='phone-box']//button[.='新增']")
    # loc_service_code = (By.XPATH, "//div[@class='el-dialog__body']/form/div[2]/div/div/input")  # 服务码
    loc_service_time = (By.XPATH, "//div[@class='el-dialog__body']/form/div[2]/div/div/input")  # 预约时间
    loc_data_time = (By.XPATH, "//table[@class='el-date-table']/tbody/tr[6]/td[5]/div/span")  # 选择时间
    loc_Appointments = (By.XPATH, "//input[@placeholder='请填写预约人']")  # 预约人
    loc_Appointments_telephone = (By.XPATH, "//div[@class='el-dialog__body']/form/div[4]/div/div/input")  # 预约人电话
    loc_human_type = (By.XPATH, "//div[@class='el-dialog__body']/form/div[5]/div/div/div[1]/input")  # 预约人类型
    loc_human_type_owner = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[1]")  # 业主
    loc_human_type_plumber = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[2]")  # 水电工
    loc_human_type_section = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[3]")  # 工长
    loc_human_type_PM = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[4]")  # 项目经理
    loc_human_type_decoration_company = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[5]")  # 装修公司
    loc_human_type_dealer = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[6]")  # 经销商
    loc_human_type_organization = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[7]")  # 机构
    loc_human_type_other = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[8]")  # 其他
    loc_Residential_address = (By.CSS_SELECTOR, "span.el-cascader__label")  # 小区地址
    loc_province = (By.XPATH, "//div[5]/ul/li[1]/span")  # 北京市一级
    loc_city = (By.XPATH, "//div[5]/ul[2]/li[1]/span")  # 北京市二级
    loc_district = (By.XPATH, "//div[5]/ul[3]/li[1]/span")  # 东城区三级
    loc_detailed_address = (By.XPATH, "//input[@placeholder='请填写详细地址']")  # 详细地址
    loc_zxhs = (By.XPATH, "//div[@class='el-dialog__body']/form/div[10]/div/div[1]/input")  # 几幢
    loc_unit = (By.XPATH, "//div[@class='el-dialog__body']/form/div[10]/div/div[2]/input")  # 几单元
    loc_room = (By.XPATH, "//div[@class='el-dialog__body']/form/div[10]/div/div[3]/input")  # 几室
    loc_choose_org = (By.XPATH, "//div[@class='el-dialog__body']/form/div[11]/div/div/div/input")  # 选择机构

    loc_choose_org_NO1 = (By.XPATH, "//div[6]/div[1]/div[1]/ul/li/span")  # 选择第一个机构
    loc_note = (By.XPATH, "textarea.el-textarea__inner")  # 备注
    loc_submit_button = (By.XPATH, "//div[@class='phone-box']//button[.='提 交']")  # 确定提交

    water_service_code = random_match()  # 随机服务码

    water_real_code = water_service_code

    # 新增订单
    def increat_order(self):
        self.wait_time(5)
        self.find_element(*self.loc_increat).click()
        # self.wait_time()
        # self.find_element(*self.loc_service_code).send_keys(self.water_real_code)
        self.wait_time()
        self.find_element(*self.loc_service_time).click()
        self.wait_time()
        self.find_element(*self.loc_data_time).click()
        self.find_element(*self.loc_Appointments).send_keys(random_name())
        self.wait_time()
        self.find_element(*self.loc_Appointments_telephone).send_keys('15067126937')
        self.wait_time()
        self.find_element(*self.loc_human_type).click()
        self.find_element(*self.loc_human_type_owner).click()
        self.wait_time()
        self.find_element(*self.loc_Residential_address).click()
        self.wait_time()
        # target = self.find_element(*self.loc_province)
        # self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.wait_time()
        self.find_element(*self.loc_province).click()
        self.wait_time()
        self.find_element(*self.loc_city).click()
        self.wait_time()
        self.find_element(*self.loc_district).click()
        self.wait_time()
        self.find_element(*self.loc_detailed_address).send_keys(random_address())
        self.find_element(*self.loc_zxhs).send_keys('3')
        self.find_element(*self.loc_unit).send_keys('4')
        self.find_element(*self.loc_room).send_keys('5')
        self.find_element(*self.loc_choose_org).click()
        self.find_element(*self.loc_choose_org_NO1).click()
        self.wait_time()
        self.find_element(*self.loc_submit_button).click()
        self.wait_time(6)

    system = (By.XPATH, "//div[@class='left-box']//span[.='系统设置']")  # 系统设置
    organ_manage = (By.XPATH, "//div[@class='left-box']/ul/div[6]/li/ul/li[1]")  # 机构管理
    organ_increase = (By.XPATH, "//div[@class='mechanism-box']//button[.='新增']")  # 机构新增
    organ_name = (By.XPATH, "//input[@placeholder='请填写机构名称']")  # 机构名称
    organ_code = (By.XPATH, "//input[@placeholder='请填写机构代码']")  # 机构代码
    organ_telephone = (By.XPATH, "//input[@placeholder='请填写机构电话']")  # 机构电话
    organ_Headquarters_management = (By.XPATH, "//form[@class='el-form']//button[.='总部管理']")  # 总部管理
    organ_The_new_headquarters = (By.XPATH, "//div[@class='mechan-detail_box']//button[.='新增']")  # 总部新增
    organ_headquarters_name = (By.XPATH, "//ul[@class='head-ul_box']/li[1]/div/span[1]/div/input")  # 总部名称
    organ_headquarters_true = (By.XPATH, "//*[@id='iconOK']/path[1]")  # 总部确认
    organ_belong_headquarters = (By.XPATH, "//div[@class='el-select']/div[1]/input")  # 所属总部
    organ_headquarters_choose = (By.XPATH, "//div[@class='el-scrollbar']//span[.='北京']")  # 总部机构选择北京
    organ_province_choose = (By.XPATH, "//div[@class='el-tree']//span[.='北京市']")  # 管辖区域选择北京市
    organ_city_choose = (By.XPATH, "//div[@class='el-tree-node__children']//span[.='北京市']")  # 选择北京市下的北京市
    organ_area_choose = (
        By.XPATH, "//div[@class='el-tree']/div[1]/div[2]/div/div[2]/div[1]/div/label/span/span")  # 第一个区域
    organ_submit_true = (By.XPATH, "//div[@class='mechanism-add_box']//button[.='提交']")  # 页面提交
    organ_Bounced_to_confirm = (
        By.XPATH, "//div[@class='el-message-box__btns']//button[normalize-space(.)='确定']")  # 弹框提交
    organ_del = (By.XPATH, "//div[@class='el-table__fixed-body-wrapper']//span[.='删除']")  # 删除
    organ_del_true = (By.XPATH, "//div[@class='el-message-box__btns']//button[normalize-space(.)='确定']")  # 弹框确定删除

    # 删除机构
    def del_organization(self):
        self.wait_time()
        self.find_element(*self.organ_del).click()
        self.wait_time(2)
        self.find_elements(*self.organ_del_true).click()

    # 机构列表
    def test_1(self):
        self.wait_time(5)
        self.find_element(*self.system).click()
        self.wait_time()
        self.find_element(*self.organ_manage).click()
        self.wait_time(5)

    # 新增机构
    def increat_organization(self):
        self.wait_time(5)
        self.find_element(*self.system).click()
        self.wait_time()
        self.find_element(*self.organ_manage).click()
        self.wait_time(5)
        self.find_element(*self.organ_increase).click()
        self.wait_time()
        self.find_element(*self.organ_name).send_keys("北京")
        self.find_element(*self.organ_code).send_keys("Beijing")
        self.find_element(*self.organ_telephone).send_keys(random_phone_number())
        self.wait_time()
        # self.find_element(*self.organ_Headquarters_management).click()
        # self.wait_time()
        # self.find_element(*self.organ_The_new_headquarters).click()
        # self.wait_time(2)
        # self.find_element(*self.organ_headquarters_name).send_keys("北京")
        # self.wait_time(2)
        # self.find_element(*self.organ_headquarters_true).click()
        self.find_element(*self.organ_belong_headquarters).click()
        self.wait_time(2)
        self.find_element(*self.organ_headquarters_choose).click()
        self.wait_time(1)
        self.find_element(*self.organ_province_choose).click()
        self.wait_time()
        self.find_element(*self.organ_city_choose).click()
        self.wait_time()
        self.find_element(*self.organ_area_choose).click()
        self.wait_time(15)
        self.find_element(*self.organ_submit_true).click()
        self.wait_time()
        self.find_element(*self.organ_Bounced_to_confirm).click()
        self.wait_time()

    work_order = (By.XPATH, "//div[@class='left-box']/ul/div[1]/li/ul/li[2]")  # 工单管理
    work_to_be_assigned = (By.XPATH, "//div/div/section/section/section/main/div[3]/div/div[1]/ul/li[2]/a")  # 标签待指派
    work_service_code_elements = (By.XPATH,
                                  "//tr[@class='el-table__row']//div[@class='cell']")  # 工单管理服务码列表
    work_service_code_texts = []
    work_service_code_exist = (By.XPATH, "//div[@class='mt-20']//div[.='" + water_service_code + "']")  # 指定服务码
    work_service_human = (By.XPATH, "//span[@class='el-radio__inner']")  # 选择服务专员
    work_service_submit_button = (By.XPATH, "//div[@class='mt-20']//button[.='确 定']")  # 服务专员选择确定

    # 工单管理，派单，现在没有服务码，可舍弃该方法
    def work_order_designate(self):
        self.wait_time()
        self.find_element(*self.work_order).click()
        self.wait_time()
        self.find_element(*self.work_to_be_assigned).click()
        self.wait_time(2)
        service_code_elements = self.find_elements(*self.work_service_code_elements)
        print(service_code_elements)
        for service_code_element in service_code_elements:
            self.work_service_code_texts.append(service_code_element.text)
        print(self.work_service_code_texts)
        self.wait_time(5)

        # 判断该订单是否存在
        try:
            self.assertIn(self.water_real_code, self.work_service_code_texts,
                          "%s 新增订单服务码成功！" % self.water_real_code)
        except Exception as e:
            print(format(e))

        code_number = self.work_service_code_texts.index(self.water_real_code)
        code_location = int((code_number + 1) / 14) + 1
        # 指派按键位置
        work_order_to_designate = (
            By.XPATH,
            "//div[@class='el-table__fixed-body-wrapper']/table/tbody/tr[" + str(
                code_location) + "]/td[15]/div/div/span[2]")
        self.find_element(*work_order_to_designate).click()
        self.wait_time()
        self.find_element(*self.work_service_human).click()
        # if self.find_element(*self.work_service_code_exist) == self.water_service_code:
        #     self.find_element()

    # 1.补贴申请，流程 (只拥有市场部权限)市场部审核
    subsidy_service_code_texts = []  # 空列表
    subsidy_wealth_management = (By.XPATH, "//div[@class='left-box']//span[.='资金管理']")  # 资金管理
    subsidy_audit = (By.XPATH, "//div[@class='left-box']/div/div[1]/div/ul/div[3]/li/ul/li")  # 补贴审核
    subsidy_service_code_elements = (By.XPATH, "//div[@class='el-table__header-wrapper']//div[@class='cell']")  # 服务卡号列表
    subsidy_agree_button = (By.XPATH, "//div[@class='el-table__fixed-body-wrapper']//span[.='同意']")  # 同意补贴申请(列表第一列同意）
    subsidy_agree_window = (
        By.XPATH, "//div[@class='el-message-box__btns']//button[normalize-space(.)='确定']")  # 列表同意后，窗口同意确认
    subsidy_to_audit = (By.XPATH, "//div[@class='personnel-box']//a[.='已审核']")  # 已审核列表
    subsidy_service_audit_code_elements = (By.XPATH, "//thead[@class='has-gutter']//div[@class='cell']")  # 列表数据
    subsidy_service_audit_codes_elements_texts = []

    # 补贴审核——同意,待审核通过后在已审核列表比对
    def subsidy_operation(self):
        # self.wait_time()
        # self.find_element(*self.subsidy_wealth_management).click()
        # self.wait_time()
        # self.find_element(*self.subsidy_audit).click()
        self.wait_time()
        subsidy_service_codes_elements = self.find_elements(*self.subsidy_service_code_elements)
        for subsidy_service_codes_element in subsidy_service_codes_elements:
            self.subsidy_service_code_texts.append(subsidy_service_codes_element)
        subsidy_code_card = self.subsidy_service_code_texts[5]  # 服务卡号
        print(subsidy_code_card)
        print("已生成服务卡号")
        subsidy_service_number = self.subsidy_service_code_texts.index(subsidy_code_card)
        subsidy_service_code_location = int((subsidy_service_number + 1) / 22) + 1  # 定位列表的行数
        # 列表同意的位置
        if subsidy_service_number <= 22:
            subsidy_service_code_real_location = (By.XPATH,
                                                  "//div[1]/div/section/section/section/div[2]/div[1]/div/main/div[3]/"
                                                  "div/div[4]/div/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[22]/div/div/span[1]")
            self.find_element(*subsidy_service_code_real_location).click()
        else:
            subsidy_service_code_real_location = (By.XPATH,
                                                  "//div[1]/div/section/section/section/div[2]/div[1]/div/main/div[3]/"
                                                  "div/div[4]/div/div/div[1]/div[4]/div[2]/table/tbody/tr[" + str(
                                                      subsidy_service_code_location) + "]/td[22]/div/div/span[1]")
            self.find_element(*subsidy_service_code_real_location).click()

        self.find_element(*self.subsidy_agree_window).click()
        self.wait_time()
        self.find_element(*self.subsidy_to_audit).click()  # 进入已审核列表
        self.wait_time()
        subsidy_service_audit_codes_elements = self.find_elements(*self.subsidy_service_code_elements)
        for subsidy_service_audit_code in subsidy_service_audit_codes_elements:
            self.subsidy_service_audit_codes_elements_texts.append(subsidy_service_audit_code)

        return subsidy_code_card, self.subsidy_service_audit_codes_elements_texts

    service_code, service_code_without = subsidy_operation()

    department_to_audit_codes_element_text = []
    department_to_audit_elements = (By.XPATH, "//div[@class='mt-20']//div[@class='cell']")  # 列表数据

    # 2.综合科初审
    def department_to_audit(self):
        # self.wait_time()
        # self.find_element(*self.subsidy_wealth_management).click()
        # self.wait_time()
        # self.find_element(*self.subsidy_audit).click()
        self.wait_time()
        department_to_audit_codes_elements = self.find_elements(*self.department_to_audit_elements)
        for department_to_audit_element in department_to_audit_codes_elements:
            self.department_to_audit_codes_element_text.append(department_to_audit_element)
        subsidy_service_number = self.subsidy_service_code_texts.index(self.service_code)
        subsidy_service_code_location = int((subsidy_service_number + 1) / 22) + 1  # 定位列表的行数
        # 列表同意的位置
        if subsidy_service_number <= 22:
            subsidy_service_code_real_location = (By.XPATH,
                                                  "//div[1]/div/section/section/section/div[2]/div[1]/div/main/div[3]/"
                                                  "div/div[4]/div/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[22]/div/div/span[1]")
            self.find_element(*subsidy_service_code_real_location).click()
        else:
            subsidy_service_code_real_location = (By.XPATH,
                                                  "//div[1]/div/section/section/section/div[2]/div[1]/div/main/div[3]/"
                                                  "div/div[4]/div/div/div[1]/div[4]/div[2]/table/tbody/tr[" + str(
                                                      subsidy_service_code_location) + "]/td[22]/div/div/span[1]")
            self.find_element(*subsidy_service_code_real_location).click()
