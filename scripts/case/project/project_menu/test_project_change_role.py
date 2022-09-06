from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name


class TestCase(BaseCase):
    def test_change_role(self):
        """项目设置-修改成员角色"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('成员管理')
        Chrome.Project.change_role(usr_2_name)
