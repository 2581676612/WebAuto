import cv2
import os
import pyautogui
import numpy as np
import core.base.parse as parse
from core.base.logger import logger


class ImgDeal():
    def __init__(self):
        self.template_file = os.path.join(parse.main_path, 'statics', 'img_demo', 'screen.png')
        self.upload_file = os.path.join(parse.main_path, 'statics', 'img_demo', 'upload')
        self.screen_width, self.screen_height = pyautogui.size()

    def find_by_img(self, img, info=''):
        if info:
            logger.info(f'图像识别查找--{info}')
        screen = pyautogui.screenshot()
        screen_dpi = int(screen.size[0] / self.screen_width)
        screen.save(self.template_file)
        temp = cv2.cvtColor(np.asarray(screen), cv2.COLOR_RGB2BGR)
        tar = cv2.imread(f'{img}.png')
        height, width = tar.shape[:2]
        res = cv2.matchTemplate(tar, temp, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val > 0.1:
            logger.info('未匹配到该图像，请重新替换匹配文件或确认程序是否运行在主屏幕')
            return False
        # 保存识别图像
        # cv2.rectangle(temp, min_loc, (min_loc[0] + width, min_loc[1] + height), (0, 0, 225), 2)
        # current_time = str(time.strftime('%y_%m_%d_%H_%M_%S', time.localtime()))
        # img_path = os.path.join(Report.report_screen, f'find_{current_time}.png')
        # logger.info(f'识别文件截图为：{img_path}')
        # cv2.imwrite(img_path, temp, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        pos = ((min_loc[0] + width // 2) // screen_dpi, (min_loc[1] + height // 2) // screen_dpi)
        logger.info(f'检测到图像，中心坐标为--{pos}')
        return pos

    def find_upload(self):
        return self.find_by_img(self.upload_file, '上传')

    @staticmethod
    def sift_detect(img1, img2):
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        bf = cv2.BFMatcher()
        matches = bf.match(des1, des2)
        sort_list = list(matches)
        sort_list.sort(key=lambda x: x.distance)
        return kp1[sort_list[0].queryIdx].pt


ImgDeal = ImgDeal()
