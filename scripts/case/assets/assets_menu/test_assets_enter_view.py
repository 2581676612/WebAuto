from core.browser.chrome import Chrome


class TestCase():
    def test_enter_assets_view(self):
        """资产首页-进入首页"""
        Chrome.Assets.enter_assets_view()