import os
import random
import re
import screeninfo
import shutil
import time
import platform
import pyautogui
import pytest
import pyperclip

from .logger import Logger
from .parse import chrome_driver, firefox_driver, project_name, web_type
from .parse import usr_1_name, usr_1, pwd_1
from .parse import usr_2_name, usr_2, pwd_2
from .parse import usr_3_name, usr_3, pwd_3
from .report import Report
from .cv import ImgDeal
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, ElementNotInteractableException


class ChromeAuto(object):
    def __init__(self):
        driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tools', chrome_driver)
        self.download_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads')
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)
        option = webdriver.ChromeOptions()
        # option.add_argument('--headless')  # 不打开可视化界面
        option.add_argument('disable-infobars')  # 取消浏览器提示信息
        option.add_argument('--no-sandbox')  # 在root权限下打开浏览器
        option.add_argument('--ignore-certificate-errors')
        width = screeninfo.get_monitors()[0].width
        height = screeninfo.get_monitors()[0].height
        option.add_argument(f'--window-size={width},{height}')  # 专门应对无头浏览器中不能最大化屏幕的方案
        s = Service(driver_path)
        # 修改下载路径，方便检测文件下载
        prefs = {"download.default_directory": self.download_path}
        option.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(service=s, options=option)
        # self.driver.maximize_window()  # 浏览器最大化显示，可视化界面有效，隐藏显示无效

    def __str__(self):
        return self.driver


class FireFoxAuto(object):
    def __init__(self):
        driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tools', firefox_driver)
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')  # 不打开可视化界面
        option.add_argument('disable-infobars')  # 取消浏览器提示信息
        option.add_argument('--no-sandbox')  # 在root权限下打开浏览器
        option.add_argument('--ignore-certificate-errors')
        width = screeninfo.get_monitors()[0].width
        height = screeninfo.get_monitors()[0].height
        option.add_argument(f'--window-size={width},{height}')  # 专门应对无头浏览器中不能最大化屏幕的方案
        s = Service(driver_path)
        self.driver = webdriver.Firefox(service=s, options=option)
        # self.driver.maximize_window()  # 浏览器最大化显示，可视化界面有效，隐藏显示无效

    def __str__(self):
        return self.driver


class WebAuto(object):
    def __init__(self, driver):
        if web_type == 'None':
            self.url = 'https://yueliu.cn/v20/#/'
        else:
            self.url = f'https://{web_type}.yueliu.cloud/v20/#/'
        self.driver = driver
        self.driver_status = True
        self.img_path = os.path.join(os.path.join(os.path.dirname(__file__), 'file'))
        self.download_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Downloads')

    #####################################
    #--------------通用---------------###
    #####################################
    def click_space(self):
        Logger.info('点击空格')
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        time.sleep(3)

    def click_by_img(self, img='', info=''):
        img_pos = ImgDeal.find_by_img(os.path.join(self.img_path, f'{img}.png'), info)
        if img_pos:
            Logger.info(f'移动到坐标--{img_pos[0]}, {img_pos[1]}')
            pyautogui.moveTo(img_pos[0], img_pos[1])
            Logger.info('点击')
            pyautogui.click()
            time.sleep(2)
            return True
        return False

    def click_by_position(self, x, y, left_click=True):
        if left_click:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.driver).move_by_offset(x, y).context_click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()

    def screen(self):
        current_time = str(time.strftime('%y_%m_%d_%H_%M_%S', time.localtime()))
        screen_path = os.path.join(Report.report_path, 'screen')
        if not os.path.exists(screen_path):
            os.makedirs(screen_path)
        file = os.path.join(screen_path, f'{current_time}.png')
        self.driver.get_screenshot_as_file(file)
        return file

    def open_page(self, url=None):
        Logger.info(f'访问url：{url}')
        self.driver.get(url)
        time.sleep(3)

    def quit(self):
        # 关闭Chromedriver
        Logger.info('关闭浏览器！')
        self.driver.quit()
        self.driver_status = False

    def check_alert(self):
        try:
            alert = self.driver.switch_to.alert
            Logger.info(f'检测到弹窗--{alert}')
            return alert
        except NoAlertPresentException as e:
            return False

    def _find_by_condition(self, condition='class', obj=None):
        if condition == 'id':
            ele = self.driver.find_element(By.ID, obj)
        elif condition == 'class':
            ele = self.driver.find_element(By.CLASS_NAME, obj)
        elif condition == 'xpath':
            ele = self.driver.find_element(By.XPATH, obj)
        elif condition == 'name':
            ele = self.driver.find_element(By.NAME, obj)
        elif condition == 'link_text':
            ele = self.driver.find_element(By.LINK_TEXT, obj)
        elif condition == 'partial_link_text':
            ele = self.driver.find_element(By.PARTIAL_LINK_TEXT, obj)
        elif condition == 'tag_name':
            ele = self.driver.find_element(By.TAG_NAME, obj)
        elif condition == 'css':
            ele = self.driver.find_element(By.CSS_SELECTOR, obj)
        else:
            raise NameError("无效参数，请输入正确的参数！")
        return ele

    def find_by_condition(self, condition='class', obj=None):
        try:
            return self._find_by_condition(condition, obj)
        except NoSuchElementException as e:
            Logger.error(f'未找到该元素：{condition}--{obj}')
            assert 0
        except ElementNotInteractableException as e:
            Logger.error(f'该元素被隐藏，或不止一个：{condition}--{obj}')
            assert 0

    def _finds_by_condition(self, condition='class', obj=None):
        if condition == 'id':
            ele = self.driver.find_elements(By.ID, obj)
        elif condition == 'class':
            ele = self.driver.find_elements(By.CLASS_NAME, obj)
        elif condition == 'xpath':
            ele = self.driver.find_elements(By.XPATH, obj)
        elif condition == 'name':
            ele = self.driver.find_elements(By.NAME, obj)
        elif condition == 'link_text':
            ele = self.driver.find_elements(By.LINK_TEXT, obj)
        elif condition == 'partial_link_text':
            ele = self.driver.find_elements(By.PARTIAL_LINK_TEXT, obj)
        elif condition == 'tag_name':
            ele = self.driver.find_elements(By.TAG_NAME, obj)
        elif condition == 'css':
            ele = self.driver.find_elements(By.CSS_SELECTOR, obj)
        else:
            raise NameError("无效参数，请输入正确的参数！")
        return ele

    def finds_by_condition(self, condition='class', obj=None):
        try:
            return self._finds_by_condition(condition, obj)
        except NoSuchElementException as e:
            Logger.error(f'未找到该元素：{condition}--{obj}')
            assert 0

    def click_by_condition(self, condition='class', obj=None, info=None, timeout=2):
        # 根据条件点击
        if condition == 'link_text':
            Logger.info(f'点击--{obj}')
        elif info:
            Logger.info(f'点击--{info}')
        self.find_by_condition(condition, obj).click()
        time.sleep(timeout)

    def click_by_condition_index(self, condition='class', obj=None, index=-1, info=None, timeout=2):
        # 根据条件点击
        if condition == 'link_text':
            Logger.info(f'点击--{obj}')
        elif info:
            Logger.info(f'点击--{info}')
        self.finds_by_condition(condition, obj)[index].click()
        time.sleep(timeout)

    def wait_until_xpath(self, xpath, timeout=10, wait=1):
        # 超时时间为10秒，每1秒检查1次，直到元素出现
        if WebDriverWait(self.driver, timeout, wait).until(EC.visibility_of_element_located((By.XPATH, xpath))):
            return True
        else:
            Logger.error('未检测到该元素！')
            return False

    def wait_until_text(self, ele_type='p', text='', timeout=10, wait=1):
        # 超时时间为10秒，每1秒检查1次，直到元素出现
        xpath = f'//{ele_type}[contains(text(), "{text}")]'
        if WebDriverWait(self.driver, timeout, wait).until(EC.visibility_of_element_located((By.XPATH, xpath))):
            return True
        else:
            Logger.error('未检测到该文本！')
            return False

    def refresh(self, timeout=5):
        self.driver.refresh()
        time.sleep(timeout)

    def check_button(self, text=''):
        try:
            ele = self.find_by_condition('xpath', f'//button[contains(text(), "{text}")]')
            return ele
        except NoSuchElementException as e:
            return False

    def click_by_js(self, button='', timeout=2):
        self.driver.execute_script("arguments[0].click()", button)
        time.sleep(timeout)

    @staticmethod
    def get_text(ele):
        return ele.get_attribute('innerText').strip()

    def click_by_text(self, ele_type='', text='', fuzzy=True):
        if ele_type and text:
            if fuzzy:
                self.click_by_condition('xpath', f'//{ele_type}[contains(text(), "{text}")]')
            else:
                self.click_by_condition('xpath', f'//{ele_type}[text()="{text}"]', text)
            time.sleep(1)
        else:
            Logger.error('请输入元素类型及文本')
            assert 0
