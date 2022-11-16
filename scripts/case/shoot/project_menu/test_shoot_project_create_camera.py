import pytest

from core.browser.chrome import Chrome


class TestCase():
    @pytest.mark.P0
    def test_remove_camera(self):
        """拍摄项目设置-删除机位"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.remove_camera()

    @pytest.mark.P0
    def test_create_camera(self):
        """拍摄项目设置-创建机位"""
        Chrome.Shoot.open_project_menu()
        Chrome.Shoot.open_project_settings('创建机位')
        Chrome.Shoot.create_camera()
