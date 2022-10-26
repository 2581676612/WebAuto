import time
import pyautogui

from core.modules.control import Control
from core.base.logger import logger
from core.base import parse


class Assets(Control):
    def enter_assets_view(self):
        """进入资产界面"""
        url = self.url + 'assets'
        self.open_page(url)

    def create_assets_group(self, group=parse.project_name):
        """创建资产组"""
        if self.check_my_assets_group(group):
            self.delete_assets_group(group)
        self.click_by_condition('class', 'iconjiahao_jiahao', '创建资产组')
        logger.info('输入资产组名称')
        group_name = self.find_by_condition('class', 'rename-input')
        group_name.clear()
        group_name.send_keys(group)
        pyautogui.press('enter')
        if self.wait_until_text(text='创建成功'):
            logger.info('创建资产组成功')
            return True
        else:
            logger.error('未检测到创建成功提示')
            assert 0

    def open_all_assets(self):
        """打开全部资产"""
        self.click_by_condition('xpath', '//span[text()="全部资产"]/..', '全部资产')

    def open_warehousing(self):
        """打开待入库"""
        self.click_by_condition('xpath', '//span[text()="待入库"]/..', '待入库')

    def open_my_assets_group(self, group=parse.project_name):
        """打开我的资产组"""
        self.click_by_condition('xpath', f'//span[contains(text(), "我的资产组")]/../..//div[text()="{group}"]', group)

    def open_join_assets_group(self, group=parse.project_name):
        """打开参与资产组"""
        self.click_by_condition('xpath', f'//span[contains(text(), "参与资产组")]/../..//div[text()="{group}"]', group)

    def open_assets_group_menu(self, group=parse.project_name):
        """打开资产组更多设置"""
        self.open_my_assets_group(group)
        self.click_by_condition('xpath', f'//div[text()="{group}"]/../../span[3]', '更多设置')

    def open_assets_group_setting(self, setting=''):
        """打开资产组设置"""
        self.click_by_condition_index('xpath', f'//div[contains(text(), "{setting}")]', -1, setting)

    def check_my_assets_group(self, group=parse.project_name):
        """检测我的资产组是否存在"""
        if self.check_condition('xpath', f'//span[contains(text(), "我的资产组")]/../..//div[text()="{group}"]'):
            logger.info(f'检测到资产组--{group}')
            return True
        else:
            logger.info(f'未检测到资产组--{group}')
            return False

    def delete_assets_group(self, group=parse.project_name):
        """删除资产组"""
        self.open_assets_group_menu(group)
        self.open_assets_group_setting('删除')
        self.click_by_text(ele_type='span', text=' 删除 ', fuzzy=False, timeout=0.1)
        if self.wait_until_text(text='删除成功'):
            logger.info('删除成功')
        else:
            logger.error('未检测到「删除成功」')
            assert 0

    def rename_assets_group(self, group=parse.project_name, new_name=''):
        """重命名资产组"""
        self.open_assets_group_menu(group)
        self.open_assets_group_setting('重命名')
        group_name = self.find_by_condition('class', 'rename-input')
        group_name.clear()
        group_name.send_keys(new_name)
        pyautogui.press('enter')
        if self.wait_until_text(text='修改成功'):
            logger.info('修改成功')
            time.sleep(2)
        else:
            logger.error('未检测到「修改成功」')
            assert 0

    def upload_file(self, file='', select_all=True):
        """上传文件"""