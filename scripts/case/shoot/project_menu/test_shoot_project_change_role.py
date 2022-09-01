from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name


class TestCase(BaseCase):
    def test_change_role(self):
        """拍摄项目设置-修改成员角色"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('成员管理')
        Chrome.Shoot.change_role(usr_2_name)
