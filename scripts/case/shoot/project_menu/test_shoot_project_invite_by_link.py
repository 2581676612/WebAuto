import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.parse import usr_2, pwd_2


class TestCase():
    @pytest.mark.P0
    def test_invite_link(self):
        """拍摄项目设置-链接邀请测试"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('添加成员', 5)
        url = Chrome.Shoot.copy_invite_link(role='管理者')
        FireFox.Shoot.accept_invite(url)
        FireFox.Shoot.check_invite()
