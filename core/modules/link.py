import time


from core.modules.control import Control
from core.base.logger import logger


class Link(Control):
    def enter_link_view(self):
        """进入链接模块首页"""
        url = self.url + 'links'
        self.open_page(url)

    def close_project_share_permission(self, *args):
        """关闭分享设置权限"""
        for s in args:
            ele = self.find_by_condition('xpath', f'//p[text()="{s}"]/../../span/span/div')
            if 'is-checked' in ele.get_attribute('class'):
                logger.info(f'{s} 权限为开启状态，点击关闭')
                ele.click()
                time.sleep(2)
            else:
                logger.info(f'{s} 权限为关闭状态')

    def open_project_share_settings(self, index=0):
        """打开审阅分享设置"""
        self.click_by_condition_index('class', 'icongengduo_gengduo', index, '更多设置')
        self.click_by_condition_index('xpath', '//li[contains(text(), "分享设置")]', -1, '分享设置')

    def close_share_setting_dialog(self):
        """关闭分享设置界面"""
        self.click_by_condition('xpath', '//div[@class="dialog-header-content"]/i')
