import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.parse import usr_2, pwd_2


class TestCase():
    @pytest.mark.P0
    def test_invite_with_verify(self):
        """拍摄项目设置-带审核邀请"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('拍摄设置', 5)
        Chrome.Shoot.set_join_verify(open=True)
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('添加成员', 5)
        url = Chrome.Shoot.copy_invite_link(role='管理者')
        # FireFox.Control.login_by_password(usr_2, pwd_2)
        FireFox.Shoot.open_page(url)
        FireFox.Shoot.refresh()
        FireFox.Shoot.check_join_verify()
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('成员管理', 5)
        Chrome.Shoot.allow_join_project(FireFox.Control.user_name)
        Chrome.Shoot.close_member_setting_view()
        Chrome.Shoot.close_message()
        FireFox.Shoot.check_invite()
