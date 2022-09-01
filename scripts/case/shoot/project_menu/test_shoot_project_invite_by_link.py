from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.base_case import BaseCase
from core.base.parse import usr_2, pwd_2
from core.base.parse import usr_3, pwd_3


class TestCase(BaseCase):
    def test_invite_link(self):
        """拍摄项目设置-链接邀请测试"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('添加成员', 5)
        url = Chrome.Shoot.copy_invite_link(role='管理者')
        FireFox.Control.login_by_password(usr_2, pwd_2)
        FireFox.Shoot.accept_invite(url)
        FireFox.Shoot.check_invite()
        #
        # FireFox.Project.login_out()
        # FireFox.Project.login_by_password(usr_3, pwd_3)
        # FireFox.Project.accept_invite(url)
        # FireFox.Project.check_invite()