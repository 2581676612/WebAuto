from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    def test_invite_link(self):
        """项目设置-链接邀请"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('邀请成员', 5)
        url = Chrome.Project.invite_member(super=False, company=False)
        FireFox.Project.accept_invite(url)
        FireFox.Project.check_invite()
