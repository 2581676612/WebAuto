import os
import time
import pyautogui
import platform
import pyperclip
import pytest
import random
import re
import shutil
import selenium.common.exceptions as ex
import core.base.parse as parse

from core.base.logger import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from core.base.report import Report
from core.base.cv import ImgDeal


class Control(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver_status = True
        if parse.web_type == 'None':
            self.url = 'https://yueliu.cn/v20/#/'
        else:
            self.url = f'https://{parse.web_type}.yueliu.cloud/v20/#/'
        self.img_path = os.path.join(parse.main_path, 'statics', 'img_demo')
        self.download_path = os.path.join(parse.main_path, 'statics', 'downloads')
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        self.first_enter_shoot = True
        self.first_enter_project = True
        self.cur_handle = self.driver.current_window_handle  # 获取当前窗口

    def quit(self):
        # 关闭Chromedriver
        logger.info('关闭浏览器！')
        self.driver.quit()
        self.driver_status = False

    @staticmethod
    def click_space():
        """模拟键盘空格"""
        logger.info('点击空格')
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        time.sleep(3)

    def click_by_img(self, img='', info=''):
        """根据图片点击，图片模版在code-file下"""
        cur_x, cur_y = pyautogui.position()
        img_pos = ImgDeal.find_by_img(os.path.join(self.img_path, img), info)
        if img_pos:
            logger.info(f'移动到坐标--{img_pos[0]}, {img_pos[1]}')
            pyautogui.moveTo(img_pos[0], img_pos[1])
            logger.info(f'点击{info}')
            pyautogui.click()
            time.sleep(2)
            pyautogui.moveTo(cur_x, cur_y)
            return True
        return False

    def check_img(self, img='', info=''):
        """图片检测，图片模版在code-file下"""
        if info:
            logger.info(f'检测图片--{info} 是否存在')
        if ImgDeal.find_by_img(os.path.join(self.img_path, img), info):
            logger.info('检测到图片')
            return True
        logger.error('未检测到图片')
        return False

    def click_by_position(self, x, y, left_click=True):  # 此方法不生效，暂不使用
        """根据坐标点击"""
        if left_click:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.driver).move_by_offset(x, y).context_click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()

    def screen(self):
        """浏览器截图"""
        current_time = str(time.strftime('%y_%m_%d_%H_%M_%S', time.localtime()))
        screen_path = os.path.join(Report.report_path, 'screen')
        if not os.path.exists(screen_path):
            os.makedirs(screen_path)
        file = os.path.join(screen_path, f'{current_time}.png')
        self.driver.get_screenshot_as_file(file)
        return file

    def open_page(self, url=None):
        """打开url"""
        logger.info(f'访问url：{url}')
        self.driver.get(url)
        time.sleep(3)

    def check_alert(self):
        """弹窗检测"""
        try:
            alert = self.driver.switch_to.alert
            logger.info(f'检测到弹窗--{alert}')
            return alert
        except ex.NoAlertPresentException as e:
            return False

    def _hover(self, ele=''):  # ActionChains模块不生效，无法使用
        """控制鼠标悬停"""
        ActionChains(self.driver).move_to_element(ele).perform()

    def hover(self, img=''):
        """图像识别匹配位置，鼠标悬停"""
        img_pos = ImgDeal.find_by_img(os.path.join(self.img_path, f'{img}'))
        if img_pos:
            logger.info(f'移动到坐标--{img_pos[0]}, {img_pos[1]}')
            pyautogui.moveTo(img_pos[0], img_pos[1])
            return True
        else:
            assert 0

    def _find_by_condition(self, condition='class', obj=None):
        """查询元素"""
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
        """
        根据条件查询元素
        :param condition:  查询属性类型 class/id/xpath
        :param obj:  查询属性
        :return:
        """
        try:
            return self._find_by_condition(condition, obj)
        except ex.NoSuchElementException as e:
            logger.error(f'未找到该元素：{condition}--{obj}')
            assert 0
        except ex.ElementNotInteractableException as e:
            logger.error(f'该元素被隐藏，或不止一个：{condition}--{obj}')
            assert 0

    def _finds_by_condition(self, condition='class', obj=None):
        """查询元素（多个）"""
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
        """
        根据条件查找（可能存在多个元素）
        :param condition:  查询属性类型
        :param obj:  查询属性
        :return:
        """
        try:
            return self._finds_by_condition(condition, obj)
        except ex.NoSuchElementException as e:
            logger.error(f'未找到该元素：{condition}--{obj}')
            assert 0

    def click_by_condition(self, condition='class', obj=None, info=None, timeout=2):
        """
        根据条件点击
        :param condition: 查询属性类型 class/id/xpath
        :param obj: 查询属性
        :param info: 存在，则log打印
        :param timeout: 点击后，等待时间
        :return:
        """
        if condition == 'link_text':
            logger.info(f'点击--{obj}')
        elif info:
            logger.info(f'点击--{info}')
        self.find_by_condition(condition, obj).click()
        time.sleep(timeout)

    def click_by_condition_index(self, condition='class', obj=None, index=-1, info=None, timeout=2):
        """
        根据条件点击（检测到多个元素）
        :param condition: 查询属性类型 class/id/xpath
        :param obj: 查询属性
        :param index: 索引
        :param info: 存在，则log打印
        :param timeout: 点击后，等待时间
        :return:
        """
        if condition == 'link_text':
            logger.info(f'点击--{obj}')
        elif info:
            logger.info(f'点击--{info}')
        self.finds_by_condition(condition, obj)[index].click()
        time.sleep(timeout)

    def wait_until_xpath(self, xpath, timeout=10, wait=1):
        """等待直到检测到xpath元素
            xpath--元素路径
            timeout--检测超时时间
            wait--检测间隔
        """
        # 超时时间为10秒，每1秒检查1次，直到元素出现
        if WebDriverWait(self.driver, timeout, wait).until(ec.visibility_of_element_located((By.XPATH, xpath))):
            return True
        else:
            logger.error('未检测到该元素！')
            return False

    def wait_until_text(self, ele_type='*', text='', timeout=10, wait=0.2):
        """等待直到检测到文本
            ele_type--元素类型
            text--文本
            timeout--检测超时时间
            wait--检测间隔
        """
        # 超时时间为10秒，每1秒检查1次，直到元素出现
        xpath = f'//{ele_type}[contains(text(), "{text}")]'
        try:
            WebDriverWait(self.driver, timeout, wait).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except ex.TimeoutException as e:
            logger.error('未检测到该文本！')
            return False

    def refresh(self, timeout=5):
        """刷新页面"""
        self.driver.refresh()
        time.sleep(timeout)

    def check_button(self, text=''):
        """检测按钮是否存在"""
        try:
            ele = self.find_by_condition('xpath', f'//button[contains(text(), "{text}")]')
            return ele
        except ex.NoSuchElementException as e:
            return False

    def click_by_js(self, button='', timeout=2):
        """通过js点击"""
        self.driver.execute_script("arguments[0].click()", button)
        time.sleep(timeout)

    @staticmethod
    def get_text(ele):
        """获取元素文本"""
        return ele.get_attribute('innerText').strip()

    def check_text(self, ele_type='', text='', fuzzy=True):
        """检测文本是否存在
            ele_type--元素类型 div/span/i/p
            text--文本
            fuzzy--模糊匹配
        """
        if not ele_type:
            ele_type = '*'
        if not text:
            logger.error('请输入文本')
            assert 0
        if fuzzy:
            return self.check_condition('xpath', f'//{ele_type}[contains(text(), "{text}")]')
        else:
            return self.check_condition('xpath', f'//{ele_type}[text()="{text}"]')

    def click_by_text(self, ele_type='', text='', fuzzy=True, timeout=2):
        """根据文本点击
            ele_type--元素类型 div/span/i/p
            text--文本
            fuzzy--模糊匹配
        """
        if not ele_type:
            ele_type = '*'
        if not text:
            logger.error('请输入文本')
            assert 0
        if fuzzy:
            self.click_by_condition('xpath', f'//{ele_type}[contains(text(), "{text}")]', text, timeout)
        else:
            self.click_by_condition('xpath', f'//{ele_type}[text()="{text}"]', text, timeout)
        time.sleep(1)


    def check_condition(self, condition, obj):
        """检测元素是否存在"""
        try:
            e = self.finds_by_condition(condition, obj)
            if len(e) == 0:
                return False
            return True
        except ex.NoSuchElementException as e:
            return False

    def choose_file_to_upload(self, file='', select_all=False):
        """选择文件上传"""
        # 请选择test_file目录下的测试文件
        file_path = os.path.join(parse.main_path, 'statics', 'upload_file')
        file = os.path.join(file_path, file)
        logger.info(f'上传文件为：{file}')
        pyperclip.copy(file)  # 复制文件路径
        platform_str = platform.system().lower()  # 获取操作系统
        logger.info(f'操作系统为：{platform_str}')
        if platform_str in ['mac', 'darwin']:
            # 打开文件搜索框
            logger.info('打开搜索框')
            self.click_keyboard('shift', 'command', 'g')  # 打开mac的搜索框，可以直接输入文件全路径定位到具体文件
            time.sleep(2)
            # 粘贴文件路径
            logger.info('粘贴文件路径')
            self.click_keyboard('command', 'v')
            time.sleep(2)
            # 回车确定

            pyautogui.press('Return')
            time.sleep(1)  # 必须停留一下，从粘贴到连续键入两个回车键有问题
            if select_all:
                logger.info('全选')
                self.click_keyboard('command', 'a')
                time.sleep(1)
            pyautogui.press('Return')
        elif 'windows' in platform_str:
            self.click_keyboard('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('enter')
        time.sleep(3)

    def login_by_password(self, usr=parse.usr_1, pwd=parse.pwd_1):
        """密码登录"""
        url = self.url + 'login'
        self.open_page(url)
        self.click_by_condition('xpath', '//li[contains(text(), "密码登录")]', '密码登录')
        logger.info('输入账号')
        self.finds_by_condition('class', 'el-input__inner')[0].clear()
        self.finds_by_condition('class', 'el-input__inner')[0].send_keys(usr)
        time.sleep(1)
        logger.info('输入密码')
        self.finds_by_condition('class', 'el-input__inner')[1].clear()
        self.finds_by_condition('class', 'el-input__inner')[1].send_keys(pwd)
        time.sleep(1)
        self.click_by_condition('class', 'login-btn-container', '登录')
        time.sleep(5)
        if self.find_by_condition('class', 'avatar-wrapper'):
            logger.info('登录成功！')
        else:
            logger.error('登录失败！')
            pytest.exit('登录失败，测试停止！')
        self.close_update_info()
        self.close_message()

    @staticmethod
    def create_user():
        """测试环境随机创建用户"""
        user_start_list = ['130', '139', '150', '186']
        user_start = random.sample(user_start_list, 1)[0]
        user_end = str(random.randint(10000000, 99999999))
        user = f'{user_start}{user_end}'
        logger.info(f'随机账号为：{user}')
        return user

    def login_by_code(self, usr=parse.usr_1, code='888888'):
        """验证码登录"""
        url = self.url + 'login'
        self.open_page(url)
        logger.info('输入账号')
        self.finds_by_condition('class', 'el-input__inner')[0].clear()
        self.finds_by_condition('class', 'el-input__inner')[0].send_keys(usr)
        time.sleep(1)
        logger.info('输入验证码')
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
            logger.info('登录成功！')
        else:
            logger.error('登录失败！')
            pytest.exit('登录失败，测试停止！')
        time.sleep(5)
        self.close_update_info()
        self.close_message()

    def login_out(self):
        """退出登录"""
        self.click_by_condition_index('class', 'avatar-wrapper', 1, '用户头像')
        self.click_by_condition('xpath', '//div[contains(text(), "退出登录")]', '退出登录')
        self.click_by_condition('xpath', '//div[text()="退出 "]', '退出', 3)

    def close_update_info(self):
        """关闭更新弹窗"""
        if self.check_condition('class', 'footer') and not self.check_condition('class', 'close-box'):
            close_ele = self.finds_by_condition('class', 'footer')
            if close_ele:
                logger.info('点击关闭更新提示')
                close_ele[0].click()
                time.sleep(2)

    def close_message(self):
        """关闭通知"""
        while self.check_condition('class', 'close-box'):
            logger.info('点击关闭消息提示')
            self.finds_by_condition('class', 'close-box')[0].click()
            time.sleep(3)

    def open_upload_page(self):
        """打开上传记录"""
        upload_ele = self.find_by_condition('class', 'uploadList')
        if upload_ele.get_attribute('aria-hidden') == 'true':
            logger.info('上传进度弹窗为隐藏状态')
            self.click_by_condition('class', 'iconchuanshu_chuanshu', '打开传输窗口')
        else:
            logger.info('上传进度弹窗为显示状态')

    def close_upload_page(self):
        """关闭上传记录"""
        upload_ele = self.find_by_condition('class', 'uploadList')
        if upload_ele.get_attribute('aria-hidden') == 'true':
            logger.info('上传进度弹窗为隐藏状态')
        else:
            logger.info('上传进度弹窗为显示状态，点击关闭')
            button_ele = self.find_by_condition('class', 'iconchuanshu_chuanshu')
            self.driver.execute_script("arguments[0].click();", button_ele)
            time.sleep(3)
            # self.click_by_condition('class', 'iconchuanshu_chuanshu', '关闭传输窗口')

    def is_file_upload(self):
        """检测是否存在文件上传"""
        if self.check_condition('xpath', '//span[contains(text(), "没有正在上传的文件")]'):
            logger.info('没有正在上传的文件')
            self.close_upload_page()
            return False
        else:
            return True

    def clear_upload_record(self):
        """清空上传记录"""
        while self.is_file_upload():
            self.click_by_condition('class', 'el-dropdown', '更多设置')
            self.click_by_condition('class', 'el-dropdown-menu__item', '清空已完成记录')
        else:
            logger.info('清除成功')

    def wait_upload(self):
        """等待上传成功"""
        self.open_upload_page()  # 打开上传记录
        if not self.is_file_upload():  # 检测是否存在文件上传
            logger.info('没有正在上传的文件')
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
                    logger.info('文件上传完成！')
                    time.sleep(5)
                    self.clear_upload_record()
                    self.close_upload_page()
                    success = True
                else:
                    logger.info(status)
                    time.sleep(5)
            else:
                logger.error('文件上传超时！')
                self.close_upload_page()
                assert 0

    @staticmethod
    def click_upload_img():
        """处理上传文件夹alert提示"""
        upload_pos = ImgDeal.find_upload()
        if upload_pos:
            logger.info(f'移动到坐标--{upload_pos[0]}, {upload_pos[1]}')
            pyautogui.moveTo(upload_pos[0], upload_pos[1])
            logger.info('点击坐标')
            pyautogui.click()
            time.sleep(2)

    def new_user_skip(self):
        """处理新手引导"""
        while True:
            if self.check_condition('xpath', '//span[text()="知道了"]'):
                self.click_by_text('span', '知道了', False)
            time.sleep(0.5)

    @staticmethod
    def get_copy_text():
        """获取剪切板文本"""
        return pyperclip.paste()

    def show_browser(self):
        """浏览器显示在最前面"""
        self.hide_browser()
        time.sleep(2)
        self.driver.maximize_window()
        time.sleep(1)

    def hide_browser(self):
        """浏览器最小化"""
        self.driver.minimize_window()

    @staticmethod
    def is_video(file_name):
        if '.' in file_name:
            file_type = file_name.split('.')[-1]
            if file_type in parse.file_type_dict['video']:
                logger.info(f'检测到视频类文件--{file_name}')
                return True
        return False

    def get_ele_width(self, ele):
        """获取元素宽度"""
        width = re.findall(r'width: +(\d+.?\d+)px', self.get_ele_style(ele))
        if width:
            return int(eval(width[0]))
        else:
            return 0

    @staticmethod
    def get_ele_style(ele):
        """获取元素样式"""
        return ele.get_attribute('style').strip()

    def check_download(self, file_count):
        download_count = len(os.listdir(self.download_path))  # 通过检测下载文件夹文件数判断下载是否成功
        logger.info(f'下载文件数量为：{download_count}')
        shutil.rmtree(self.download_path)  # 清空下载文件夹
        os.mkdir(self.download_path)
        if download_count == file_count:
            logger.info('检测到下载文件夹文件数相同，下载成功')
        else:
            logger.error('下载文件夹和测试项目文件数不一致，下载失败')
            assert 0

    def switch_to_another_page(self):
        """切换到另一个标签页"""
        all_windows = self.driver.window_handles
        for handle in all_windows:
            if handle != self.cur_handle:
                logger.info(f'检测到新标签页，点击切换标签页')
                self.driver.switch_to.window(handle)
                time.sleep(2)
                break
        else:
            logger.error('获取另一个标签页异常')
            assert 0

    def switch_to_main_page(self):
        """切回主标签页"""
        logger.info('切回主标签页')
        self.driver.switch_to.window(self.cur_handle)
        time.sleep(2)

    def open_another_page(self, url):
        """新的标签页打开页面"""
        new_window = f'window.open("{url}")'
        self.driver.execute_script(new_window)
        time.sleep(3)

    def get_media_file_count(self):
        """获取资源文件数"""
        media_file_ele = self.find_by_condition('xpath', '//span[contains(text(), "个文件")]')
        media_file_count = int(re.findall(r'(\d+)个文件', self.get_text(media_file_ele))[0])
        logger.info(f'当前资源文件数为：{media_file_count}')
        return media_file_count

    @staticmethod
    def click_keyboard(*args, interval=0.25):
        logger.info(f'模拟键盘操作：{args}')
        pyautogui.hotkey(*args, interval=interval)

    def close_another_page(self):
        """关闭其他标签页"""
        self.switch_to_another_page()
        self.driver.close()
        self.switch_to_main_page()