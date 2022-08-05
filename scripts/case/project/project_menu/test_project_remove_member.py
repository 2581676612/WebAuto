from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name


class TestCaseRemoveMember(BaseCase):
    def test_remove_member(self):
        """移除用户测试"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('成员管理')
        Chrome.Project.remove_member(usr_2_name)