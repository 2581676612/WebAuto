from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name


class TestCase(BaseCase):
    def test_remove_member(self):
        """拍摄项目设置-移除用户测试"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('成员管理')
        Chrome.Shoot.remove_member(usr_2_name)