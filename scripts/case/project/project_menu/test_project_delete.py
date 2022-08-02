from code.web import Chrome
from code.base_case import BaseCase


class TestCase(BaseCase):
    def test_delete(self):
        """删除项目"""
        Chrome.delete_project()
