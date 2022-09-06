from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.base_case import BaseCase
from core.base.parse import usr_2, pwd_2
from core.base.parse import usr_3, pwd_3


class TestCase(BaseCase):
    def test_invite_link(self):
        """项目设置-链接邀请"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        url = Chrome.Project.invite_member(super=False, company=False)
        FireFox.Project.login_by_password(usr_2, pwd_2)
        FireFox.Project.accept_invite(url)
        FireFox.Project.check_invite()

        # FireFox.Project.login_out()
        # FireFox.Project.login_by_password(usr_3, pwd_3)
        # FireFox.Project.accept_invite(url)
        # FireFox.Project.check_invite()