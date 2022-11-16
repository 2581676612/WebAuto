from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    def test_invite(self):
        """项目设置-企业内邀请"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        Chrome.Project.invite_member(FireFox.Control.user_name)
