import importlib.machinery
import inspect
import os
import screeninfo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from core.base import parse
from core.base.common import Common


class FireFox(object):
    def __init__(self):
        driver_path = os.path.join(parse.main_path, 'statics', 'tools',
                                   parse.firefox_driver)
        option = webdriver.FirefoxOptions()
        # option.add_argument('--headless')  # 不打开可视化界面
        option.add_argument('disable-infobars')  # 取消浏览器提示信息
        option.add_argument('--no-sandbox')  # 在root权限下打开浏览器
        option.add_argument('--ignore-certificate-errors')
        width = screeninfo.get_monitors()[0].width
        height = screeninfo.get_monitors()[0].height
        option.add_argument(f'--window-size={width},{height}')  # 专门应对无头浏览器中不能最大化屏幕的方案
        s = Service(driver_path)
        self.driver = webdriver.Firefox(service=s, options=option)
        self.driver.minimize_window()  # 浏览器最小化显示，可视化界面有效，隐藏显示无效
        self.get_all_modules()

    def get_all_modules(self):
        modules_list = Common.get_class_name()
        for name, cl in modules_list:
            setattr(FireFox, name, cl(self.driver))


if parse.firefox_run.lower() == 'true':
    FireFox = FireFox()
else:
    FireFox = None