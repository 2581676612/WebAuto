import pytest

from core.browser.chrome import Chrome


class TestCase():
    @pytest.mark.P0
    def test_delete(self):
        """拍摄项目设置-删除项目"""
        Chrome.Shoot.delete_project()
