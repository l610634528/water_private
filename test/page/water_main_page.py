"""终端环境"""
# from selenium.webdriver.common.by import By
# import sys
# sys.path.append("..\\common")
# from page import Page
#
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

water_service_code_1 = '7gfOxckv'


class WaterMainPage(Page):
    URL = Config().get('URL')
    excel = DATA_PATH + '/water.xlsx'
    loc_account = (By.XPATH, "//input[@placeholder='请输入手机号码']")
    loc_password = (By.XPATH, "//input[@placeholder='请输入密码']")
    loc_button = (By.XPATH, "//button[@class='el-button submit-info el-button--default']")

    def element(self, account, password):
        """登录功能"""
        self.find_element(*self.loc_account).send_keys(account)
        self.find_element(*self.loc_password).send_keys(password)
        self.find_element(*self.loc_button).click()

    def login(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            self.element(d['account'], d['password'])
            self.implicitly_wait_time()
            self.wait_time()

    # 新增水工单
    loc_increat = (By.XPATH, "//div[@class='phone-box']//button[.='新增']")
    loc_service_code = (By.XPATH, "//div[@class='el-dialog__body']/form/div[2]/div/div/input")  # 服务码
    loc_service_time = (By.XPATH, "//div[@class='el-dialog__body']/form/div[3]/div/div/input")  # 预约时间
    loc_data_time = (By.XPATH, "//table[@class='el-date-table']/tbody/tr[6]/td[7]/div/span")  # 选择时间
    loc_Appointments = (By.XPATH, "//div[@class='el-dialog__body']/form/div[4]/div/div/input")
    loc_Appointments_telephone = (By.XPATH, "//div[@class='el-dialog__body']/form/div[5]/div/div[1]/input")
    loc_human_type = (By.XPATH, "//div[@class='el-dialog__body']/form/div[6]/div/div/div[1]/input")
    loc_human_type_owner = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[1]")  # 业主
    loc_human_type_plumber = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[2]")  # 水电工
    loc_human_type_section = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[3]")  # 工长
    loc_human_type_PM = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[4]")  # 项目经理
    loc_human_type_decoration_company = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[5]")  # 装修公司
    loc_human_type_dealer = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[6]")  # 经销商
    loc_human_type_organization = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[7]")  # 机构
    loc_human_type_other = (By.XPATH, "//div[4]/div[1]/div[1]/ul/li[8]")  # 其他
    loc_Residential_address = (By.CSS_SELECTOR, "span.el-cascader__label")  # 小区地址
    loc_province = (By.XPATH, "//div[5]/ul/li[1]/span")  # 北京市
    loc_city = (By.XPATH, "//div[5]/ul[2]/li[1]/span")  # 北京市
    loc_district = (By.XPATH, "//div[5]/ul[3]/li[1]")  # 东城区
    loc_detailed_address = (By.XPATH, "//div[@class='el-dialog__body']/form/div[10]/div/div/input")  # 详细地址
    loc_choose_org = (By.XPATH, "//div[@class='el-dialog__body']/form/div[11]/div/div/div/input")  # 选择机构
    loc_choose_org_NO1 = (By.XPATH, "//div[6]/div[1]/div[1]/ul/li")  # 选择第一个机构
    loc_note = (By.XPATH, "textarea.el-textarea__inner")  # 备注
    loc_submit_button = (By.XPATH, "//div[@class='phone-box']//button[.='提 交']")  # 确定提交

    water_service_code = random_match()  # 随机服务码
    water_real_code = water_service_code

    # 新增订单
    def increat_order(self):
        self.wait_time(5)
        self.find_element(*self.loc_increat).click()
        self.wait_time()
        self.find_element(*self.loc_service_code).send_keys(self.water_real_code)
        self.wait_time()
        self.find_element(*self.loc_service_time).click()
        self.wait_time()
        self.find_element(*self.loc_data_time).click()
        self.find_element(*self.loc_Appointments).send_keys(random_name())
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
        self.wait_time(20)
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
    work_service_submit_button = (By.XPATH, "//div[@class='mt-20']//button[.='确 定']") # 服务专员选择确定

    # 工单管理，指派
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
            self.assertIn(water_service_code_1, self.work_service_code_texts,
                          "%s 新增订单服务码失败！" % self.water_real_code)
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
