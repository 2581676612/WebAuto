from code.web import Chrome, FireFox
from code.base_case import BaseCase
from code.parse import usr_2_name, usr_3_name


class TestCaseRemoveMember(BaseCase):
    def test_remove_member(self):
        """移除用户测试"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('成员管理')
        Chrome.remove_member(usr_2_name)