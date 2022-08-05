import os
import time
import pyautogui
import platform
import pyperclip
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

    def wait_until_text(self, ele_type='p', text='', timeout=10, wait=1):
        """等待直到检测到文本
            ele_type--元素类型
            text--文本
            timeout--检测超时时间
            wait--检测间隔
        """
        # 超时时间为10秒，每1秒检查1次，直到元素出现
        xpath = f'//{ele_type}[contains(text(), "{text}")]'
        if WebDriverWait(self.driver, timeout, wait).until(ec.visibility_of_element_located((By.XPATH, xpath))):
            return True
        else:
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

    def click_by_text(self, ele_type='', text='', fuzzy=True):
        """根据文本点击
            ele_type--元素类型 div/span/i/p
            text--文本
            fuzzy--模糊匹配
        """
        if ele_type and text:
            if fuzzy:
                self.click_by_condition('xpath', f'//{ele_type}[contains(text(), "{text}")]')
            else:
                self.click_by_condition('xpath', f'//{ele_type}[text()="{text}"]', text)
            time.sleep(1)
        else:
            logger.error('请输入元素类型及文本')
            assert 0

    def check_condition(self, condition, obj):
        """检测元素是否存在"""
        try:
            e = self.finds_by_condition(condition, obj)
            if len(e) == 0:
                return False
            return True
        except ex.NoSuchElementException as e:
            return False

    @staticmethod
    def choose_file_to_upload(file='', select_all=False):
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
            logger.info('粘贴文件路径')
            pyautogui.hotkey('command', 'v')
            time.sleep(2)
            # 回车确定
            pyautogui.press('Return')
            time.sleep(1)  # 必须停留一下，从粘贴到连续键入两个回车键有问题
            if select_all:
                logger.info('全选')
                pyautogui.hotkey('command', 'a')
                time.sleep(1)
            pyautogui.press('Return')
        elif 'windows' in platform_str:
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            pyautogui.press('enter')
        time.sleep(3)
