from code.web import Chrome
from code.base_case import BaseCase


class TestCaseFangLuPing(BaseCase):
    def test_fangluping_open(self):
        """防录屏权限开启测试"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('项目设置')
        Chrome.set_fangluping(True)
        Chrome.check_fangluping(True)

    def test_fangluping_close(self):
        """防录屏权限关闭测试"""
        Chrome.open_project_menu()
        Chrome.open_project_settings('项目设置')
        Chrome.set_fangluping(False)
        Chrome.check_fangluping(False)

