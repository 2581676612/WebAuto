import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    @pytest.mark.P0
    def test_remove_member(self):
        """拍摄项目设置-移除用户测试"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('成员管理')
        Chrome.Shoot.remove_member(FireFox.Control.user_name)