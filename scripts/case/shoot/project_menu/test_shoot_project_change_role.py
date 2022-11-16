import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    @pytest.mark.P0
    def test_change_role(self):
        """拍摄项目设置-修改成员角色"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('成员管理')
        Chrome.Shoot.change_role(FireFox.Control.user_name)
