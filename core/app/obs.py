import os
import platform
import pyautogui
import time

from core.base import parse
from core.base.logger import logger
from core.base.cv import ImgDeal


class OBS(object):
    def __init__(self):
        self.img_path = os.path.join(parse.main_path, 'statics', 'obs')
        self.is_start = False

    @staticmethod
    def click_keyboard(*args, interval=0.25):
        logger.info(f'模拟键盘操作：{args}')
        pyautogui.hotkey(*args, interval=interval)
        time.sleep(1)

    def get_img_position(self, img, info=None):
        """检测文件是否存在,获取坐标"""
        pos = ImgDeal.find_by_img(os.path.join(self.img_path, img), info)
        if pos:
            return pos
        else:
            assert 0

    def check_img(self, img, info=None):
        """检测文件是否存在"""
        return ImgDeal.find_by_img(os.path.join(self.img_path, img), info)

    def click_by_img(self, img, info, timeout=3):
        """根据图片获取坐标并点击"""
        pos = self.get_img_position(img, info)
        self.click_by_position(pos)
        time.sleep(timeout)

    @staticmethod
    def click_by_position(pos):
        """根据坐标点击"""
        cur_x, cur_y = pyautogui.position()
        logger.info(f'点击坐标--{pos[0]}, {pos[1]}')
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()
        pyautogui.moveTo(cur_x, cur_y)
        time.sleep(2)

    def start(self, app='OBS'):
        """启动app"""
        pt = platform.system().lower()
        logger.info(f'当前操作系统为：{pt}')
        if pt in ['mac', 'darwin']:
            os.system(f'open /Applications/{app}.app')
            if self.is_start:
                logger.info('等待2秒，打开app窗口')
                time.sleep(2)
            else:
                self.is_start = True
                logger.info('等待5秒，app启动')
                time.sleep(5)
        else:
            logger.error('当前系统未适配，请适配')
            assert 0

    def open_settings(self):
        """打开设置"""
        self.click_by_img('setting', '设置')

    def open_push_settings(self):
        """打开推流设置"""
        try:
            self.click_by_img('push_setting', '推流设置')
        except:
            self.click_by_img('push_setting_1', '推流设置')

    def set_push_server(self):
        """设置推流服务器"""
        server_pos = self.get_img_position('server')
        self.click_by_position((server_pos[0] + 100, server_pos[1]))
        self.click_keyboard('command', 'a')
        self.click_keyboard('command', 'v')

    def submit(self):
        """点击确定"""
        self.click_by_img('submit', '确定')

    def start_push(self):
        """开始推流"""
        self.click_by_img('start_push', '开始推流')

    def stop_push(self):
        """停止推流"""
        if self.check_img('cancel', '取消设置'):
            self.click_by_img('cancel', '取消')
        else:
            self.click_by_img('stop_push', '停止推流')

    def quit(self):
        """退出app"""
        if self.check_img('cancel', '取消设置'):
            self.click_by_img('cancel', '取消')
        self.click_by_img('quit', '退出')
        self.is_start = False


OBS = OBS()
