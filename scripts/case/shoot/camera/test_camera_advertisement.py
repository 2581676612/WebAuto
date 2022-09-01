from core.browser.chrome import Chrome
from core.base.base_case import BaseCase


class TestCase(BaseCase):
    def test_advertisement(self):
        """机位列表页-广告位"""
        Chrome.Shoot.open_project()
        Chrome.Shoot.check_advertisement(status='open')
        Chrome.Shoot.close_advertisement()
        Chrome.Shoot.check_advertisement(status='close')
        Chrome.Shoot.login_out()
        Chrome.Shoot.login_by_password()
        Chrome.Shoot.enter_shoot_page()
        Chrome.Shoot.open_project()
        Chrome.Shoot.check_advertisement(status='open')


