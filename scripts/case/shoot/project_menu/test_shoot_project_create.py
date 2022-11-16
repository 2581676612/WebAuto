import pytest

from core.browser.chrome import Chrome


class TestCase():
    @pytest.mark.P0
    def test_create(self):
        """拍摄项目设置-创建项目"""
        Chrome.Shoot.create_project()

    def test_create_exist(self):
        """拍摄项目设置-创建重名项目"""
        Chrome.Shoot.create_project_exist()
