from core.browser.chrome import Chrome


class TestCase():
    def test_by_plan(self):
        """会员方案"""
        Chrome.Shoot.check_buy_plan_link()
        Chrome.Shoot.enter_shoot_page()

    def test_convert(self):
        """兑换会员码"""
        Chrome.Shoot.check_convert()
        Chrome.Control.close_dialog()