#####################################
#--------------功能---------------###
#####################################
    def login_by_password(self, usr=usr_1, pwd=pwd_1):
        url = self.url + 'login'
        self.open_page(url)
        self.click_by_condition('xpath', '//li[contains(text(), "密码登录")]', '密码登录')
        Logger.info('输入账号')
        self.finds_by_condition('class', 'el-input__inner')[0].clear()
        self.finds_by_condition('class', 'el-input__inner')[0].send_keys(usr)
        time.sleep(1)
        Logger.info('输入密码')
        self.finds_by_condition('class', 'el-input__inner')[1].clear()
        self.finds_by_condition('class', 'el-input__inner')[1].send_keys(pwd)
        time.sleep(1)
        self.click_by_condition('class', 'login-btn-container', '登录')
        time.sleep(3)
        if self.find_by_condition('class', 'avatar-wrapper'):
            Logger.info('登录成功！')
        else:
            Logger.error('登录失败！')
            pytest.exit('登录失败，测试停止！')
        time.sleep(5)
        self.close_update_info()
        self.close_message()

    @staticmethod
    def create_user():
        user_start_list = ['130', '139', '150', '186']
        user_start = random.sample(user_start_list, 1)[0]
        user_end = str(random.randint(10000000, 99999999))
        user = f'{user_start}{user_end}'
        Logger.info(f'随机账号为：{user}')
        return user

    def login_by_code(self, usr=usr_1, code='888888'):
        url = self.url + 'login'
        self.open_page(url)
        Logger.info('输入账号')
        self.finds_by_condition('class', 'el-input__inner')[0].clear()
        self.finds_by_condition('class', 'el-input__inner')[0].send_keys(usr)
        time.sleep(1)
        Logger.info('输入验证码')
        self.find_by_condition('xpath', '//label[contains(text(), "发送验证码")]').click()
        self.finds_by_condition('class', 'el-input__inner')[1].clear()
        self.finds_by_condition('class', 'el-input__inner')[1].send_keys(code)
        time.sleep(1)
        self.click_by_condition('class', 'login-btn-container', '登录')
        time.sleep(10)
        start_button = self.check_button('开启阅流')
        if start_button:
            time.sleep(5)
            choose_button = self.check_button('其他')
            choose_button.click()
            time.sleep(1)
            start_button.click()
            time.sleep(3)
            self.click_by_condition('class', 'skip')
        if self.find_by_condition('class', 'avatar-wrapper'):
            Logger.info('登录成功！')
        else:
            Logger.error('登录失败！')
            pytest.exit('登录失败，测试停止！')
        time.sleep(5)
        self.close_update_info()
        self.close_message()

    def login_out(self):
        self.click_by_condition_index('class', 'avatar-wrapper', 1, '用户头像')
        self.click_by_condition('xpath', '//div[contains(text(), "退出登录")]', '退出登录')
        self.click_by_condition('xpath', '//div[text()="退出 "]', '退出', 3)

    def close_update_info(self):
        if self.check_condition('class', 'footer'):
            Logger.info('点击关闭更新提示')
            self.finds_by_condition('class', 'footer')[0].click()
            time.sleep(3)

    def close_message(self):
        while self.check_condition('class', 'close-box'):
            Logger.info('点击关闭消息提示')
            self.finds_by_condition('class', 'close-box')[0].click()
            time.sleep(3)

    def open_project_menu(self):
        try:
            setting_ele = self.finds_by_condition('xpath', f'//span[contains(text(), "{project_name}")]/../div[2]')
            if len(setting_ele) > 1:
                Logger.info('检测到相关项目不止一个，默认使用第一个测试')
            setting_ele[0].click()
            time.sleep(1)
        except:
            Logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def open_project_settings(self, setting='项目设置', timeout=2):
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{setting}")]', -1, f'{setting}', timeout)

    def close_project_setting(self):
        self.click_by_condition('xpath', '//span[contains(text(), "项目设置")]/../i', '关闭项目设置')

    def touch_to_project(self):
        project_ele_list = self.finds_by_condition('xpath',
                                                   '//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[@class="cardList-clone-wrapper "]')
        for project_ele in project_ele_list:
            if project_ele.get_attribute('innerText') == project_name:
                Logger.info('检测到测试项目，点击打开')
            project_ele.click()
            time.sleep(1)
            break
        else:
            Logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def set_permission(self):
        self.click_by_condition('xpath', '//p[contains(text(), "身份权限设置")]/../../div[2]/div', '打开权限设置')

    def set_fangluping(self, open=True):
        # 设置防录屏
        fangluping_ele = self.find_by_condition('xpath', '//p[contains(text(), "防录屏")]/../../div[2]/div')
        if open:
            if fangluping_ele.get_attribute('aria-checked'):
                Logger.info('防录屏开关为打开状态')
            else:
                Logger.info('防录屏开关未打开，点击打开')
                fangluping_ele.click()
                self.wait_until_text(text='保存项目成功')
        else:
            if fangluping_ele.get_attribute('aria-checked'):
                Logger.info('防录屏开关为打开状态，点击关闭')
                fangluping_ele.click()
                self.wait_until_text(text='保存项目成功')
            else:
                Logger.info('防录屏开关为未打开状态')
        self.close_project_setting()

    def check_project_has_file(self):
        if self.driver.find_element('class', 'file-list'):
            Logger.info('检测到项目内存在文件')
        else:
            Logger.info('检测到项目内不存在文件')

    def choose_file_to_upload(self, dir='', file='', all=False):
        # 请选择test_file目录下的测试文件
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_file')
        file = os.path.join(file_path, dir, file)
        Logger.info(f'上传文件为：{file}')
        pyperclip.copy(file)  # 复制文件路径
        platform_str = platform.system().lower()  # 获取操作系统
        Logger.info(f'操作系统为：{platform_str}')
        if platform_str in ['mac', 'darwin']:
            # 打开文件搜索框
            Logger.info('打开搜索框')
            pyautogui.keyDown('shift')
            pyautogui.keyDown('command')
            pyautogui.keyDown('g')
            time.sleep(1)
            pyautogui.keyUp('g')
            pyautogui.keyUp('command')
            pyautogui.keyUp('shift')
            # pyautogui.hotkey('shift', 'command', 'g')  # 打开mac的搜索框，可以直接输入文件全路径定位到具体文件
            time.sleep(2)
            # 粘贴文件路径
            Logger.info('粘贴文件路径')
            pyautogui.hotkey('command', 'v')
            time.sleep(2)
            # 回车确定
            pyautogui.press('Return')
            time.sleep(1)  # 必须停留一下，从粘贴到连续键入两个回车键有问题
            if all:
                Logger.info('全选')
                pyautogui.hotkey('command', 'a')
                time.sleep(1)
            pyautogui.press('Return')
        elif 'windows' in platform_str:
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('enter')
        time.sleep(3)

    def open_upload_page(self):
        upload_ele = self.find_by_condition('class', 'uploadList')
        if upload_ele.get_attribute('aria-hidden') == 'true':
            Logger.info('上传进度弹窗为隐藏状态')
            self.click_by_condition('class', 'iconchuanshu_chuanshu', '打开传输窗口')
        else:
            Logger.info('上传进度弹窗为显示状态')

    def close_upload_page(self):
        upload_ele = self.find_by_condition('class', 'uploadList')
        if upload_ele.get_attribute('aria-hidden') == 'true':
            Logger.info('上传进度弹窗为隐藏状态')
        else:
            Logger.info('上传进度弹窗为显示状态，点击关闭')
            button_ele = self.find_by_condition('class', 'iconchuanshu_chuanshu')
            self.driver.execute_script("arguments[0].click();", button_ele)
            time.sleep(3)
            # self.click_by_condition('class', 'iconchuanshu_chuanshu', '关闭传输窗口')

    def check_condition(self, condition, obj):
        try:
            e = self.finds_by_condition(condition, obj)
            if len(e) == 0:
                return False
            return True
        except NoSuchElementException as e:
            return False

    def is_file_upload(self):
        if self.check_condition('xpath', '//span[contains(text(), "没有正在上传的文件")]'):
            Logger.info('没有正在上传的文件')
            self.close_upload_page()
            return False
        else:
            return True

    def clear_upload_record(self):
        while self.is_file_upload():
            self.click_by_condition('class', 'el-dropdown', '更多设置')
            self.click_by_condition('class', 'el-dropdown-menu__item', '清空已完成记录')
        else:
            Logger.info('清除成功')

    def wait_upload(self):
        self.open_upload_page()
        if not self.is_file_upload():
            Logger.info('没有正在上传的文件')
            self.close_upload_page()
            return False
        success = False
        start_time = time.time()
        # 设置文件上传最多三十分钟
        while not success:
            if time.time() - start_time < 1800:
                status_ele = self.find_by_condition('class', 'total-file-info')
                status = status_ele.get_attribute('innerText').strip()
                if '上传成功' in status:
                    Logger.info('文件上传完成！')
                    time.sleep(5)
                    self.clear_upload_record()
                    self.close_upload_page()
                    success = True
                else:
                    Logger.info(status)
                    time.sleep(5)
            else:
                Logger.error('文件上传超时！')
                self.close_upload_page()
                assert 0

    def upload_file(self, dir='', file='', all=False):
        for i in range(5):
            self.touch_to_project()
            self.click_by_condition('xpath', '//button[contains(text(), "上传/新建")]', '上传/新建')
            self.click_by_condition('class', 'el-upload-dragger', '上传文件')
            self.choose_file_to_upload(dir, file, all)
            self.open_upload_page()
            if self.is_file_upload():
                break
            Logger.info('文件未正确选取，重试！')

    def upload_dir(self, dir=''):
        for i in range(5):
            self.touch_to_project()
            self.click_by_condition('xpath', '//button[contains(text(), "上传/新建")]', '上传/新建')
            self.click_by_condition('xpath', '//div[contains(text(), "上传")]/../div[2]//div[contains(text(), "文件夹")]', '上传文件夹')
            self.choose_file_to_upload(dir)
            time.sleep(3)
            upload_pos = ImgDeal.find_upload()
            if upload_pos:
                Logger.info(f'移动到坐标--{upload_pos[0]}, {upload_pos[1]}')
                pyautogui.moveTo(upload_pos[0], upload_pos[1])
                Logger.info('点击')
                pyautogui.click()
                time.sleep(2)
            self.open_upload_page()
            if self.is_file_upload():
                break
            Logger.info('文件未正确选取，重试！')

    def delete_all_files(self):
        self.touch_to_project()
        while self.check_condition('xpath', '//div[@class="project-title"]/span[contains(text(), "文件")]'):
            Logger.info('检测到项目内存在文件/文件夹')
            self.click_by_condition('xpath', '//*[@id="project-file__content"]//div[@class="el-tooltip more-icon item"]', '文件设置')
            Logger.info('点击--删除')
            self.finds_by_condition('xpath', '//div[contains(text(), "删除")]')[-1].click()
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            Logger.info('删除成功！')
            self.refresh()

    def delete_file(self, file_name=""):
        if not file_name:
            Logger.info('未传入文件，默认删除项目内所有文件')
            self.delete_all_files()
            return True
        self.touch_to_project()
        while self.check_condition('xpath', f'//div[@class="file-subInfo"]//span[contains(text(), "{file_name}")]'):
            self.click_by_condition('xpath', f'//div[@class="file-subInfo"]//span[contains(text(), "{file_name}")]/../../../../div[@class="el-tooltip more-icon item"]', '更多设置')
            Logger.info('点击--删除')
            self.finds_by_condition('xpath', '//div[contains(text(), "删除")]')[-1].click()
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            Logger.info('删除成功！')
            self.refresh()
        else:
            Logger.info('未检测到该文件！')

    def delete_dir(self, dir_name=""):
        if not dir_name:
            Logger.info('未传入文件夹名，默认删除项目内所有文件')
            self.delete_all_files()
            return True
        self.touch_to_project()
        while self.check_condition('xpath', f'//div[@class="file-subInfo"]//span[contains(text(), {dir_name})]'):
            self.click_by_condition('xpath', '//div[@class="file-subInfo"]//span[contains(text(), "video")]/../../../../div[@class="el-tooltip more-icon item"]', '更多设置')
            Logger.info('点击--删除')
            self.finds_by_condition('xpath', '//div[contains(text(), "删除")]')[-1].click()
            time.sleep(3)
            self.click_by_condition('xpath', '//*[@class="alert"]//div[text()="删除 "]', '删除', 1)
            self.wait_until_xpath('//p[contains(text(), "删除成功")]')
            Logger.info('删除成功！')
            self.refresh()
        else:
            Logger.info('未检测到该文件！')

    def check_video_in_project(self):
        video_type_list = ['avi', 'wmv', 'mpg', 'mpeg', 'mov', 'rm', 'ram', 'swf', 'flv', 'mp4']
        project_file_list = self.finds_by_condition('xpath', '//div[@class="subInfo-title"]/span')
        for project_file in project_file_list:
            file_name = project_file.get_attribute('innerText')
            if '.' in file_name:
                file_type = file_name.split('.')[-1]
                if file_type in video_type_list:
                    Logger.info(f'检测到存在视频类文件--{file_name}')
                    break
        else:
            Logger.info('未检测到视频文件，自动上传')
            self.upload_file('video', 'video.mov')
            self.wait_upload()

    def check_fangluping(self, open=True):
        self.check_video_in_project()
        if open:
            if self.check_condition('class', 'mark-bg'):
                Logger.info('检测到防录屏标志')
                return True
            else:
                Logger.error('未检测到防录屏标志')
                assert 0
        else:
            if self.check_condition('class', 'mark-bg'):
                Logger.error('检测到防录屏标志')
                assert 0
            else:
                Logger.info('未检测到防录屏标志')
                return True

    def create_project_quickly(self, p_name=project_name):
        self.click_by_condition('class', 'iconjiahao_jiahao', '左上角加号图标', 3)
        Logger.info('输入项目名称')
        self.find_by_condition('class', 'el-input__inner').send_keys(p_name)
        # 点击完成创建
        self.click_by_condition('xpath', '//span[contains(text(), "完成创建")]', '完成创建', 1)
        # 等待检测到创建项目成功提示
        if self.wait_until_xpath('//p[contains(text(), "创建项目成功")]'):
            Logger.info('检测到提示--创建项目成功')
            time.sleep(3)
        else:
            Logger.error('未检测到项目创建成功提示！')
            assert 0

    def create_project(self):
        flag_color_dict = {1: ['无色', 'None'],
                           2: ['蓝色', 'rgb(52, 109, 254)'],
                           3: ['粉色', 'rgb(255, 114, 116)'],
                           4: ['黄色', 'rgb(252, 197, 16)'],
                           5: ['紫色', 'rgb(104, 87, 255)'],
                           6: ['绿色', 'rgb(2, 196, 169)'],
                           7: ['橙色', 'rgb(241, 143, 96)']
                            }
        # 随机选择标记颜色
        choose_color_num = random.randint(1, 7)
        color = flag_color_dict.get(choose_color_num)[0]
        self.click_by_condition('class', 'iconjiahao_jiahao', '左上角加号图标')
        Logger.info('输入项目名称')
        self.find_by_condition('class', 'el-input__inner').send_keys(project_name)
        Logger.info(f'选择标记颜色--{color}')
        if choose_color_num == 1:
            self.find_by_condition('xpath', '//*[@class="color-marker"]/div[@class="clear-icon-box"]').click()
        else:
            self.find_by_condition('xpath', f'//*[@class="color-marker-wrapper"]/div[@class="color-marker"]/div[@class="color-marker-item-wrapper"][{choose_color_num-1}]/i').click()
        # 点击完成创建
        self.click_by_condition('xpath', '//span[contains(text(), "完成创建")]', '完成创建', 1)
        # 等待检测到创建项目成功提示
        if self.wait_until_xpath('//p[contains(text(), "创建项目成功")]'):
            Logger.info('检测到提示--创建项目成功')
            time.sleep(3)
        else:
            Logger.error('未检测到项目创建成功提示！')
            assert 0
        # 创建成功后检测标记颜色是否正确
        color_ele = self.find_by_condition('xpath', '//*[@class="cardList"]/div[1]/div[1]/div[1]/i')
        color_style = color_ele.get_attribute('style')
        real_color = ''
        if color_style:
            for key, val in flag_color_dict.items():
                if val[1] in color_style:
                    real_color = val[0]
                    break
        else:
            if choose_color_num == 1:
                real_color = '无色'
        Logger.info(f'实际显示颜色为--{real_color}')
        if real_color == color:
            Logger.info('标记颜色验证通过！')
        else:
            Logger.error('标记颜色验证不通过！')

    def get_my_project_list(self):
        project_ele_list = self.finds_by_condition('xpath', '//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[@class="cardList-clone-wrapper "]')
        project_list = [e.get_attribute('innerText') for e in project_ele_list]
        Logger.info(f'项目列表为：{project_list}')
        return project_list

    def delete_project(self, project=project_name):
        Logger.info('检测是否存在创建的测试项目')
        project_list = self.get_my_project_list()
        while project in project_list:
            Logger.info('检测到创建测试项目')
            project_ele_list = self.finds_by_condition('xpath', '//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[@class="cardList-clone-wrapper "]')
            project_count = len(project_ele_list)
            Logger.info(f'项目总数为：{project_count}')
            index = 1
            for ele in project_ele_list:
                p_name = ele.get_attribute('innerText')
                if p_name == project:
                    Logger.info('检测到创建测试项目')
                    self.click_by_condition('xpath', f'//span[contains(text(), "我的项目")]/../..//ul[@class="cardList"]/div[1]/div[{index}]/div[1]/div[2]', '更多设置')
                    Logger.info('点击--删除项目')
                    self.finds_by_condition('xpath', '//div[contains(text(), "删除项目")]')[-1].click()
                    self.click_by_condition('xpath', '//*[@class="space-round"]/div[2]/div[contains(text(), "删除")]', '删除', 1)
                    project_count -= 1
                    cur_project_count = len(self.get_my_project_list())
                    Logger.info(f'当前项目数为：{cur_project_count}')
                    if cur_project_count == project_count:
                        Logger.info('删除成功')
                        self.refresh(3)
                        break
                    else:
                        Logger.error('删除失败')
                        assert 0
                index += 1
            project_list = self.get_my_project_list()

    def close_invite_view(self):
        self.click_by_condition_index('xpath', '//div[@class="dialog-header-content"]/i', -1, '关闭邀请界面')

    def invite_member(self, usr_name=usr_2_name, super=True, company=True):
        # super --True 管理员 False 成员
        # company --True 企业内邀请 False 链接邀请
        self.click_by_condition_index('xpath', '//div[@class="identity-content-select"]', -1, '选择身份')
        identity = '管理员' if super else '成员'
        self.click_by_condition_index('xpath', f'//div[@class="select-item"]/p[contains(text(), "{identity}")]', -1, f'{identity}')
        time.sleep(5)
        invite_type = "从企业内" if company else "链接扫码"
        self.click_by_condition_index('xpath', f'//p[contains(text(), "{invite_type}")]', -1, invite_type)
        if company:
            self.click_by_condition_index('class', 'search-header-box', -1, '搜索')
            self.finds_by_condition('class', 'search-input')[-1].send_keys(usr_name)
            time.sleep(2)
            result_ele = self.check_condition('xpath', '//div[@class="content-item user-item-box"]')
            if result_ele:
                status = self.finds_by_condition('xpath', '//div[@class="content-item user-item-box"]/span[2]')[0].get_attribute('innerText')
                if '已邀请' in status:
                    Logger.info('该用户已被邀请')
                    self.close_invite_view()
                    return True
                self.click_by_condition_index('xpath', '//div[@class="content-item user-item-box"]/span[contains(text(), "邀请")]', -1, '邀请')
            if self.wait_until_xpath('//p[contains(text(), "邀请加入成功")]'):
                Logger.info('邀请成功')
                self.close_invite_view()
                return True
        else:
            self.click_by_condition_index('class', 'copy-url-btn', -1, '复制链接')
            if self.wait_until_xpath('//p[contains(text(), "复制链接成功")]'):
                Logger.info('复制链接成功')
                url = self.finds_by_condition('class', 'url')[-1].get_attribute('innerText').strip()
                Logger.info(url)
                self.close_invite_view()
                return url

    def accept_invite(self, url):
        self.open_page(url)
        if self.check_condition('xpath', '//p[contains(text(), "你已在项目内")]'):
            Logger.info('你已在项目内')
            self.click_by_condition('class', 'join-btn')
        elif self.check_condition('class', 'join-btn'):
            self.click_by_condition('class', 'join-btn', '加入项目')
            time.sleep(3)
        else:
            Logger.error('界面异常')
            assert 0

    def accept_shoot_invite(self, url):
        self.open_page(url)
        self.refresh()
        if self.check_condition('xpath', '//div[contains(text(), "进入拍摄项目")]'):
            Logger.info('你已在项目内')
            self.click_by_condition('xpath', '//div[contains(text(), "进入拍摄项目")]')
            time.sleep(5)
            for i in range(4):
                if self.check_condition('class', 'skip-btn'):
                    self.click_by_condition('class', 'skip-btn')
                    break
                time.sleep(3)
        elif self.check_condition('xpath', '//div[contains(text(), "加入拍摄项目")]'):
            self.click_by_condition('xpath', '//div[contains(text(), "加入拍摄项目")]')
            time.sleep(3)
            for i in range(4):
                if self.check_condition('class', 'skip-btn'):
                    self.click_by_condition('class', 'skip-btn')
                    break
                time.sleep(3)
        else:
            Logger.error('界面异常')
            assert 0

    def check_join(self):
        join_pro_list = self.finds_by_condition('xpath', '//div[@class="cardList-clone-wrapper "]')
        for join_pro in join_pro_list:
            if project_name in join_pro.get_attribute('innerText'):
                Logger.info('参与项目检测到测试项目，加入成功')
                return True
        Logger.info('参与项目未检测到测试项目')
        return False

    def check_invite(self):
        if self.check_join():
            return True
        Logger.error('邀请失败')
        assert 0

    def close_member_setting_view(self):
        self.click_by_condition_index('xpath', '//div[@class="header-content-box"]/i', -1, '关闭成员管理界面')

    def remove_member(self, member=''):
        if not member:
            Logger.info('未检测到用户参数，默认删除所有用户')
        member_ele_list = self.finds_by_condition('class', 'infinite-list-item')
        while len(member_ele_list) > 1:
            for i in range(1, len(member_ele_list)):
                cur_member = self.find_by_condition('xpath', f'//li[@class="infinite-list-item"][{i+1}]/div[1]/span[1]').get_attribute('innerText').strip()
                if (not member) or (member and cur_member == member):
                    self.click_by_condition('xpath', f'//li[@class="infinite-list-item"][{i+1}]/div[@class="ops-wrapper"]', '设置')
                    self.click_by_condition_index('xpath', '//div[contains(text(), "移除成员")]', -1, '移除成员')
                    self.click_by_condition('xpath', '//div[contains(text(), "移除 ")]', '移除')
                    if self.wait_until_xpath('//p[contains(text(), "移除成员成功")]'):
                        Logger.info('移除成员成功')
                        time.sleep(3)
                        if member:
                            self.close_member_setting_view()
                            return True
                        break
            else:
                Logger.info('未检测到用户！')
                assert 0
            member_ele_list = self.finds_by_condition('class', 'infinite-list-item')
        else:
            Logger.info('项目内成员为1，无法删除')
        self.close_member_setting_view()

    def change_role(self, member=''):
        """修改成员角色身份"""
        if not member:
            Logger.error('未检测到用户参数!')
            assert 0
        member_ele_list = self.finds_by_condition('class', 'infinite-list-item')
        for i in range(1, len(member_ele_list)):
            cur_member = self.find_by_condition('xpath',
                                                f'//li[@class="infinite-list-item"][{i + 1}]/div[1]/span[1]').\
                                                get_attribute('innerText').strip()
            if cur_member == member:
                cur_role = self.find_by_condition('xpath',
                                        f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="role"]').\
                                        get_attribute('innerText').strip()
                change_role = '成员' if cur_role == '管理员' else '管理员'
                self.click_by_condition('xpath',
                                        f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="ops-wrapper"]',
                                        '设置')
                self.click_by_condition_index('xpath', f'//span[contains(text(), "{change_role}")]', -1, f'{change_role}')
                if self.wait_until_text(text='操作成功') and self.find_by_condition('xpath',
                                                        f'//li[@class="infinite-list-item"][{i + 1}]/div[@class="role"]').\
                                                        get_attribute('innerText').strip() == change_role:
                    Logger.info(f'修改成员-{member} 角色成功：{cur_role}->{change_role}')
                    time.sleep(3)
                    break
        else:
            Logger.info('未检测到该成员！')
            assert 0
        self.close_member_setting_view()

    def open_project(self, p_name=project_name):
        """点击项目名，打开项目"""
        try:
            setting_ele = self.finds_by_condition('xpath', f'//span[contains(text(), "{p_name}")]')
            if len(setting_ele) > 1:
                Logger.info('检测到相关项目不止一个，默认使用第一个测试')
            setting_ele[0].click()
            time.sleep(1)
        except:
            Logger.error('未找到测试项目，请检查项目是否存在！')
            assert 0

    def get_project_file_list(self):
        """获取项目文件列表"""
        return self.finds_by_condition('class', 'card-wrapper')

    def select_all_file(self):
        """全选"""
        file_list = self.get_project_file_list()  # 获取所有文件
        file_count = len(file_list)  # 获取文件数
        if file_count == 0:
            Logger.error('该项目无文件')
            assert 0
        Logger.info('选中文件')
        file_list[0].click()  # 选中第一个文件
        time.sleep(1)
        self.click_by_condition('xpath', '//div[contains(text(), "全选")]')  # 点击全选
        if self.check_condition('xpath', '//div[contains(text(), "取消全选")]'):
            Logger.info('检测到「取消全选」，点击全选成功')
        select_count_ele = self.find_by_condition('xpath', '//div[contains(text(), "已选中")]')  # 获取已选中文件文案
        select_count = re.findall(r'(\d+)', self.get_text(select_count_ele))[0]  # 正则获取选中文件数
        if eval(select_count) == file_count:  # 通过文件数判断全选是否成功
            Logger.info(f'选中数量「{select_count}」和文件数量「{file_count}」一致，全选成功')
            return True
        else:
            Logger.info(f'选中数量「{select_count}」和文件数量「{file_count}」不一致，全选失败')
            self.click_by_text('button', '取消', False)
            assert 0

    def unselect_file(self):
        """取消全选"""
        file_list = self.get_project_file_list()  # 获取项目文件列表
        file_count = len(file_list)  # 获取文件总数
        if file_count == 0:
            Logger.error('该项目无文件')
            assert 0
        Logger.info('选中文件')
        file_list[0].click()  # 选择第一个文件
        time.sleep(1)
        self.click_by_condition('xpath', '//div[contains(text(), "全选")]')  # 点击全选
        if self.check_condition('xpath', '//div[contains(text(), "取消全选")]'):  # 点击全选后，会出现取消全选文本
            Logger.info('检测到「取消全选」，点击全选成功')
        self.click_by_condition('xpath', '//div[contains(text(), "取消全选")]')  # 点击取消全选
        select_count_ele = self.find_by_condition('xpath', '//div[contains(text(), "已选中")]')  # 获取已选中文案
        select_count = re.findall(r'(\d+)', self.get_text(select_count_ele))[0]  # 正则获取选中数量
        if eval(select_count) == 0:  # 通过数量判断是否取消成功
            Logger.info('选中数量为0，取消选中成功')
            return True
        else:
            Logger.info('选中数量不为0，取消选中失败')
            self.click_by_text('button', '取消', False)
            assert 0

    def close_choose_file(self):
        """取消选择文件"""
        self.click_by_text('button', '取消', False)

    def choose_test_file(self, index=0):
        """点击选择测试文件，index选择第几个测试文件"""
        self.get_project_file_list()[index].click()
        time.sleep(3)

    def pre_view(self):
        """点击空格预览"""
        self.click_space()

    def check_pre_view(self):
        """通过检测对话框是否存在，检测预览是否成功"""
        if self.check_condition('class', 'dialog-content'):
            Logger.info('检测预览状态成功')
        else:
            Logger.error('预览失败')
            assert 0

    def change_file_name_by_info(self):
        """修改文件名"""
        # 获取文件名元素
        file_name_ele = self.finds_by_condition('xpath', '//div[@class="header-folder-box"]//input')[0]
        file_name = file_name_ele.get_attribute('value').strip()  # 获取文件名，首尾去空格
        Logger.info(f'当前文件名为：{file_name}')
        file_type = file_name.split('.')[-1]  # 获取文件后缀
        change_name = f'change_name.{file_type}'  # 组合新文件名
        file_name_ele.clear()  # 输入框清空
        file_name_ele.send_keys(change_name)  # 输入新文件名
        time.sleep(1)
        pyautogui.press('Return')  # 回车确定
        time.sleep(3)
        project_file = self.find_by_condition('xpath', '//div[@class="subInfo-title"]/span')  # 获取修改后文件名
        if project_file.get_attribute('innerText').strip() == change_name:  # 对比判断
            Logger.info(f'修改文件名--{change_name} 成功')
        else:
            Logger.error('修改文件名失败')
            assert 0

    def get_file_grade(self):
        # 通过获取星星元素数量判断当前评分
        grade_num = len(self.finds_by_condition('class', 'starFill'))
        Logger.info(f'当前评分为--{grade_num}')
        return grade_num

    def change_file_grade_by_info(self):
        """修改文件评分"""
        cur_grade = self.get_file_grade()  # 获取当前评分
        if cur_grade == 5:  # 5星则评分降低，否则默认加1星测试
            change_grade = 4
        else:
            change_grade = cur_grade + 1
        Logger.info(f'设置评分为：{change_grade}颗🌟')
        # python索引比实际序列小1位
        self.click_by_condition_index('xpath', '//div[@class="rate-icon-wrap"]/span', change_grade - 1)
        if self.get_file_grade() == change_grade:  # 判断打分后结果和打分是否一致
            Logger.info('评分设置成功')
        else:
            Logger.error('评分设置失败')
            assert 0

    def change_file_discription_by_info(self):
        """修改文件描述"""
        dis_info = '这是一条描述'
        # 获取描述输入框
        discription_ele = self.finds_by_condition('xpath', '//div[@class="el-collapse-item__content"]//input')[0]
        discription_ele.clear()  # 清空输入框文本
        Logger.info('输入描述')
        discription_ele.send_keys(dis_info)  # 输入描述
        time.sleep(1)
        pyautogui.press('Return')  # 回车确定
        time.sleep(3)
        cur_discription = discription_ele.get_attribute('value').strip()  # 获取输入框文本
        Logger.info(f'当前描述为：{cur_discription}')
        if cur_discription == dis_info:  # 判断是否和输入内容一致
            Logger.info('描述修改成功')
        else:
            Logger.error('描述修改失败')
            assert 0

    def add_file_tag(self, index=0):
        """添加标签"""
        tag_list = self.finds_by_condition('xpath', '//p[contains(text(), "全部标签")]/../ul/li')  # 获取标签列表
        choose_tag = tag_list[index].get_attribute('innerText').strip()  # 获取标签文本
        tag_list[index].click()  # 点击选中标签
        time.sleep(1)
        self.click_by_text('span', '添加', False)  # 点击添加
        return choose_tag  # 返回选中的标签，后续判断使用

    def change_file_tag_by_info(self):
        """修改文件标签"""
        self.click_by_condition('xpath', '//div[@class="file-tickets-cmp"]')  # 点击添加标签
        tag = self.add_file_tag()  # 选中标签，添加
        cur_tag = self.find_by_condition('class', 'ticket-name').get_attribute('innerText').strip()  # 获取当前文件标签
        if cur_tag == tag:  # 判断当前标签是否和选中的标签一致
            Logger.info('添加标签成功')
        else:
            Logger.error('添加标签失败')
            assert 0
        self.click_by_condition('class', 'delete-box', '删除标签')
        if self.check_condition('class', 'ticket-name'):  # 检测标签元素是否存在
            Logger.info('检测到标签，删除失败')
        else:
            Logger.info('删除标签成功')

    def change_file_link_by_info(self):
        """修改文件链接"""
        link_url = 'www.baidu.com'
        # 获取添加链接元素
        link_ele = self.finds_by_condition('xpath', '//div[@class="el-collapse-item__content"]//input')[1]
        link_ele.clear()  # 清空输入框
        link_ele.send_keys(link_url)  # 输入url
        time.sleep(1)
        pyautogui.press('Return')
        time.sleep(3)
        cur_link = link_ele.get_attribute('value').strip()  # 获取当前输入框内容
        if cur_link == link_url:
            Logger.info('添加链接成功')
        else:
            Logger.error('添加链接失败')
            assert 0
        cur_handle = self.driver.current_window_handle  # 获取当前窗口
        Logger.info(f'当前窗口为：{cur_handle}')
        self.click_by_condition('class', 'tolink', '打开链接')
        all_handle = self.driver.window_handles  # 获取所有标签页
        Logger.info(f'窗口列表为：{all_handle}')
        if len(all_handle) == 2:  # 通过判断是否存在两个标签页判断链接是否打开成功
            Logger.info('打开链接成功')
            self.driver.switch_to.window(cur_handle)  # 切回阅流工作台
            time.sleep(3)
        else:
            Logger.error('打开链接失败')
            assert 0

    def create_dir_by_file(self):
        """通过选中文件创建文件夹"""
        self.choose_test_file(-1)  # 选中最后一个文件
        self.click_by_text('div', '用所选文件新建文件夹')
        self.click_by_text('div', '确认')
        time.sleep(3)
        if self.check_condition('xpath', '//span[text()="文件夹"]'):  # 新建成功后会出现文件夹文本
            Logger.info('新建文件夹成功')
        else:
            Logger.error('新建文件夹失败')
            assert 0

    def copy_all_files(self, to_project=''):
        """复制所有文件"""
        self.select_all_file()  # 选中所有文件
        self.click_by_condition('class', 'iconfuzhi_fuzhi', '复制到')  # 点击复制到
        self.click_by_condition_index('class', 'tab-item', 0, '项目')  # 点击项目
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{to_project}")]', -1)  # 点击复制到项目
        self.click_by_text('div', '确定')  # 点击确定
        if self.wait_until_text(ele_type='strong', text='您复制到项目的文件已成功', timeout=30):  # 检测通知
            Logger.info('检测到复制成功通知')
        else:
            Logger.error('未检测到复制成功通知')
            assert 0
        file_count = len(self.get_project_file_list())  # 项目内文件数
        self.open_project(to_project)  # 打开被复制项目
        new_count = len(self.get_project_file_list())  # 获取被复制项目内文件数
        if new_count == file_count:  # 对比是否一致
            Logger.info('检测到被复制项目文件数相同，复制成功')
        else:
            Logger.error('被复制项目和测试项目文件数不一致，复制失败')
            assert 0

    def move_all_files(self, to_project=''):
        """移动所有文件"""
        before_move_count = len(self.get_project_file_list())  # 获取移动前，项目文件数
        self.select_all_file()  # 选中所有文件
        self.click_by_condition('class', 'iconmove', '移动到')  # 点击移动到
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{to_project}")]', -1)  # 选择移动到项目
        self.click_by_text('div', '确定')  # 点击确定
        if self.wait_until_text(text='移动成功', timeout=30):  # 检测移动成功toast
            Logger.info('检测到移动成功通知')
        else:
            Logger.error('未检测到移动成功通知')
            assert 0
        after_move_count = len(self.get_project_file_list())  # 获取移动后，项目文件数
        self.open_project(to_project)  # 打开被移动项目
        new_count = len(self.get_project_file_list())  # 获取项目文件数
        if new_count == before_move_count and after_move_count == 0:  # 判断移动文件数是否正确，原项目文件是否为0
            Logger.info('检测到被移动项目文件数相同，移动成功')
        else:
            Logger.error('被移动项目和测试项目文件数不一致，移动失败')
            assert 0

    def download_all_files(self):
        """下载所有文件"""
        shutil.rmtree(self.download_path)  # 清空下载文件夹
        os.mkdir(self.download_path)
        self.select_all_file()  # 选中所有文件
        self.click_by_condition('class', 'iconjiaofu_download', '批量下载')  # 点击下载
        self.click_by_text('div', '确认下载')  # 二次确认
        self.click_by_img('allow_download', '允许下载多个文件')  # 浏览器授权允许下载多个文件
        time.sleep(10)
        file_count = len(self.get_project_file_list())  # 获取当前项目文件数
        download_count = len(os.listdir(self.download_path))  # 通过检测下载文件夹文件数判断下载是否成功
        if download_count == file_count:
            Logger.info('检测到下载文件夹文件数相同，下载成功')
        else:
            Logger.error('下载文件夹和测试项目文件数不一致，下载失败')
            assert 0


Chrome = WebAuto(ChromeAuto().driver)
time.sleep(1)
FireFox = WebAuto(FireFoxAuto().driver)
