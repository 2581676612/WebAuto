from code.web import Chrome, FireFox
from code.base_case import BaseCase


class TestCase(BaseCase):
    def test_close(self):
        """退出浏览器"""
        Chrome.quit()
        FireFox.quit()
