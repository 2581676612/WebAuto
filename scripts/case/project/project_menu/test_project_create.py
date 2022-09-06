from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_create(self):
        """项目设置-创建项目"""
        Chrome.Project.create_project()
