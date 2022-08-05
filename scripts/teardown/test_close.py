from core.browser.chrome import Chrome
from core.browser.firefox import FireFox
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_close(self):
        """退出浏览器"""
        Chrome.Control.quit()
        if FireFox:
            FireFox.Control.quit()
