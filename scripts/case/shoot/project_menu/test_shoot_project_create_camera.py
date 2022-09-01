from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_remove_carema(self):
        """拍摄项目设置-删除机位"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.remove_camera('测试机位-自动化')

    def test_create_carema(self):
        """拍摄项目设置-创建机位"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('创建机位')
        Chrome.Shoot.create_camera('测试机位-自动化')
