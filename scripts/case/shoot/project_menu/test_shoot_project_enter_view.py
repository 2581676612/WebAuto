from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_enter(self):
        """首页-进入拍摄首页"""
        Chrome.Shoot.enter_shoot_page()
