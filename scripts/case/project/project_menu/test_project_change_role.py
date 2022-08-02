from code.web import Chrome
from code.base_case import BaseCase
from code.parse import usr_2_name


class TestCase(BaseCase):
    def test_change_role(self):
        """修改成员角色"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('成员管理')
        Chrome.change_role(usr_2_name)
