from code.web import Chrome, FireFox
from code.base_case import BaseCase
from code.parse import usr_2, pwd_2
from code.parse import usr_3, pwd_3


class TestCaseInviteByLink(BaseCase):
    def test_invite_link(self):
        """链接邀请测试"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('邀请成员', 5)
        url = Chrome.invite_member(super=False, company=False)
        FireFox.login_by_password(usr_2, pwd_2)
        FireFox.accept_invite(url)
        FireFox.check_invite()

        FireFox.login_out()
        FireFox.login_by_password(usr_3, pwd_3)
        FireFox.accept_invite(url)
        FireFox.check_invite()