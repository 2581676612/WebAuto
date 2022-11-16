import os
import platform
import time

import pyautogui
import importlib.machinery
import inspect
import zipfile

from core.base.logger import logger
from core.base.cv import ImgDeal
from core.base import parse


class Common(object):
    def __init__(self):
        self.obs_img_path = os.path.join(parse.main_path, 'statics', 'obs')

    @staticmethod
    def get_class_name():
        cls_list = []
        dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modules')
        file_list = [f for f in os.listdir(dir_path) if '.py' in f]
        file_name_list = [f[:-3] for f in file_list]
        module = ''
        for file in file_list:
            file = os.path.join(dir_path, file)
            module = importlib.machinery.SourceFileLoader('all_module', file).load_module()
        for cls in inspect.getmembers(module, inspect.isclass):
            if cls[0].lower() in file_name_list:
                cls_list.append(cls)
        return cls_list

    @staticmethod
    def click_by_position(pos):
        """根据坐标点击"""
        cur_x, cur_y = pyautogui.position()
        logger.info(f'点击坐标--{pos[0]}, {pos[1]}')
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()
        pyautogui.moveTo(cur_x, cur_y)
        time.sleep(2)

    @staticmethod
    def get_img_position(img, info=None):
        """检测文件是否存在,获取坐标"""
        pos = ImgDeal.find_by_img(img, info)
        if pos:
            return pos
        else:
            assert 0

    @staticmethod
    def click_keyboard(*args, interval=0.25):
        logger.info(f'模拟键盘操作：{args}')
        pyautogui.hotkey(*args, interval=interval)
        time.sleep(1)

    def click_by_img(self, img, info, timeout=2):
        """根据图片获取坐标并点击"""
        pos = self.get_img_position(img, info)
        self.click_by_position(pos)
        time.sleep(timeout)

    @staticmethod
    def unzip_file(zip_src, dst_dir):
        r = zipfile.is_zipfile(zip_src)
        if r:
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                fz.extract(file, dst_dir)
        else:
            logger.info('非ZIP类型文件！')
