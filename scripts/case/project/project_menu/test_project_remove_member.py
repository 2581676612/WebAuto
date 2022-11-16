from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    def test_remove_member(self):
        """项目设置-移除用户"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('成员管理')
        Chrome.Project.remove_member(FireFox.Control.user_name)