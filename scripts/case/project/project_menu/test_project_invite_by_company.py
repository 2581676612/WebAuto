from code.web import Chrome, FireFox
from code.base_case import BaseCase
from code.parse import usr_2_name, usr_3_name


class TestCaseInviteByCompany(BaseCase):
    def test_invite(self):
        """企业内邀请测试"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('邀请成员', 5)
        Chrome.invite_member(usr_2_name)

    def test_invite_third(self):
        """第三方邀请测试"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('邀请成员', 5)
        Chrome.invite_member(usr_3_name)
