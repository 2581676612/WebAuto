from core.browser.chrome import Chrome
from core.base.base_case import BaseCase
from core.base.parse import usr_2_name, usr_3_name


class TestCase(BaseCase):
    def test_invite(self):
        """项目设置-企业内邀请"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        Chrome.Project.invite_member(usr_2_name)

    def test_invite_third(self):
        """项目设置-第三方邀请"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        Chrome.Project.invite_member(usr_3_name)
