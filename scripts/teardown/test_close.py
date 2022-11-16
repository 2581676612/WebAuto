import pytest

from core.browser.chrome import Chrome
from core.browser.firefox import FireFox


class TestCase():
    @pytest.mark.P0
    def test_close(self):
        """退出浏览器"""
        Chrome.Control.quit()
        if FireFox:
            FireFox.Control.quit()
