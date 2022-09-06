from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_delete(self):
        """项目设置-删除项目"""
        Chrome.Project.delete_project()
