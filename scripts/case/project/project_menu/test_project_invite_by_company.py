from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name, usr_3_name


class TestCaseInviteByCompany(BaseCase):
    def test_invite(self):
        """企业内邀请测试"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        Chrome.Project.invite_member(usr_2_name)

    def test_invite_third(self):
        """第三方邀请测试"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        Chrome.Project.invite_member(usr_3_name)
