from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name


class TestCase(BaseCase):
    def test_remove_member(self):
        """项目设置-移除用户"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('成员管理')
        Chrome.Project.remove_member(usr_2_name)