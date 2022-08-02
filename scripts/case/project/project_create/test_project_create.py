from code.web import Chrome
from code.base_case import BaseCase


class TestCase(BaseCase):
    def test_create(self):
        """创建项目"""
        Chrome.create_project()
