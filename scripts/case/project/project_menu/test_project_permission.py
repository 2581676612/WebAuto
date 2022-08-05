from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCaseFangLuPing(BaseCase):
    def test_fangluping_open(self):
        """防录屏权限开启测试"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('项目设置')
        Chrome.Project.set_fangluping(True)
        Chrome.Project.check_fangluping(True)

    def test_fangluping_close(self):
        """防录屏权限关闭测试"""
        Chrome.Project.open_project_menu()
        Chrome.Project.open_project_settings('项目设置')
        Chrome.Project.set_fangluping(False)
        Chrome.Project.check_fangluping(False)

