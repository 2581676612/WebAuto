import pytest

from core.browser.chrome import Chrome


class TestCase():
    @pytest.mark.P0
    def test_enter(self):
        """首页-进入拍摄首页"""
        Chrome.Shoot.enter_shoot_page()
